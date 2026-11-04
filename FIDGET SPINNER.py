import io
import math
import sys
import urllib.request
import pygame
pygame.init()
START_WIDTH,START_HEIGHT=900,640
FPS=60
SPINNER_BASE_SIZE=280
FRICTION=0.985
MAX_SPIN_SPEED=35
SPIN_GAIN=0.35
#colors
WHITE=(245,247,255)
SOFT_WHITE=(220,225,240)
BLUE=(0,110,255)
RED=(225,85,85)
YELLOW=(240,205,80)
MINT=(90,200,170)
GRAY=(210,210,210)  
SHADOW=(10,10,30)
PANEL=(18,24,48,160)
SPINNER_URLS = [
    "https://pngimg.com/uploads/fidget_spinner/fidget_spinner_PNG82.png",
    "https://pngimg.com/uploads/fidget_spinner/small/fidget_spinner_PNG82.png",
    "https://pngimg.com/uploads/fidget_spinner/small/fidget_spinner_PNG81.png",
    "https://pngimg.com/uploads/fidget_spinner/small/fidget_spinner_PNG80.png",
]
FALLBACK_COLORS=[BLUE,RED,YELLOW,MINT]
BACKGROUND_COLORS = [
    (20, 30, 95),
    (80, 20, 100),
    (10, 90, 80),
    (100, 40, 20),
    (15, 15, 15),
]
def create_fallback_spinner(size,accent_color):
    """Create a simple spinner surface when an online asset is unavailable."""
    width,height=size
    center=(width//2,height//2)
    radius=min(width,height)//2-18
    arm_offset=radius//2+18
    arm_radius=max(24,radius//3)
    surface=pygame.Surface(size,pygame.SRCALPHA)
    pygame.draw.circle(surface,(*SHADOW,60),center,radius+6)
    for degrees in (0,120,240):
        angle=math.radians(degrees)
        arm_center=(int(center[0]+math.cos(angle)*arm_offset),int(center[1]+math.sin(angle)*arm_offset),)
        pygame.draw.line(surface,GRAY,center,arm_center,18)
        pygame.draw.circle(surface,accent_color,arm_center,arm_radius)
        pygame.draw.circle(surface,WHITE,arm_center,arm_radius//2)
        pygame.draw.circle(surface,GRAY,center,radius//3)
        pygame.draw.circle(surface,WHITE,center,radius//6)
    return surface

def load_online_image(url,size):
    """Load a PNG from a URL and scale it, or return None on failure."""
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            image_data=io.BytesIO(response.read())
            image=pygame.image.load(image_data).convert_alpha()
            return pygame.transform.smoothscale(image,size)
    except Exception:
        return None

def build_spinner_set(size):
    spinners = []
    for index, url in enumerate(SPINNER_URLS):
        spinner = load_online_image(url, size)
        if spinner is None:
            spinner = create_fallback_spinner(size, FALLBACK_COLORS[index])
        spinners.append(spinner)
    return spinners

    
def draw_background(surface, base_color):
    width, height = surface.get_size()

    for y in range(height):
        blend = y / max(1, height - 1)

        red = int(base_color[0] + 35 * blend)
        green = int(base_color[1] + 55 * blend)
        blue = int(base_color[2] + 40 * blend)

        pygame.draw.line(surface, (min(255, red), min(255, green), min(255, blue)), (0, y), (width, y))

    for offset, radius, alpha in ((0.18, 150, 28), (0.74, 120, 24), (0.5, 210, 18)):
        glow = pygame.Surface((width, height), pygame.SRCALPHA)
        center = (int(width * offset), int(height * 0.28 + radius * 0.2))
        pygame.draw.circle(glow, (255, 255, 255, alpha), center, radius)
        surface.blit(glow, (0, 0))

def draw_panel(surface, rect):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, PANEL, panel.get_rect(), border_radius=18)
    surface.blit(panel, rect.topleft)

def angle_from_center(position, center):
    dx = position[0] - center[0]
    dy = position[1] - center[1]
    return math.degrees(math.atan2(dy, dx))

def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))

def main():
    screen = pygame.display.set_mode((START_WIDTH, START_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Fidget Spinner")
    clock = pygame.time.Clock()
    title_font = pygame.font.Font(None, 40)
    body_font = pygame.font.Font(None, 26)
    hint_font = pygame.font.Font(None, 24)

    spinner_size = (SPINNER_BASE_SIZE, SPINNER_BASE_SIZE)
    spinners = build_spinner_set(spinner_size)

    current_spinner = 0
    current_background = 0
    spinner_angle = 0.0
    angular_speed = 0.0
    dragging = False
    last_mouse_angle = None
    spin_count = 0
    top_speed = 0.0
    running = True
    while running:
        width, height = screen.get_size()
        spinner_center = (width // 2, height // 2 + 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_SPACE, pygame.K_RIGHT):
                    current_spinner = (current_spinner + 1) % len(spinners)
                elif event.key == pygame.K_LEFT:
                    current_spinner = (current_spinner - 1) % len(spinners)
                elif event.key == pygame.K_r:
                    spinner_angle = 0.0
                    angular_speed = 0.0
                    spin_count = 0
                    top_speed = 0.0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                    last_mouse_angle = angle_from_center(event.pos, spinner_center)
                elif event.button == 3:
                    current_background = (current_background + 1) % len(BACKGROUND_COLORS)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False
                last_mouse_angle = None
            elif event.type == pygame.MOUSEMOTION and dragging:
                mouse_angle = angle_from_center(event.pos, spinner_center)
                if last_mouse_angle is not None:
                    delta = (mouse_angle - last_mouse_angle + 180) % 360 - 180
                    spinner_angle += delta
                    angular_speed = clamp(delta * SPIN_GAIN, -MAX_SPIN_SPEED, MAX_SPIN_SPEED)
                last_mouse_angle = mouse_angle
                angular_speed *= FRICTION
        if abs(angular_speed) < 0.01:
            angular_speed = 0.0
        spinner_angle += angular_speed


        spin_count += abs(angular_speed) / 360
        top_speed = max(top_speed, abs(angular_speed))


        draw_background(screen, BACKGROUND_COLORS[current_background])


        rotated = pygame.transform.rotate(spinners[current_spinner], -spinner_angle)
        rect = rotated.get_rect(center=spinner_center)
        screen.blit(rotated, rect)


        panel_rect = pygame.Rect(20, 20, min(360, width - 40), 120)
        draw_panel(screen, panel_rect)


        title = title_font.render(f"Spinner {current_spinner + 1}/{len(spinners)}", True, WHITE)
        speed = body_font.render(f"Speed: {abs(angular_speed):.1f} deg/frame", True, SOFT_WHITE)
        best = body_font.render(f"Top speed: {top_speed:.1f}  |  Spins: {spin_count:.1f}", True, SOFT_WHITE)


        screen.blit(title, (panel_rect.x + 16, panel_rect.y + 14))
        screen.blit(speed, (panel_rect.x + 16, panel_rect.y + 56))
        screen.blit(best, (panel_rect.x + 16, panel_rect.y + 84))

        hint = hint_font.render(
            "Left drag: spin  |  Right click: change background  |  Space: next spinner  |  R: reset  |  Esc: quit",
            True,
            WHITE,
        )
        hint_rect = hint.get_rect(center=(width // 2, height - 28))
        screen.blit(hint, hint_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()