import pygame
import numpy as np

colour = 51,25,0

class Obstacle:
    def __init__(self, x, size, GroundHeight):
        self.x = x
        self.size = size
        self.GroundHeight = GroundHeight
        self.collided = False  # Avoid multiple collisions with the same object
        self.passed = False

    def draw(self, gameDisplay):
        pygame.draw.rect(gameDisplay, colour, [self.x, self.GroundHeight - self.size, self.size, self.size])

    def update(self, deltaTime, velocity):
        self.x -= velocity * deltaTime

    def checkOver(self):
        return self.x < 0

    def reset(self, x, size, GroundHeight):
        self.x = x
        self.size = size
        self.GroundHeight = GroundHeight
        self.collided = False
        self.passed = False

class ObstaclePool:
    def __init__(self, initial_size, width, GROUND_HEIGHT, MINGAP, MAXGAP, VELOCITY, game_display=None):
        lastObstacle = width
        lastObstacle += MINGAP + (MAXGAP - MINGAP) * np.random.uniform(0, 1)
        self.pool = [Obstacle(lastObstacle, 50 * np.random.normal(loc=0.75, scale=0.5), GROUND_HEIGHT) for _ in range(initial_size)]
        self.game_display = game_display
        self.active = []
        self.lastObstacle = lastObstacle
        self.VELOCITY = VELOCITY
        self.GROUND_HEIGHT = GROUND_HEIGHT
        self.MINGAP = MINGAP
        self.MAXGAP = MAXGAP

    def get_obstacle(self):
        if self.pool:
            obs = self.pool.pop(0)
        else:
            return Obstacle(random.randint(600, 800), 50, self.GROUND_HEIGHT)
        self.active.append(obs)
        return obs

    def reset_obstacle(self, obs, deltaTime):
        self.lastObstacle += self.lastObstacle - self.VELOCITY * deltaTime
        new_size = 50 * np.random.normal(loc=0.5, scale=0.1)  # Adjust the new size as needed
        new_last_obstacle = self.MINGAP + (self.MAXGAP - self.MINGAP) * np.random.uniform(0.4, 1)
        obs.reset(new_last_obstacle, new_size, self.GROUND_HEIGHT)
        obs.collided = False
        obs.passed = False
        self.active.remove(obs)
        self.pool.append(obs)
