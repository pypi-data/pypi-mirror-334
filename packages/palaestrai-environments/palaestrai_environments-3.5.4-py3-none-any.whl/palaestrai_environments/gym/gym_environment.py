"""This module contains a wrapper for the openai gym library"""
import gymnasium as gym
import palaestrai.types
import numpy as np
from palaestrai.types import Space, Box
from palaestrai.agent.actuator_information import ActuatorInformation
from palaestrai.agent.reward_information import RewardInformation
from palaestrai.agent.sensor_information import SensorInformation
from palaestrai.environment.environment import Environment
from palaestrai.environment.environment_baseline import EnvironmentBaseline
from palaestrai.environment.environment_state import EnvironmentState
from typing import Dict, List, Optional
import logging

LOG = logging.getLogger(__name__)

default_conversion = {
    gym.spaces.box.Box: (
        palaestrai.types.box.Box,
        ["low", "high", "shape", "dtype"],
    ),
    gym.spaces.discrete.Discrete: (palaestrai.types.discrete.Discrete, ["n"]),
}


def convert_space(space, conversion):
    if type(space) in conversion.keys():
        new_type = conversion[type(space)][0]
        parameters = conversion[type(space)][1]
        return new_type(
            *[
                getattr(space, parameters[i], None)
                for i in range(len(parameters))
            ]
        )
    else:
        raise Exception(
            f"Could not convert space {type(space)}, no conversion defined!"
        )


def obs_to_sensors(
    obs: List, space: gym.Space, conversion
) -> SensorInformation:
    try:
        assert space.contains(obs), "Sensor not matching space!"
    except AssertionError:
        # The last step might give out-of-bounds values
        # (e.g., in the Lunar Lander)
        obs = np.max([obs, space.low], axis=0)
        obs = np.min([obs, space.high], axis=0)
    return SensorInformation(obs, convert_space(space, conversion), "0")


def space_to_actuator(space, conversion) -> ActuatorInformation:
    # assert space.contains(obs), "Actuator not matching space!"
    return ActuatorInformation(
        space.sample(), convert_space(space, conversion), "0"
    )


class GymEnvironment(Environment):
    def __init__(
        self,
        uid,
        broker_uri,
        seed: int,
        env_name: str,
        conversion: Optional[Dict[str, str]],
        reward_space: Optional[str],
        **gym_kwargs,
    ):
        super().__init__(uid, broker_uri, seed)

        if env_name is None or env_name == "":
            raise Exception("Parameter 'env_name' must not be empty!")
        self.env_name: str = env_name

        self.conversion: Dict[
            gym.spaces.Space, palaestrai.types.Space
        ] = default_conversion
        if conversion is not None and conversion:
            self.conversion = {
                eval(key): [eval(val1), val2]
                for (key, [val1, val2]) in conversion.items()
            }

        if reward_space is not None and reward_space != "":
            self.reward_space = Space.from_string(reward_space)
            LOG.debug(f"Reward space was compiled to {self.reward_space}")
        else:
            self.reward_space = Box(float("-inf"), float("inf"), (1,), dtype=float)
            LOG.warning(
                "No 'reward_space' found in params, defaulting to Box(float('-inf'), float('inf'), (1,))"
            )
        self.kwargs = gym_kwargs
        self.env = None

    def start_environment(self) -> EnvironmentBaseline:
        if self.env is None:
            self.env = gym.make(self.env_name, **self.kwargs)

        obs, info = self.env.reset()
        LOG.info(
            "GymEnvironment (id=0x%x, uid=%s, gym=%s) starting...",
            id(self),
            self.uid,
            self.env_name,
        )
        return EnvironmentBaseline(
            sensors_available=[
                obs_to_sensors(
                    obs, self.env.observation_space, self.conversion
                )
            ],
            actuators_available=[
                space_to_actuator(self.env.action_space, self.conversion)
            ],
        )

    def update(self, actuators: List[ActuatorInformation]) -> EnvironmentState:
        obs, reward, terminated, truncated, info = self.env.step(
            [a.value for a in actuators][0]
        )  # gym can only handle one actuator
        done = terminated or truncated
        LOG.debug(
            "GymEnvironment (id=0x%x, uid=%s, gym=%s) updating! obs: %s reward: %d done: %s info: %s",
            id(self),
            self.uid,
            self.env_name,
            obs,
            reward,
            done,
            info,
        )
        return EnvironmentState(
            sensor_information=[
                obs_to_sensors(
                    obs, self.env.observation_space, self.conversion
                )
            ],
            rewards=[
                RewardInformation(np.array([reward]), self.reward_space, "gym.reward")
            ],
            done=done,
        )
