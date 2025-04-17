import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

# 🎞️ 애니메이션 strip 이미지 자르기 함수
def load_animation(path, frame_count):
    image = pygame.image.load(path).convert_alpha()
    width = image.get_width() // frame_count
    height = image.get_height()
    return [image.subsurface(pygame.Rect(i * width, 0, width, height)) for i in range(frame_count)]

# 🧍 플레이어 클래스
class Player:
    def __init__(self, x, y, size=30):
        # 사각형 충돌박스와 부드러운 위치 벡터
        self.rect = pygame.Rect(x, y, size, size)
        self.pos = pygame.Vector2(x, y)  # ✅ 실수 위치로 저장

        self.speed = 2.5  # 이동 속도
        self.facing_left = False  # 방향
        self.state = "idle"       # 상태: idle, walk, mine
        self.is_mining = False    # 채굴 중 여부

        # 🎞️ 애니메이션 프레임 등록
        self.animations = {
            "idle": load_animation("./asset/player/idle_strip3.png", 3),
            "walk": load_animation("./asset/player/walk_strip8.png", 8),
            "mine": load_animation("./asset/player/pickaxe_strip5.png", 5)
        }
        self.frame_index = 0
        self.animation_speed = 0.15

    # 🎮 이동 처리
    def update(self, keys):
        if self.is_mining:
            return

        dx = dy = 0
        # 방향키 입력 처리
        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.facing_left = True
        elif keys[pygame.K_RIGHT]:
            dx = self.speed
            self.facing_left = False
        if keys[pygame.K_UP]:
            dy = -self.speed
        elif keys[pygame.K_DOWN]:
            dy = self.speed

        # 실수 좌표에 더함
        self.pos.x += dx
        self.pos.y += dy

        # ✅ 화면 경계 제한
        self.pos.x = max(0, min(self.pos.x, SCREEN_WIDTH - self.rect.width))
        self.pos.y = max(0, min(self.pos.y, SCREEN_HEIGHT - self.rect.height))

        # 정수 좌표 반영
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # 상태 갱신
        self.state = "walk" if dx != 0 or dy != 0 else "idle"

    # ⛏ 채굴 시도
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

    # 🖼️ 플레이어 그리기
    def draw(self, screen):
        frames = self.animations[self.state]
        frame = frames[int(self.frame_index) % len(frames)]

        # 크기 및 방향 반영
        scaled_frame = pygame.transform.scale(frame, (self.rect.width, self.rect.height))
        if self.facing_left:
            scaled_frame = pygame.transform.flip(scaled_frame, True, False)

        # 화면에 그리기
        screen.blit(scaled_frame, self.rect.topleft)

        # 애니메이션 진행
        self.frame_index += self.animation_speed
        if self.state == "mine" and self.frame_index >= len(frames):
            self.state = "idle"
            self.is_mining = False
            self.frame_index = 0
