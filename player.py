# player.py
import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.image.fill((0, 0, 0, 0))
        pygame.draw.polygon(self.image, "white", self.get_triangle_points(), 2)

    def get_triangle_points(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(1, 0).rotate(self.rotation) * self.radius / 1.5
        a = pygame.Vector2(self.radius, self.radius) + forward * self.radius
        b = pygame.Vector2(self.radius, self.radius) - forward * self.radius - right
        c = pygame.Vector2(self.radius, self.radius) - forward * self.radius + right

        return [a, b, c]

    def draw(self, screen):
        super().draw(screen)

    def rotate(self, dt):
        self.rotation += dt * PLAYER_TURN_SPEED
        self.rotation %= 360
        self.image.fill((0, 0, 0, 0))
        pygame.draw.polygon(self.image, "white", self.get_triangle_points(), 2)

    def move(self, dt):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.shoot_timer <= 0:
            shot = Shot(self.position.x, self.position.y)
            direction = pygame.Vector2(0, -1).rotate(self.rotation)
            shot.velocity = direction * PLAYER_SHOOT_SPEED
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        self.shoot_timer -= dt

        super().update(dt)