import unittest
from palaestrai_random.continuous_environment import (
    ContinuousRandomEnvironment,
)


class ContinuousRandomEnvironmentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.env = ContinuousRandomEnvironment(
            None, 0, 123, **{"num_sensors": 10, "max_value": 10, "max_iter": 10}
        )
        self.env.start_environment()

    def test_sensors_actuators(self):
        # the length of actuators should be the same as the specified
        # num_sensors (10)
        self.assertEqual(
            len(self.env.sensors),
            len(self.env.actuators),
            "Length of sensors and actuators did not match",
        )
        self.assertEqual(
            len(self.env.sensors), 10, "Unexpected length of sensors"
        )
        # no value in sensors or actuators should be greater than the
        # specified max_value (10)
        self.assertFalse(
            False in map(lambda x: [0] <= x() <= [10], self.env.sensors),
            "Value out of range for sensor",
        )
        self.assertFalse(
            False in map(lambda x: [0] <= x.value <= [10], self.env.actuators),
            "Value out of range for actuator",
        )

    def test_reward(self):
        """Test the reward.

        The reward is defined as:
        max_value (10) - avg_discrepancy (0,1,2 respectively),
        so the resulting reward should be max_value, max_value-1,
        max_value-2, respectively.
        """
        actuators = self.env.actuators
        for i in range(len(self.env.sensors)):
            actuators[i].value = [round(self.env.sensors[i].value)]
        self.assertEqual(
            10.0 - 0, self.env.update(actuators).rewards[0](), "unexpected reward"
        )

        for i in range(len(self.env.sensors)):
            actuators[i].value = [round(self.env.sensors[i].value) + (1 if round(self.env.sensors[i].value) < 10 else -1)]
        self.assertEqual(
            10.0 - 1, self.env.update(actuators).rewards[0](), "unexpected reward"
        )

        for i in range(len(self.env.sensors)):
            actuators[i].value = [round(self.env.sensors[i].value) + (2 if round(self.env.sensors[i].value) < 9 else -2)]
        self.assertEqual(
            10.0 - 2, self.env.update(actuators).rewards[0](), "unexpected reward"
        )

    def test_iteration(self):
        # The environment should terminate after the specified max_iter
        # (10) but not before
        for _ in range(10):
            state = self.env.update(self.env.actuators)
            self.assertNotEqual(
                (list(), 5.1, False),
                (state.sensor_information, state.rewards[0](), state.done),
                "Environment terminated unexpectedly",
            )
        state = self.env.update(self.env.actuators)
        self.assertEqual(
            (list(), 5.1, True),
            (state.sensor_information, state.rewards[0](), state.done),
            "Environment did not terminate on time",
        )


if __name__ == "__main__":
    unittest.main()
