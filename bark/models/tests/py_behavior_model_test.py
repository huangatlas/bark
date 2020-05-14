# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import unittest
import os
import numpy as np
from bark.runtime.scenario.scenario_generation.deterministic \
  import DeterministicScenarioGeneration
from bark.runtime.scenario.scenario_generation.scenario_generation \
  import ScenarioGeneration
from bark.pybark.core.world.goal_definition import GoalDefinition, GoalDefinitionPolygon
from bark.pybark.core.geometry import *
from bark.pybark.core.world import World
from bark.runtime.commons.parameters import ParameterServer
from bark.runtime.runtime import Runtime
from bark.runtime.viewer.matplotlib_viewer import MPViewer
from bark.pybark.core.models.behavior import BehaviorModel, DynamicBehaviorModel
from bark.pybark.core.models.dynamic import SingleTrackModel


class PythonBehaviorModelWrapper(BehaviorModel):
  """Dummy Python behavior model
  """
  def __init__(self,
               dynamic_model = None,
               params = None):
    # DynamicBehaviorModel.__init__(self, dynamic_model, params)
    BehaviorModel.__init__(self, params)
    self._dynamic_model = dynamic_model
    self._params = params

  def Plan(self, delta_time, world):
    super(PythonBehaviorModelWrapper, self).SetLastAction(
      np.array([2., 1.], dtype=np.float32))
    # print(super(PythonBehaviorModelWrapper, self).GetLastAction())
    trajectory = np.array([[0., 0., 0., 0., 0.],
                           [0., 0., 0., 0., 0.]], dtype=np.float32)
    super(PythonBehaviorModelWrapper, self).SetLastTrajectory(trajectory)
    return trajectory

  def Clone(self):
    return self


class PythonBehaviorModelWrapperInheritance(BehaviorModel):
  """Dummy Python behavior model
  """
  def __init__(self,
               dynamic_model = None,
               params = None):
    BehaviorModel.__init__(
      self, params)
    self._dynamic_behavior_model = DynamicBehaviorModel(dynamic_model, params)
  
  def Plan(self, delta_time, world):
    self._dynamic_behavior_model.SetLastAction(
      np.array([2., 1.], dtype=np.float32))
    trajectory = self._dynamic_behavior_model.Plan(delta_time, world)
    super(PythonBehaviorModelWrapperInheritance, self).SetLastTrajectory(trajectory)
    return trajectory

  def Clone(self):
    return self


class PyBehaviorModelTests(unittest.TestCase):
  def test_python_model(self):
    param_server = ParameterServer(
      filename="modules/runtime/tests/data/deterministic_scenario.json")
    scenario_generation = DeterministicScenarioGeneration(num_scenarios=3,
                                                          random_seed=0,
                                                          params=param_server)
    viewer = MPViewer(params=param_server,
                      follow_agent_id=False,
                      use_world_bounds=True)
    scenario, idx = scenario_generation.get_next_scenario()
    world = scenario.get_world_state()
    single_track_model = SingleTrackModel(param_server)
    behavior_model = PythonBehaviorModelWrapper(
      single_track_model, param_server)
    world.GetAgent(0).behavior_model = behavior_model
    world.GetAgent(0).behavior_model.SetLastAction(
      np.array([1., 1.], dtype=np.float32))
    world.Step(0.2)

  def test_python_model_inheritance(self):
    param_server = ParameterServer(
      filename="modules/runtime/tests/data/deterministic_scenario.json")
    scenario_generation = DeterministicScenarioGeneration(num_scenarios=3,
                                                          random_seed=0,
                                                          params=param_server)
    viewer = MPViewer(params=param_server,
                      follow_agent_id=False,
                      use_world_bounds=True)
    scenario, idx = scenario_generation.get_next_scenario()
    world = scenario.get_world_state()
    single_track_model = SingleTrackModel(param_server)

    behavior_model = PythonBehaviorModelWrapperInheritance(
      single_track_model, param_server)
    
    world.GetAgent(0).behavior_model = behavior_model
    world.GetAgent(0).behavior_model.SetLastAction(
      np.array([1., 1.], dtype=np.float32))
    world.Step(0.2)


if __name__ == '__main__':
  unittest.main()