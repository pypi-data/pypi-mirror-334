"""This module contains a dummy environment that can be used for
reference purposes.
"""
import logging

import numpy as np

from palaestrai.agent.actuator_information import ActuatorInformation
from palaestrai.agent.reward_information import RewardInformation
from palaestrai.agent.sensor_information import SensorInformation
from palaestrai.environment.environment import Environment
from palaestrai.environment.environment_baseline import EnvironmentBaseline
from palaestrai.environment.environment_state import EnvironmentState
from palaestrai.types import Box, Discrete
from palaestrai.types.simtime import SimTime
from palaestrai.util import seeding

LOG = logging.getLogger(__name__)


class DiscreteRandomEnvironment(Environment):
    """The discrete dummy environment.

    This environment has discrete actuators and continuous sensors.

    """

    def __init__(
        self,
        uid,
        broker_uri,
        seed,
        max_iter: int = 1000,
        num_sensors: int = 10,
        max_value: int = 10,
        resolution: int = 100,
        **kwargs,
    ):
        super().__init__(uid, broker_uri, seed)
        self.rng = seeding.np_random(seed)[0]
        self.iter = 0
        self.max_iter = max_iter
        self.num_sensors = num_sensors
        self.max_value = max_value
        self.resolution = resolution
        self.reward_space = Box(0, self.resolution, ())

    def start_environment(self):
        """Function to start the environment

        The function sets the random sensors and for each sensor one
        actuator.
        """
        self.iter = 0
        self._set_random_sensors()
        self.actuators = [
            ActuatorInformation(
                value=0,
                space=Discrete(self.resolution),
                uid="Actuator-0",
            )
        ]
        LOG.info(
            "DiscreteEnvironment (id=0x%x, uid=%s) starting...",
            id(self),
            self.uid,
        )
        return EnvironmentBaseline(
            sensors_available=self.sensors,
            actuators_available=self.actuators,
            simtime=SimTime(self.iter, None),
        )

    def update(self, actuators):
        """Creates new sensor information

        This method creates new sensor readings. The actuator value
        is ignored because the values are random. Only one actuator is
        allowed

        Parameters
        ----------
        actuators : list[ActuatorInformation]
            List of actuators, in this case only one actuator is
            allowed.

        Returns
        -------
        Tuple[List[SensorInformation], List[RewardInformation], bool]
            List of SensorInformation with new random values, list of rewards,
            and done-flag

        """
        LOG.debug(
            "DiscreteEnvironment (id=0x%x, uid=%s) updating (%d/%d)...",
            id(self),
            self.uid,
            self.iter + 1,
            self.max_iter,
        )
        assert len(actuators) == 1, "Can only handle 1 actuator"
        self.iter += 1
        reward = self._calc_reward(actuators[0])
        if self.iter < self.max_iter:
            self._set_random_sensors()
            return EnvironmentState(
                sensor_information=self.sensors,
                rewards=[reward],
                done=False,
                simtime=SimTime(self.iter, None),
            )
        else:
            return EnvironmentState(
                sensor_information=[],
                rewards=[reward],
                done=True,
                simtime=SimTime(self.iter, None),
            )

    def _set_random_sensors(self):
        """creates random value for a sensor

        This function creates a random value for each sensor.
        """
        self.sensors = [
            SensorInformation(
                value=self.rng.uniform() * self.max_value,
                space=Box(0, self.max_value, ()),
                uid="Sensor-" + str(num),
            )
            for num in range(self.num_sensors)
        ]

    def _calc_reward(self, actuator):
        mean_of_sensors = float(
            sum(map(lambda x: x(), self.sensors)) / len(self.sensors)
        )
        perfect_setpoint = round(
            mean_of_sensors / (self.max_value / self.resolution)
        )
        reward = self.resolution - abs(actuator.value - perfect_setpoint)
        return RewardInformation(reward, self.reward_space, "Reward")
