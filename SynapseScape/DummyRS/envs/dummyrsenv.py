import gymnasium as gym
from gymnasium import spaces
from typing import Any, Dict, Tuple
from envs import *

class OldSchoolRunescapeEnv(gym.Env):
    """
    A custom gym environment for Old School Runescape.

    Attributes:
        game_map (List[List[Tile]]): The game map consisting of tiles.
        player_pos (Tuple[int, int]): The current position of the player.
        action_space (spaces.Space): The action space of the environment.
        observation_space (spaces.Space): The observation space of the environment.
    """

    def __init__(self):
        super().__init__()
        self.world_model = WorldModel()
        self.current_map = Map()
        self.player_pos = (3, 5)  # Set initial player position

        self.action_space = spaces.Tuple((
            spaces.Discrete(3),  # Action type: 0 - move, 1 - attack, 2 - interact
            spaces.Discrete(10), # X coordinate
            spaces.Discrete(7)   # Y coordinate
        ))

        self.observation_space = spaces.Dict({
            "current_map": spaces.Box(low=0, high=1, shape=(7, 10), dtype=object), # 7x10 game map
            "player_pos": spaces.Tuple((spaces.Discrete(10), spaces.Discrete(7))) # Player position
        })

    def step(self, action: Tuple[int, int, int]) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        """
        Executes the specified action in the environment.

        Args:
            action (Tuple[int, int, int]): The action to execute.

        Returns:
            Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
                observation (Dict[str, Any]): The new observation of the environment.
                reward (float): The reward obtained for taking the action.
                done (bool): Whether the episode is finished.
                info (Dict[str, Any]): Additional information about the step.
        """
        action_type, x, y = action

        if action_type == 0:  # Move
            self.move_player(x, y)
        elif action_type == 1:  # Attack
            pass  # Implement attack logic
        elif action_type == 2:  # Interact
            pass  # Implement interact logic

        observation = self.get_observation()
        reward = 0  # Define the reward logic
        done = False  # Define the episode termination logic
        info = {}  # Provide any additional information if needed

        return observation, reward, done, info

    def reset(self) -> Dict[str, Any]:
        """
        Resets the environment to its initial state.

        Returns:
            Dict[str, Any]: The initial observation of the environment.
        """
        self.game_map = create_game_map()
        self.player_pos = (3, 5)  # Reset player position
        return self.get_observation()

    def render(self, mode: str = "human") -> None:
        """
        Renders the environment.

        Args:
            mode (str, optional): The mode to use for rendering.
        """
        # Implement the rendering logic

    def get_observation(self) -> Dict[str, Any]:
        """
        Returns the current observation of the environment.

        Returns:
            Dict[str, Any]: The current observation of the environment.
        """
        return {
            "current_map": self.current_map.tiles,
            "player_pos": self.player_pos
        }
    
    def move_player(self, x: int, y: int) -> None:
        """
        Moves the player to the specified position if the move is valid.

        Args:
            x (int): The x coordinate of the target position.
            y (int): The y coordinate of the target position.
        """
        target_tile = self.game_map[y][x]
        if not target_tile.inaccessible:
            # Update the player's position on the current tile
            current_tile = self.game_map[self.player_pos[1]][self.player_pos[0]]
            new_current_tile = Tile.new_tile_with_player(current_tile, player=False)
            self.game_map[self.player_pos[1]][self.player_pos[0]] = new_current_tile

            # Update the player's position on the target tile
            new_target_tile = Tile.new_tile_with_player(target_tile, player=True)
            self.game_map[y][x] = new_target_tile

            # Update the player's position attribute
            self.player_pos = (x, y)

    def create_game_map(width: int = 10, height: int = 7) -> List[List[Tile]]:
        """
        Creates a game map consisting of tiles in a specified configuration.

        Args:
            width (int, optional): The width of the game map. Defaults to 10.
            height (int, optional): The height of the game map. Defaults to 7.

        Returns:
            List[List[Tile]]: A 2D list of tiles representing the game map.
        """
        game_map = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(Tile(x=x, y=y))
            game_map.append(row)
        return game_map
