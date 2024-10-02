from __future__ import annotations

import pygame

from minigrid.core.constants import COLOR_NAMES  # type: ignore
from minigrid.core.grid import Grid  # type: ignore
from minigrid.core.mission import MissionSpace  # type: ignore
from minigrid.core.world_object import Goal, Wall  # type: ignore
from minigrid.manual_control import ManualControl  # type: ignore
from minigrid.minigrid_env import MiniGridEnv  # type: ignore

from DFSMaze import MazeGenerator


# taken from https://minigrid.farama.org/
class SimpleEnv(MiniGridEnv):
    def __init__(
        self,
        size=10,
        # agent_start_pos=(1, 1),
        agent_start_pos=None,
        agent_start_dir=0,
        max_steps: int | None = None,
        **kwargs,
    ):
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir

        mission_space = MissionSpace(mission_func=self._gen_mission)

        generator = MazeGenerator()
        self.maze = generator.generate_maze()

        if max_steps is None:
            max_steps = 4 * size**2

        super().__init__(
            mission_space=mission_space,
            grid_size=size,
            # Set this to True for maximum speed
            see_through_walls=True,
            max_steps=max_steps,
            **kwargs,
        )

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = self.grid or Grid(width, height)

        # Generate the maze from the static layout
        for i in range(10):
            for j in range(10):
                if self.maze[i][j] == 1:
                    self.grid.set(j, i, Wall())  # Set wall
                elif self.maze[i][j] == 2:
                    self.agent_start_pos = (j, i)  # Set agent's start position
                elif self.maze[i][j] == 3:
                    self.grid.set(j, i, Goal())  # Sub-goal
                elif self.maze[i][j] == 4:
                    self.grid.set(j, i, Goal())  # End goal

        # Set agent position
        if self.agent_start_pos:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = 0  # Default agent direction

    @staticmethod
    def _gen_mission():
        return "Reach sub-goal and then end-goal"

    # def _gen_grid(self, width, height):
    #     # Create an empty grid
    #     self.grid = Grid(width, height)

    #     # Generate the surrounding walls
    #     #self.grid.wall_rect(0, 0, width, height)

    #     #generate visuals from grid
    #     print(self.maze)
    #     for i in range(0,10):
    #         for t in range(0,10):
    #             if self.maze[i][t] == 1:
    #                 self.grid.set(t, i, Wall())
                                    
        # Generate vertical separation wall
        # for i in range(0, height):
        #     self.grid.set(5, i, Wall())


def main():
    pygame.init()
    env = SimpleEnv(render_mode="human")

    # enable manual control for testing
    manual_control = ManualControl(env, seed=42)
    manual_control.start()

    
if __name__ == "__main__":
    main()
