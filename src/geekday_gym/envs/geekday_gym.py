import os, subprocess, time, signal
import gym
from gym import error, spaces
from gym import utils
from gym.utils import seeding
import numpy as np

import logging
logger = logging.getLogger(__name__)

class GeekdayGym(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # Init stuff here
        print('Initializing OpenAI GeekDay gym...')
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0]), np.array([10, 10, 10, 10, 10]), dtype=np.int)

    def step(self, action):
        print('Calculating the next action...')

    def reset(self):
        print('Reseting game...')

    def render(self, mode='human'):
        print('Rendering the current frame...')

    def close(self):
        print('Closing...')