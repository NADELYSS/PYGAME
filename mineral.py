import pygame
import random

# 🪨 광물 클래스
class Mineral:
    def __init__(self, name, rect, hp):
        self.name = name      # 이름 ("돌", "철" 등)
        self.rect = rect      # 위치와 크기 (pygame.Rect)
        self.hp = hp          # 체력

# 광물 기본 속성
mineral_names = ["돌", "철"]
mineral_hps = {"돌": 1, "철": 2}
mineral_prices = {"돌": 1, "철": 2}
mineral_weights = [80, 20]  # 생성 확률: 돌 80%, 철 20%

# 🎯 광물 생성 함수
def create_mineral(player_rect, minerals):
    if len(minerals) >= 20:
        return  # ✅ 맵에 광물이 20개 이상이면 리젠 중지
    for _ in range(5):
        name = random.choices(mineral_names, weights=mineral_weights)[0]
        hp = mineral_hps[name]
        x = random.randint(0, 770)
        y = random.randint(0, 570)
        new_rect = pygame.Rect(x, y, 30, 30)

        # 플레이어 또는 기존 광물과 겹치지 않도록
        if player_rect.colliderect(new_rect): continue
        if any(m.rect.colliderect(new_rect) for m in minerals): continue

        # 생성
        minerals.append(Mineral(name, new_rect, hp))
        break
