import pygame
import random
import sys
import os
import numpy as np
import psutil
from monkey import Monkey
from obstacle import Obstacle, ObstaclePool
from peanut import Peanut

class Game:
    def __init__(self):
        self.SCORE = 0
        self.surfaceHeight = 720
        self.width = 960
        self.height = 720
        self.GROUND_HEIGHT = self.height - 100
        self.MINGAP = 400
        self.VELOCITY = 300
        self.MAXGAP = 1200
        self.bkg_image_victory = '/Users/pablo/Desktop/Scripts/LearnGames/Sprites/campello.jpeg'
        self.bkg_image = '/Users/pablo/Desktop/Scripts/LearnGames/Sprites/jungle.jpeg'
        self.initialize_game()

    def initialize_game(self):
        pygame.init()  # this ‘starts up’ pygame

        self.font = pygame.font.SysFont(None, 36)
        self.size = self.width, self.height
        self.gameDisplay = pygame.display.set_mode(self.size)  # creates screen
        pygame.display.set_caption("Monkey Game")

        if os.path.exists(self.bkg_image):
            self.backgroundImage = pygame.image.load(self.bkg_image).convert()
            self.backgroundImage = pygame.transform.scale(self.backgroundImage, self.size)
        if os.path.exists(self.bkg_image_victory):
            self.backgroundImage_exito = pygame.image.load(self.bkg_image_victory).convert()
            self.backgroundImage_exito = pygame.transform.scale(self.backgroundImage_exito, self.size)

        self.obstacle_pool = ObstaclePool(5, self.width, self.GROUND_HEIGHT, self.MINGAP, self.MAXGAP, self.VELOCITY, self.gameDisplay)
        self.obstacles = [self.obstacle_pool.get_obstacle() for _ in range(4)]  # Start with 4 obstacles

        self.Monito = Monkey(self.GROUND_HEIGHT)
        self.MariscoMono = Peanut(self.GROUND_HEIGHT)
        self.peanut_time = 6

        self.lastFrame = pygame.time.get_ticks()  # get ticks returns current time in milliseconds

        self.running = True

    def reset(self):
        self.SCORE = 0
        self.initialize_game()
        return self.get_state()

    def update(self):
        t = pygame.time.get_ticks()
        deltaTime = (t - self.lastFrame) / 1000.0
        self.lastFrame = t

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.Monito.jump()

        if os.path.exists(self.bkg_image):
            self.gameDisplay.blit(self.backgroundImage, (0, 0))
        else:
            self.gameDisplay.fill((51, 255, 255))

        self.Monito.update(deltaTime)
        self.Monito.draw(self.gameDisplay)

        for obs in self.obstacles:
            obs.update(deltaTime, self.VELOCITY)
            obs.draw(self.gameDisplay)
            if obs.checkOver():
                if t / 1000.0 < (self.peanut_time - 5):
                    self.obstacle_pool.reset_obstacle(obs, deltaTime)
                    self.obstacles.remove(obs)
                    self.obstacles.append(self.obstacle_pool.get_obstacle())

            obs_rect = pygame.Rect(obs.x, self.GROUND_HEIGHT - obs.size, obs.size, obs.size)

            if t / 1000.0 > self.peanut_time:
                self.MariscoMono.update(deltaTime, self.VELOCITY)
                self.MariscoMono.draw(self.gameDisplay)

            if (self.MariscoMono.x < -1000) or (self.Monito.rect.colliderect(self.MariscoMono.rect)):
                if not (self.Monito.rect.colliderect(self.MariscoMono.rect)):
                    self.display_victory_text(self.gameDisplay, self.font, "meh")
                    self.gameDisplay.fill((51, 255, 255))
                if (self.Monito.rect.colliderect(self.MariscoMono.rect)):
                    self.gameDisplay.blit(self.backgroundImage_exito, (0, 0))
                    self.display_victory_text(self.gameDisplay, self.font, "Victory!")
                self.Monito.mono_feliz()
                self.MariscoMono.draw(self.gameDisplay)
                self.Monito.draw(self.gameDisplay)
                waiting_for_input = True
                while waiting_for_input:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                waiting_for_input = False
                            elif event.key == pygame.K_RETURN:
                                waiting_for_input = False
                                self.running = False
                        elif event.type == pygame.QUIT:
                            waiting_for_input = False
                            self.running = False
            self.Monito.rect.y = self.GROUND_HEIGHT - self.Monito.y - 50

            if self.Monito.rect.colliderect(obs_rect) and not obs.collided:
                self.SCORE -= 5
                obs.collided = True
                print("Collision Detected! Score: ", self.SCORE)

            if not self.Monito.rect.colliderect(obs_rect) and not obs.passed:
                obs.passed = True
                self.SCORE += 1
                print("Obstacle Passed! Score: ", self.SCORE)

        pygame.draw.rect(self.gameDisplay, (102, 204, 0), [0, self.GROUND_HEIGHT, self.width, self.height - self.GROUND_HEIGHT])
        self.update_score_display()
        pygame.display.update()

    def get_state(self):
        return np.zeros((self.height, self.width, 3), dtype=np.uint8)

    def is_over(self):
        return not self.running

    def display_victory_text(self, gameDisplay, font, text):
        victory_text = font.render(text, True, (255, 255, 255), (0, 0, 0))
        text_rect = victory_text.get_rect(center=(self.width / 2, self.height / 2))
        gameDisplay.blit(victory_text, text_rect)
        pygame.display.update()

    def update_score_display(self):
        score_text = self.font.render('Score: ' + str(self.SCORE), True, (0, 0, 0))
        self.gameDisplay.blit(score_text, (10, 10))

        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent

        cpu_text = self.font.render(f'CPU Usage: {cpu_usage}%', True, pygame.Color('black'))
        memory_text = self.font.render(f'Memory Usage: {memory_usage}%', True, pygame.Color('black'))

        cpu_text_x = self.width - cpu_text.get_width() - 10
        memory_text_x = self.width - memory_text.get_width() - 10

        self.gameDisplay.blit(cpu_text, (cpu_text_x, 10))
        self.gameDisplay.blit(memory_text, (memory_text_x, 30))

if __name__ == "__main__":
    game = Game()
    while game.running:
        game.update()
    pygame.quit()
    sys.exit()
