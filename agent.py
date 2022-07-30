from typing import Deque
import torch
import random
import numpy as np

from collections import deque
from Space import Game, Actions

MAX_MEMORY = 100_100
BATCH_SIZE = 1000
LEARNING_RATE = 0.001


class Agent:

    def __init__(self):
        pass

    def get_state(self, game):
        self.num_games = 0
        self.epsilon = 0  # contol randomness
        self.gamma = 0  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self):
        pass

    def get_action(self, state):
        pass


def train():
    plot_scores = []
    plot_avg_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Game()

    while True:
        # get old state
        old_state = agent.get_state(game)

        # get move
        final_move = agent.get_action(old_state)

        # perform movea and get new_state
        reward, done, score = game.play_action(final_move)
        new_state = agent.get_state(game)

        # train short memory
        agent.train_short_memory()


if __name__ == '__main__':
    train()
