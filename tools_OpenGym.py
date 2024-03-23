import gym
from gym import spaces
import pygame

class CustomGameEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(CustomGameEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(N) # N actions
        self.observation_space = spaces.Box(low=0, high=255, shape=
                    (HEIGHT, WIDTH, CHANNELS), dtype=np.uint8) # Example for image-based game

        # Initialize your game
        # self.game = YourPygameGame()

    def step(self, action):
        # Execute one time step within the environment
        # self.game.update(action)
        # next_state, reward, done, info = self.game.get_state()
        return next_state, reward, done, info

    def reset(self):
        # Reset the state of the environment to an initial state
        # self.game.reset()
        # observation = self.game.get_initial_state()
        return observation

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        # self.game.draw()
        pass

    def close(self):
        # Cleanup any resources
        pass
