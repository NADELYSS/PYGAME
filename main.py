import pygame
import random

# 초기 설정
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("광산의 노동자")
clock = pygame.time.Clock()
font = pygame.font.Font("miner_game/fonts/NanumGothic.ttf", 24)
small_font = pygame.font.Font("miner_game/fonts/NanumGothic.ttf", 16)

# 색상 정의
GRAY = (60, 60, 60)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY_ROCK = (150, 150, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 플레이어 설정 (크기 40x40 → 32x32로 축소)
player = pygame.Rect(100, 100, 32, 32)
player_speed = 5

# 광물 클래스
class Mineral:
    def __init__(self, name, color, rect, hp):
        self.name = name
        self.color = color
        self.rect = rect
        self.hp = hp

# 자원 정보
mineral_names = ["돌", "철"]
mineral_colors = {
    "돌": GRAY_ROCK,
    "철": YELLOW
}
mineral_hps = {
    "돌": 1,
    "철": 2
}
mineral_weights = [80, 20]

# 광물 리스트
minerals = []

# 인벤토리 상태 (이름 → [숫자 리스트])
inventory = {
    "돌": [],
    "철": []
}

# 인벤토리 창
inventory_open = False
inventory_rect = pygame.Rect(250, 150, 300, 200)
close_button = pygame.Rect(inventory_rect.right - 30 - 10, inventory_rect.top + 10, 20, 20)

# 광물 생성 함수
def create_mineral():
    for _ in range(5):
        name = random.choices(mineral_names, weights=mineral_weights)[0]
        color = mineral_colors[name]
        hp = mineral_hps[name]

        x = random.randint(0, 770)
        y = random.randint(0, 570)
        new_rect = pygame.Rect(x, y, 30, 30)

        if player.colliderect(new_rect):
            continue
        if any(m.rect.colliderect(new_rect) for m in minerals):
            continue

        minerals.append(Mineral(name, color, new_rect, hp))
        break

# 초기 광물 생성
for _ in range(10):
    create_mineral()

# 리젠 이벤트 설정
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1800)

# 게임 루프
running = True
while running:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_EVENT:
            create_mineral()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for m in minerals:
                    if player.colliderect(m.rect):
                        m.hp -= 1
                        if m.hp <= 0:
                            # 인벤토리에 넣기 (99개 제한)
                            stacks = inventory[m.name]
                            if not stacks or stacks[-1] >= 99:
                                stacks.append(1)
                            else:
                                stacks[-1] += 1
                            minerals.remove(m)
                        break
            elif event.key == pygame.K_i:
                inventory_open = not inventory_open
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if inventory_open and close_button.collidepoint(event.pos):
                inventory_open = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player.x -= player_speed
    if keys[pygame.K_RIGHT]: player.x += player_speed
    if keys[pygame.K_UP]: player.y -= player_speed
    if keys[pygame.K_DOWN]: player.y += player_speed

    # 화면 밖 방지
    player.x = max(0, min(player.x, 800 - player.width))
    player.y = max(0, min(player.y, 600 - player.height))

    # 광물 + 체력바
    for m in minerals:
        pygame.draw.rect(screen, m.color, m.rect)

        max_hp = mineral_hps[m.name]
        hp_ratio = m.hp / max_hp

        if hp_ratio >= 0.7:
            bar_color = (0, 200, 0)
        elif hp_ratio >= 0.3:
            bar_color = (255, 215, 0)
        else:
            bar_color = (200, 0, 0)

        bar_width = m.rect.width
        bar_height = 4
        bar_x = m.rect.x
        bar_y = m.rect.y - bar_height - 2

        pygame.draw.rect(screen, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, bar_width * hp_ratio, bar_height))

    # 플레이어
    pygame.draw.rect(screen, RED, player)

    # 인벤토리 창
    if inventory_open:
        pygame.draw.rect(screen, (30, 30, 30), inventory_rect)
        pygame.draw.rect(screen, WHITE, inventory_rect, 2)

        pygame.draw.rect(screen, (100, 0, 0), close_button)
        close_text = font.render("X", True, WHITE)
        text_rect = close_text.get_rect(center=close_button.center)
        screen.blit(close_text, text_rect)

        # 인벤토리 그리기
        slot_size = 40
        margin = 10
        start_x = inventory_rect.x + margin
        start_y = inventory_rect.y + 50
        index = 0

        for name, stack_list in inventory.items():
            for count in stack_list:
                row = index // 5
                col = index % 5
                slot_x = start_x + col * (slot_size + margin)
                slot_y = start_y + row * (slot_size + margin)

                pygame.draw.rect(screen, mineral_colors[name], (slot_x, slot_y, slot_size, slot_size))

                label_text = small_font.render(f"{name} {count}개", True, WHITE)
                label_rect = label_text.get_rect(center=(slot_x + slot_size // 2, slot_y + slot_size + 10))
                screen.blit(label_text, label_rect)

                index += 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
