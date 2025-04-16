# ui_shop.py
# 🛍️ 상점 UI를 그리는 모듈 (플레이어가 shop_rect 근처에서 스페이스 누르면 열림)

import pygame
from settings import WHITE, YELLOW, GRAY, BLACK

def draw_shop(screen, font, small_font, shop_window, shop_close_button, sell_selection, inventory, mineral_names, mineral_prices, mineral_icons):
    # 상점 배경
    pygame.draw.rect(screen, (20, 20, 60), shop_window)
    pygame.draw.rect(screen, WHITE, shop_window, 2)

    # 닫기 버튼
    pygame.draw.rect(screen, (100, 0, 0), shop_close_button)
    screen.blit(font.render("X", True, WHITE), font.render("X", True, WHITE).get_rect(center=shop_close_button.center))

    for i, name in enumerate(mineral_names):
        base_y = shop_window.y + 60 + i * 60

        # 아이콘 표시
        icon = pygame.transform.scale(mineral_icons[name], (32, 32))
        screen.blit(icon, (shop_window.x + 20, base_y))

        # 가격 및 선택 수량
        screen.blit(small_font.render(f"판매가: {mineral_prices[name]}골드", True, WHITE), (shop_window.x + 70, base_y))
        screen.blit(small_font.render(f"선택: {sell_selection[name]}", True, WHITE), (shop_window.x + 200, base_y + 20))

        # + 버튼
        pygame.draw.rect(screen, GRAY, (shop_window.x + 300, base_y, 30, 30))
        screen.blit(font.render("+", True, BLACK), (shop_window.x + 308, base_y))

        # - 버튼
        pygame.draw.rect(screen, GRAY, (shop_window.x + 340, base_y, 30, 30))
        screen.blit(font.render("-", True, BLACK), (shop_window.x + 348, base_y - 2))

        # 최대 버튼
        pygame.draw.rect(screen, GRAY, (shop_window.x + 380, base_y, 50, 30))
        screen.blit(small_font.render("최대", True, BLACK), (shop_window.x + 385, base_y + 5))

        # 판매 버튼
        pygame.draw.rect(screen, YELLOW, (shop_window.x + 440, base_y, 50, 30))
        screen.blit(small_font.render("판매", True, BLACK), (shop_window.x + 448, base_y + 5))
