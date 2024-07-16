import pygame

CACAOWIDTH = 78
CACAOHEIGHT = 100

class Peanut:
    def __init__(self, surfaceHeight):
        pygame.sprite.Sprite.__init__(self)
        self.x = 800
        self.y = 0
        self.yvelocity = 0
        self.height = CACAOHEIGHT
        self.width = CACAOWIDTH
        self.surfaceHeight = surfaceHeight

        # Load sprite
        original_image = pygame.image.load('/Users/pablo/Desktop/Scripts/LearnGames/Sprites/cacahuete.png').convert_alpha()
        self.image = pygame.transform.scale(original_image, (CACAOWIDTH, CACAOHEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.surfaceHeight - self.y - self.height

    def update(self, timer, velocity):
        self.x -= velocity * timer
        self.rect.x = self.x

    def draw(self, display):
        display.blit(self.image, (self.x, self.surfaceHeight - self.y - self.height, self.width, self.height))
