import pygame
import random

# --- 초기 설정 ---
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("광산의 노동자")
clock = pygame.time.Clock()
font = pygame.font.Font("miner_game/fonts/NanumGothic.ttf", 24)
small_font = pygame.font.Font("miner_game/fonts/NanumGothic.ttf", 16)

# --- 색상 정의 ---
GRAY = (60, 60, 60)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY_ROCK = (150, 150, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
ORANGE = (255, 140, 0)

# --- 맵 & 창 상태 ---
current_map = "광산"
map_select_open = False
inventory_open = False
shop_open = False

# --- 게임 상태 ---
gold = 0
sell_selection = {"돌": 0, "철": 0}

# --- 창 위치 설정 ---
inventory_rect = pygame.Rect(250, 150, 300, 200)
close_button = pygame.Rect(inventory_rect.right - 40, inventory_rect.top + 10, 20, 20)
map_rect = pygame.Rect(200, 120, 400, 300)
map_close_button = pygame.Rect(map_rect.right - 40, map_rect.top + 10, 20, 20)
mine_button = pygame.Rect(map_rect.x + 50, map_rect.y + 100, 120, 80)
village_button = pygame.Rect(map_rect.x + 230, map_rect.y + 100, 120, 80)

# --- 마을 내 요소 ---
shop_rect = pygame.Rect(200, 200, 150, 100)
forge_rect = pygame.Rect(450, 200, 150, 100)
shop_window = pygame.Rect(150, 100, 500, 300)
shop_close_button = pygame.Rect(shop_window.right - 40, shop_window.top + 10, 20, 20)

# --- 플레이어 설정 ---
player = pygame.Rect(100, 100, 32, 32)
player_speed = 5

# --- 광물 클래스 ---
class Mineral:
    def __init__(self, name, color, rect, hp):
        self.name = name
        self.color = color
        self.rect = rect
        self.hp = hp

mineral_names = ["돌", "철"]
mineral_colors = {"돌": GRAY_ROCK, "철": YELLOW}
mineral_hps = {"돌": 1, "철": 2}
mineral_prices = {"돌": 1, "철": 2}
mineral_weights = [80, 20]
minerals = []

# --- 인벤토리 상태 ---
inventory = {"돌": [], "철": []}

# --- 광물 생성 함수 ---
def create_mineral():
    for _ in range(5):
        name = random.choices(mineral_names, weights=mineral_weights)[0]
        color = mineral_colors[name]
        hp = mineral_hps[name]
        x = random.randint(0, 770)
        y = random.randint(0, 570)
        new_rect = pygame.Rect(x, y, 30, 30)
        if player.colliderect(new_rect): continue
        if any(m.rect.colliderect(new_rect) for m in minerals): continue
        minerals.append(Mineral(name, color, new_rect, hp))
        break

# --- 초기 광물 생성 ---
for _ in range(10):
    create_mineral()

# --- 리젠 타이머 ---
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 2000)

