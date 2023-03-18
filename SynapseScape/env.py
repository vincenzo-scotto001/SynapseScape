# env.py
import abc

class Env(metaclass=abc.ABCMeta):
    """Superclass for all environments."""
    def __init__(self):
        self.action_space = None
        self.observation_space = None
        self.reward_range = None
        self.state = None

    @abc.abstractmethod
    def step(self, action):
        """Take a step in the environment."""
        pass

    @abc.abstractmethod
    def get_state(self):
        """Get the current state of the environment."""
        pass

    @abc.abstractmethod
    def set_state(self, state):
        """Set the current state of the environment."""
        pass