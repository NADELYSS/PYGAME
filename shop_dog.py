import pygame
from mineral import mineral_names

# 강아지 상태를 추적하기 위한 전역 변수
dog_state = "sleep"
dog_frame_index = 0

# 강아지 상태 갱신 및 화면 출력 함수
def update_and_draw_dog(screen, player, shop_rect, shop_dog_frames, event, current_map, shop_open, sell_selection):
    global dog_state, dog_frame_index

    # 거리 계산 (플레이어와 상점 중앙 기준)
    player_center = player.rect.center
    dog_pos = shop_rect.center
    distance = ((player_center[0] - dog_pos[0]) ** 2 + (player_center[1] - dog_pos[1]) ** 2) ** 0.5

    # 상태 결정
    if distance > 100:
        dog_state = "sleep"
    elif distance > 50:
        dog_state = "lay"
    elif distance > 30:
        dog_state = "sit"
    else:
        dog_state = "sit"

    # 애니메이션 프레임 인덱스 증가
    dog_frame_index += 0.05
    dog_frame = shop_dog_frames[dog_state][int(dog_frame_index) % 2]

    # 상태별 크기 비율 설정
    if dog_state == "sleep":
        scale_x, scale_y = 1.9, 1.5
    elif dog_state == "lay":
        scale_x, scale_y = 1.9, 1.5
    else:
        scale_x, scale_y = 1.3, 1.3

    # 이미지 크기 계산
    width = int(player.rect.width * scale_x)
    height = int(player.rect.height * scale_y)
    dog_scaled = pygame.transform.scale(dog_frame, (width, height))

    # 위치 중앙 정렬 후 화면에 출력
    dog_rect = dog_scaled.get_rect(center=shop_rect.center)
    screen.blit(dog_scaled, dog_rect.topleft)

    # 상점 열기: sit 상태 + 아직 안 열려있을 때만
    if event and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        if current_map == "마을" and dog_state == "sit" and not shop_open[0]:
            shop_open[0] = True
            for name in mineral_names:
                sell_selection[name] = 0
