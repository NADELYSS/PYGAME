import pygame

# 🎞️ 애니메이션 strip 이미지 자르기 함수
def load_animation(path, frame_count):
    image = pygame.image.load(path).convert_alpha()
    width = image.get_width() // frame_count
    height = image.get_height()
    return [image.subsurface(pygame.Rect(i * width, 0, width, height)) for i in range(frame_count)]

# 🧍 플레이어 클래스
class Player:
    def __init__(self, x, y, size=30):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = 2  # 이동 속도 절반 조정
        self.facing_left = False
        self.state = "idle"      # 상태: idle / walk / mine
        self.is_mining = False   # 채굴 중이면 True

        # 애니메이션 프레임 로딩
        self.animations = {
            "idle": load_animation("miner_game/asset/player/idle_strip3.png", 3),
            "walk": load_animation("miner_game/asset/player/walk_strip8.png", 8),
            "mine": load_animation("miner_game/asset/player/pickaxe_strip5.png", 5)
        }
        self.frame_index = 0
        self.animation_speed = 0.15

    def update(self, keys):
        if self.is_mining:
            return

        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.facing_left = True
        elif keys[pygame.K_RIGHT]:
            dx = self.speed
            self.facing_left = False
        if keys[pygame.K_UP]: dy = -self.speed
        if keys[pygame.K_DOWN]: dy = self.speed

        self.rect.x += dx
        self.rect.y += dy

        # 이동 후 화면 경계 제한
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))

        self.state = "walk" if dx != 0 or dy != 0 else "idle"

    def try_mine(self, current_map, minerals, inventory):
        if self.is_mining or current_map != "광산":
            return
        for m in minerals:
            if self.rect.colliderect(m.rect):
                self.state = "mine"
                self.is_mining = True
                self.frame_index = 0
                m.hp -= 1
                if m.hp <= 0:
                    stacks = inventory[m.name]
                    if not stacks or stacks[-1] >= 99:
                        stacks.append(1)
                    else:
                        stacks[-1] += 1
                    minerals.remove(m)
                break

    def draw(self, screen):
        frames = self.animations[self.state]
        frame = frames[int(self.frame_index) % len(frames)]
        scaled_frame = pygame.transform.scale(frame, (self.rect.width, self.rect.height))
        if self.facing_left:
            scaled_frame = pygame.transform.flip(scaled_frame, True, False)
        screen.blit(scaled_frame, self.rect.topleft)

        self.frame_index += self.animation_speed
        if self.state == "mine" and self.frame_index >= len(frames):
            self.state = "idle"
            self.is_mining = False
            self.frame_index = 0
