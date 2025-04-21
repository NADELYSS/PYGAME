import pygame

# UI 영역
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