# --- 게임 루프 ---
running = True
while running:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_EVENT and current_map == "광산":
            create_mineral()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_map == "광산":
                    for m in minerals:
                        if player.colliderect(m.rect):
                            m.hp -= 1
                            if m.hp <= 0:
                                stacks = inventory[m.name]
                                if not stacks or stacks[-1] >= 99:
                                    stacks.append(1)
                                else:
                                    stacks[-1] += 1
                                minerals.remove(m)
                            break
                elif current_map == "마을" and player.colliderect(shop_rect):
                    shop_open = True
                    sell_selection = {"돌": 0, "철": 0}
            elif event.key == pygame.K_i:
                inventory_open = not inventory_open
            elif event.key == pygame.K_m:
                map_select_open = not map_select_open
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if inventory_open and close_button.collidepoint(event.pos):
                inventory_open = False
            if map_select_open:
                if map_close_button.collidepoint(event.pos):
                    map_select_open = False
                elif mine_button.collidepoint(event.pos):
                    current_map = "광산"
                    map_select_open = False
                elif village_button.collidepoint(event.pos):
                    current_map = "마을"
                    map_select_open = False
            if shop_open:
                if shop_close_button.collidepoint(event.pos):
                    shop_open = False
                for i, name in enumerate(mineral_names):
                    base_y = shop_window.y + 60 + i * 60
                    plus = pygame.Rect(shop_window.x + 300, base_y, 30, 30)
                    minus = pygame.Rect(shop_window.x + 340, base_y, 30, 30)
                    maxbtn = pygame.Rect(shop_window.x + 380, base_y, 50, 30)
                    sellbtn = pygame.Rect(shop_window.x + 440, base_y, 50, 30)
                    if plus.collidepoint(event.pos):
                        total = sum(inventory[name]) if name in inventory else 0
                        if sell_selection[name] < total:
                            sell_selection[name] += 1
                    elif minus.collidepoint(event.pos):
                        if sell_selection[name] > 0:
                            sell_selection[name] -= 1
                    elif maxbtn.collidepoint(event.pos):
                        sell_selection[name] = sum(inventory[name])
                    elif sellbtn.collidepoint(event.pos):
                        count = sell_selection[name]
                        total = sum(inventory[name])
                        if count > 0 and total >= count:
                            gold += mineral_prices[name] * count
                            # 인벤토리에서 count만큼 제거
                            removed = 0
                            new_stacks = []
                            for stack in inventory[name]:
                                if removed + stack <= count:
                                    removed += stack
                                    continue
                                elif removed < count:
                                    new_stacks.append(stack - (count - removed))
                                    removed = count
                                else:
                                    new_stacks.append(stack)
                            inventory[name] = new_stacks
                            sell_selection[name] = 0

    # --- 키 입력 ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player.x -= player_speed
    if keys[pygame.K_RIGHT]: player.x += player_speed
    if keys[pygame.K_UP]: player.y -= player_speed
    if keys[pygame.K_DOWN]: player.y += player_speed
    player.x = max(0, min(player.x, 800 - player.width))
    player.y = max(0, min(player.y, 600 - player.height))

    # --- 광물 그리기 ---
    if current_map == "광산":
        for m in minerals:
            pygame.draw.rect(screen, m.color, m.rect)
            max_hp = mineral_hps[m.name]
            hp_ratio = m.hp / max_hp
            if hp_ratio >= 0.7: bar_color = (0, 200, 0)
            elif hp_ratio >= 0.3: bar_color = (255, 215, 0)
            else: bar_color = (200, 0, 0)
            bar_width = m.rect.width
            bar_height = 4
            bar_x = m.rect.x
            bar_y = m.rect.y - bar_height - 2
            pygame.draw.rect(screen, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, bar_color, (bar_x, bar_y, bar_width * hp_ratio, bar_height))

    elif current_map == "마을":
        pygame.draw.rect(screen, ORANGE, shop_rect)
        pygame.draw.rect(screen, BROWN, forge_rect)
        screen.blit(font.render("상점", True, BLACK), font.render("상점", True, BLACK).get_rect(center=shop_rect.center))
        screen.blit(font.render("대장간", True, WHITE), font.render("대장간", True, WHITE).get_rect(center=forge_rect.center))

    # --- 플레이어 ---
    pygame.draw.rect(screen, RED, player)

    # --- 현재 맵 출력 ---
    map_name_text = font.render(f"현재 위치: {current_map}", True, WHITE)
    screen.blit(map_name_text, map_name_text.get_rect(center=(400, 30)))

    # --- 골드 출력 ---
    gold_text = small_font.render(f"골드: {gold}", True, WHITE)
    screen.blit(gold_text, (10, 570))

    # --- 인벤토리 UI ---
    if inventory_open:
        pygame.draw.rect(screen, (30, 30, 30), inventory_rect)
        pygame.draw.rect(screen, WHITE, inventory_rect, 2)
        pygame.draw.rect(screen, (100, 0, 0), close_button)
        close_text = font.render("X", True, WHITE)
        screen.blit(close_text, close_text.get_rect(center=close_button.center))
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
                label = small_font.render(f"{name} {count}개", True, WHITE)
                screen.blit(label, label.get_rect(center=(slot_x + 20, slot_y + 50)))
                index += 1

    # --- 상점 UI ---
    if shop_open:
        pygame.draw.rect(screen, (20, 20, 60), shop_window)
        pygame.draw.rect(screen, WHITE, shop_window, 2)
        pygame.draw.rect(screen, (100, 0, 0), shop_close_button)
        screen.blit(font.render("X", True, WHITE), font.render("X", True, WHITE).get_rect(center=shop_close_button.center))

        for i, name in enumerate(mineral_names):
            base_y = shop_window.y + 60 + i * 60
            screen.blit(font.render(name, True, WHITE), (shop_window.x + 20, base_y))
            screen.blit(small_font.render(f"판매가: {mineral_prices[name]}골드", True, WHITE), (shop_window.x + 120, base_y))
            screen.blit(small_font.render(f"선택: {sell_selection[name]}", True, WHITE), (shop_window.x + 200, base_y + 20))

            pygame.draw.rect(screen, GRAY, (shop_window.x + 300, base_y, 30, 30))
            screen.blit(font.render("+", True, BLACK), (shop_window.x + 308, base_y))

            pygame.draw.rect(screen, GRAY, (shop_window.x + 340, base_y, 30, 30))
            screen.blit(font.render("-", True, BLACK), (shop_window.x + 348, base_y - 2))

            pygame.draw.rect(screen, GRAY, (shop_window.x + 380, base_y, 50, 30))
            screen.blit(small_font.render("최대", True, BLACK), (shop_window.x + 385, base_y + 5))

            pygame.draw.rect(screen, YELLOW, (shop_window.x + 440, base_y, 50, 30))
            screen.blit(small_font.render("판매", True, BLACK), (shop_window.x + 448, base_y + 5))

    # --- 지도 선택 창 ---
    if map_select_open:
        pygame.draw.rect(screen, (50, 50, 80), map_rect)
        pygame.draw.rect(screen, WHITE, map_rect, 2)
        pygame.draw.rect(screen, (100, 0, 0), map_close_button)
        close_text = font.render("X", True, WHITE)
        screen.blit(close_text, close_text.get_rect(center=map_close_button.center))
        pygame.draw.rect(screen, GRAY_ROCK, mine_button)
        pygame.draw.rect(screen, YELLOW, village_button)
        screen.blit(font.render("광산", True, BLACK), font.render("광산", True, BLACK).get_rect(center=mine_button.center))
        screen.blit(font.render("마을", True, BLACK), font.render("마을", True, BLACK).get_rect(center=village_button.center))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
