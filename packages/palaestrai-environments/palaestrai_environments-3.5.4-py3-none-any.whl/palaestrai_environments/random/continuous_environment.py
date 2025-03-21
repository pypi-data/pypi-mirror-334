"""This module contains a dummy environment that can be used for
reference purposes.
"""
import logging

from palaestrai.agent.actuator_information import ActuatorInformation
from palaestrai.agent.reward_information import RewardInformation
from palaestrai.agent.sensor_information import SensorInformation
from palaestrai.environment.environment import Environment
from palaestrai.environment.environment_baseline import EnvironmentBaseline
from palaestrai.environment.environment_state import EnvironmentState
from palaestrai.types import Box
from palaestrai.types.simtime import SimTime
from palaestrai.util import seeding

LOG = logging.getLogger(__name__)


class ContinuousRandomEnvironment(Environment):
    """
    The continuous dummy environment.
    The goal is to set the actuators to the closest integer of the
    corresponding sensor values

    """

    def __init__(
        self,
        uid: str,
        broker_uri: str,
        seed: int,
        max_iter: int = 5,
        num_sensors: int = 10,
        max_value: float = 10.0,
    ):
        super().__init__(uid, broker_uri, seed)
        self.rng = seeding.np_random(seed)[0]
        self.iter = 0
        self.max_iter = max_iter
        self.num_sensors = num_sensors
        self.max_value = max_value
        self.reward_space = Box(0, self.max_value, ())

    def start_environment(self):
        """Function to start the environment

        The function sets the random sensors and for each sensor one
        actuator.

        Returns
        -------
        tuple
            A *tuple* of two lists, one containing SensorInformation
            and the second containing ActuatorInformation.

        """
        self.iter = 0
        self._set_random_sensors()
        for num in range(self.num_sensors):
            self.actuators.append(
                ActuatorInformation(
                    value=0,
                    space=Box(0, self.max_value, shape=()),
                    uid="Actuator-" + str(num),
                )
            )
        LOG.info(
            "ContinousEnvironment (id=0x%x, uid=%s) starting...",
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

        This method creates new sensor readings. The actuator values
        are ignored because the values are random.

        Parameters
        ----------
        actuators : list[actuator]
            List of actuators, currently not used

        Returns
        -------
        Tuple[List[SensorInformation], List[RewardInformation], bool]
            List of SensorInformation with new random values, list of rewards,
            and done-flag

        """
        LOG.debug(
            "ContinuousEnvironment (id=0x%x, uid=%s) updating (%d/%d)...",
            id(self),
            self.uid,
            self.iter + 1,
            self.max_iter,
        )
        self.actuators = actuators
        self.iter += 1
        reward = self._calc_reward(actuators)
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
        """This function creates a random value for each sensor."""
        self.sensors = [
            SensorInformation(
                value=self.rng.uniform() * self.max_value,
                space=Box(0, self.max_value, shape=()),
                uid="Sensor-" + str(num),
            )
            for num in range(self.num_sensors)
        ]

    def _calc_reward(self, actuators):
        reward = (
            self.max_value
            - sum(
                [
                    abs(round(sens.value) - act.value)
                    for sens, act in zip(self.sensors, actuators)
                ]
            )
            / self.num_sensors
        )
        return RewardInformation(reward, self.reward_space, "Reward")
