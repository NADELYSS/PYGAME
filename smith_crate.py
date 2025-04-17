import pygame
from settings import PLAYER_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW

# 대장간 상태 변수
crate_state = "idle"
crate_frame_index = 0
smith_open = [False]

# 이미지 로딩
crate_idle = pygame.image.load("./asset/smith/crate_idle.png").convert_alpha()
crate_peak = pygame.image.load("./asset/smith/crate_peak2.png").convert_alpha()

# 프레임 추출 (열리는 애니메이션 6프레임)
peak_frames = []
for i in range(6):
    frame = crate_peak.subsurface(pygame.Rect(i * 16, 0, 16, 16))
    peak_frames.append(frame)

# 대장간 UI 창 설정
smith_window = pygame.Rect(150, 120, 500, 300)
smith_close_button = pygame.Rect(smith_window.right - 40, smith_window.top + 10, 20, 20)

# 대장간 상자 위치
crate_rect = pygame.Rect(450, 200, PLAYER_SIZE, PLAYER_SIZE)


# 🔧 대장간 상호작용 함수
def update_and_draw_crate(screen, player, font, small_font, event, current_map):
    global crate_state, crate_frame_index

    # 현재 맵이 아니면 리턴
    if current_map != "마을":
        return

    # 거리 계산
    player_center = player.rect.center
    crate_center = crate_rect.center
    distance = ((player_center[0] - crate_center[0]) ** 2 + (player_center[1] - crate_center[1]) ** 2) ** 0.5

    # 상태 전환 (거리 기반 애니메이션)
    if distance > 150:
        crate_state = "idle"
        crate_frame_index = 0
    elif distance <= 150 and distance > 120:
        crate_state = "peak"
        crate_frame_index = 0
    elif distance <= 120 and distance > 90:
        crate_state = "peak"
        crate_frame_index = 1
    elif distance <= 90 and distance > 60:
        crate_state = "peak"
        crate_frame_index = 2
    elif distance <= 60 and distance > 30:
        crate_state = "peak"
        crate_frame_index = 3
    elif distance <= 30:
        crate_state = "peak"
        crate_frame_index = 5  # 완전 열린 상태

    # SPACE 누르면 대장간 창 열기
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        if current_map == "마을" and crate_state == "peak" and crate_frame_index == 5:
            smith_open[0] = True

    # 상자 그리기
    if crate_state == "idle":
        image = pygame.transform.scale(crate_idle.subsurface(pygame.Rect(0, 0, 16, 16)), (PLAYER_SIZE, PLAYER_SIZE))
    else:
        frame = peak_frames[min(crate_frame_index, 5)]
        image = pygame.transform.scale(frame, (PLAYER_SIZE, PLAYER_SIZE))

    screen.blit(image, crate_rect.topleft)

    # 대장간 창 그리기
    if smith_open[0]:
        pygame.draw.rect(screen, (15, 15, 40), smith_window)
        pygame.draw.rect(screen, WHITE, smith_window, 2)
        pygame.draw.rect(screen, (100, 0, 0), smith_close_button)
        close_text = font.render("X", True, WHITE)
        screen.blit(close_text, close_text.get_rect(center=smith_close_button.center))

        label = small_font.render("대장간 기능은 아직 개발 중입니다.", True, YELLOW)
        screen.blit(label, label.get_rect(center=smith_window.center))


# 🔧 마우스 클릭 처리
def handle_smith_event(event):
    if smith_open[0] and event.type == pygame.MOUSEBUTTONDOWN:
        if smith_close_button.collidepoint(event.pos):
            smith_open[0] = False
