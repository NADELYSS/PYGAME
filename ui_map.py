# ui_map.py
# 🗺️ M 키를 눌렀을 때 뜨는 맵 선택 창 UI를 그리는 함수 모듈

import pygame
from settings import WHITE, GRAY_ROCK, YELLOW, BLACK

def draw_map_selection(screen, font, map_rect, map_close_button, mine_button, village_button):
    # 배경 및 외곽선
    pygame.draw.rect(screen, (50, 50, 80), map_rect)
    pygame.draw.rect(screen, WHITE, map_rect, 2)

    # 닫기 버튼
    pygame.draw.rect(screen, (100, 0, 0), map_close_button)
    close_text = font.render("X", True, WHITE)
    screen.blit(close_text, close_text.get_rect(center=map_close_button.center))

    # 광산 버튼
    pygame.draw.rect(screen, GRAY_ROCK, mine_button)
    screen.blit(font.render("광산", True, BLACK), font.render("광산", True, BLACK).get_rect(center=mine_button.center))

    # 마을 버튼
    pygame.draw.rect(screen, YELLOW, village_button)
    screen.blit(font.render("마을", True, BLACK), font.render("마을", True, BLACK).get_rect(center=village_button.center))
