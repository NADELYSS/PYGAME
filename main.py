import pygame
from settings import *
from mineral import Mineral, create_mineral, mineral_names, mineral_hps, mineral_prices
from player import Player
from ui_inventory import draw_inventory
from ui_map import draw_map_selection
from ui_shop import draw_shop

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("광산의 노동자")
clock = pygame.time.Clock()
font = pygame.font.Font(FONT_PATH, 24)
small_font = pygame.font.Font(FONT_PATH, 16)

# 상태
current_map = "광산"
map_select_open = False
inventory_open = False
shop_open = False
gold = 0
sell_selection = {name: 0 for name in mineral_names}

# UI 위치
inventory_rect = pygame.Rect(250, 150, 300, 200)
close_button = pygame.Rect(inventory_rect.right - 40, inventory_rect.top + 10, 20, 20)
map_rect = pygame.Rect(200, 120, 400, 300)
map_close_button = pygame.Rect(map_rect.right - 40, map_rect.top + 10, 20, 20)
mine_button = pygame.Rect(map_rect.x + 50, map_rect.y + 100, 120, 80)
village_button = pygame.Rect(map_rect.x + 230, map_rect.y + 100, 120, 80)
shop_rect = pygame.Rect(200, 200, 150, 100)
forge_rect = pygame.Rect(450, 200, 150, 100)
shop_window = pygame.Rect(150, 100, 500, 300)
shop_close_button = pygame.Rect(shop_window.right - 40, shop_window.top + 10, 20, 20)

# 이미지 로드
tool_img = pygame.image.load(ASSET_PATH).convert_alpha()
mineral_icons = {
    "돌": tool_img.subsurface(pygame.Rect(16, 0, 16, 16)),
    "철": tool_img.subsurface(pygame.Rect(16, 16, 16, 16)),
}
mineral_ground_icons = {
    "돌": tool_img.subsurface(pygame.Rect(0, 0, 16, 16)),
    "철": tool_img.subsurface(pygame.Rect(0, 16, 16, 16)),
}

# 객체 생성
player = Player(100, 100)
inventory = {name: [] for name in mineral_names}
minerals = []
for _ in range(10): create_mineral(player.rect, minerals)

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 2000)

# 게임 루프
running = True
while running:
    screen.fill(GRAY)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_EVENT and current_map == "광산":
            create_mineral(player.rect, minerals)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                inventory_open = not inventory_open
            elif event.key == pygame.K_m:
                map_select_open = not map_select_open
            elif event.key == pygame.K_SPACE:
                if current_map == "광산":
                    player.try_mine(current_map, minerals, inventory)
                elif current_map == "마을" and player.rect.colliderect(shop_rect):
                    shop_open = True
                    sell_selection = {name: 0 for name in mineral_names}
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
                        total = sum(inventory[name])
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

    player.update(keys)

    if current_map == "광산":
        for m in minerals:
            icon = pygame.transform.scale(mineral_ground_icons[m.name], (30, 30))
            screen.blit(icon, m.rect.topleft)
            ratio = m.hp / mineral_hps[m.name]
            color = (0, 200, 0) if ratio > 0.7 else (255, 215, 0) if ratio > 0.3 else (200, 0, 0)
            pygame.draw.rect(screen, (80, 80, 80), (m.rect.x, m.rect.y - 6, m.rect.width, 4))
            pygame.draw.rect(screen, color, (m.rect.x, m.rect.y - 6, m.rect.width * ratio, 4))

    elif current_map == "마을":
        pygame.draw.rect(screen, ORANGE, shop_rect)
        pygame.draw.rect(screen, BROWN, forge_rect)
        screen.blit(font.render("상점", True, BLACK), font.render("상점", True, BLACK).get_rect(center=shop_rect.center))
        screen.blit(font.render("대장간", True, WHITE), font.render("대장간", True, WHITE).get_rect(center=forge_rect.center))

    player.draw(screen)

    if inventory_open:
        draw_inventory(screen, font, small_font, inventory, inventory_rect, close_button, mineral_icons)
    if map_select_open:
        draw_map_selection(screen, font, map_rect, map_close_button, mine_button, village_button)
    if shop_open:
        draw_shop(screen, font, small_font, shop_window, shop_close_button, sell_selection, inventory, mineral_names, mineral_prices, mineral_icons)

    screen.blit(font.render(f"현재 위치: {current_map}", True, WHITE), (300, 30))
    screen.blit(small_font.render(f"골드: {gold}", True, WHITE), (10, SCREEN_HEIGHT - 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
