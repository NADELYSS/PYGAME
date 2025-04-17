import pygame

def draw_shop(screen, font, small_font, shop_window, shop_close_button, sell_selection,
              inventory, mineral_names, mineral_prices, mineral_icons):
    # 상점 창
    pygame.draw.rect(screen, (10, 10, 60), shop_window)
    pygame.draw.rect(screen, (255, 255, 255), shop_window, 2)

    # 닫기 버튼
    pygame.draw.rect(screen, (100, 0, 0), shop_close_button)
    close_text = font.render("X", True, (255, 255, 255))
    screen.blit(close_text, close_text.get_rect(center=shop_close_button.center))

    # 광물 리스트
    for i, name in enumerate(mineral_names):
        base_y = shop_window.y + 60 + i * 60

        # 아이콘
        icon = pygame.transform.scale(mineral_icons[name], (32, 32))
        screen.blit(icon, (shop_window.x + 20, base_y))

        # 판매가
        price_text = small_font.render(f"판매가: {mineral_prices[name]}골드", True, (255, 255, 255))
        screen.blit(price_text, (shop_window.x + 70, base_y))

        # 선택 수량
        selected = sell_selection[name]
        select_text = small_font.render(f"선택: {selected}", True, (255, 255, 255))
        screen.blit(select_text, (shop_window.x + 240, base_y + 6))

        # + 버튼
        pygame.draw.rect(screen, (50, 50, 50), (shop_window.x + 300, base_y, 30, 30))
        screen.blit(font.render("+", True, (255, 255, 255)), (shop_window.x + 308, base_y))

        # - 버튼
        pygame.draw.rect(screen, (50, 50, 50), (shop_window.x + 340, base_y, 30, 30))
        screen.blit(font.render("-", True, (255, 255, 255)), (shop_window.x + 348, base_y - 2))

        # 최대 버튼
        pygame.draw.rect(screen, (50, 50, 50), (shop_window.x + 380, base_y, 50, 30))
        screen.blit(small_font.render("최대", True, (255, 255, 255)), (shop_window.x + 385, base_y + 5))

        # 판매 버튼
        pygame.draw.rect(screen, (255, 255, 0), (shop_window.x + 440, base_y, 50, 30))
        screen.blit(small_font.render("판매", True, (0, 0, 0)), (shop_window.x + 448, base_y + 5))
