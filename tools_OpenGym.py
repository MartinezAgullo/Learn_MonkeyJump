import gym
from gym import spaces
import numpy as np
import random
from game import Game

class CustomGameEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(CustomGameEnv, self).__init__()
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(low=0, high=255, shape=(720, 960, 3), dtype=np.uint8)
        self.game = Game()

    def reset(self):
        return self.game.reset()

    def step(self, action):
        if action == 1:
            self.game.Monito.jump()
        self.game.update()
        reward = self.game.SCORE
        done = self.game.is_over()
        info = {}
        return self.game.get_state(), reward, done, info

    def render(self, mode='human', close=False):
        pass  # No rendering needed for headless mode

    def close(self):
        pygame.quit()

    def seed(self, seed=None):
        random.seed(seed)
        np.random.seed(seed)
