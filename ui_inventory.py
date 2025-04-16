# ui_inventory.py
# 📦 인벤토리 UI를 그려주는 함수 모듈

import pygame
from settings import WHITE

def draw_inventory(screen, font, small_font, inventory, inventory_rect, close_button, mineral_icons):
    # 인벤토리 배경 및 외곽선
    pygame.draw.rect(screen, (30, 30, 30), inventory_rect)
    pygame.draw.rect(screen, WHITE, inventory_rect, 2)

    # 닫기 버튼
    pygame.draw.rect(screen, (100, 0, 0), close_button)
    close_text = font.render("X", True, WHITE)
    screen.blit(close_text, close_text.get_rect(center=close_button.center))

    # 슬롯 UI 구성
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

            # 슬롯 배경
            pygame.draw.rect(screen, (30, 30, 30), (slot_x, slot_y, slot_size, slot_size))

            # 아이템 아이콘 (부서진 상태 아이콘 사용)
            icon = pygame.transform.scale(mineral_icons[name], (32, 32))
            screen.blit(icon, (slot_x + 4, slot_y + 4))

            # 아이템 수량 텍스트
            label = small_font.render(f"{name} {count}개", True, WHITE)
            screen.blit(label, label.get_rect(center=(slot_x + 20, slot_y + 50)))
            index += 1
