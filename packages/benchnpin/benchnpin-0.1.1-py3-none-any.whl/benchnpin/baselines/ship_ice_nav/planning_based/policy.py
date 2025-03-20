import benchnpin.environments
import gymnasium as gym
from benchnpin.baselines.ship_ice_nav.planning_based.planners.lattice import LatticePlanner
from benchnpin.baselines.ship_ice_nav.planning_based.planners.predictive import PredictivePlanner
from benchnpin.baselines.base_class import BasePolicy
from benchnpin.common.metrics.ship_ice_metric import ShipIceMetric
from benchnpin.common.controller.dp import DP
from typing import List, Tuple
import numpy as np


class PlanningBasedPolicy(BasePolicy):
    """
    A baseline policy for autonomous ship navigation in ice-covered waters. 
    This policy first plans a path using a ship planner and outputs actions to track the planned path.
    """

    def __init__(self, planner_type, cfg=None) -> None:
        super().__init__()

        if planner_type not in ['predictive', 'lattice']:
            raise Exception("Invalid planner type. Choose a planner between 'lattice' or 'predictive'.")
        self.planner_type = planner_type

        self.lattice_planner = LatticePlanner()
        self.predictive_planner = PredictivePlanner()
        self.path = None

        self.cfg = cfg

    
    def plan_path(self, ship_pos, goal, observation, conc, obstacles=None):
        if self.planner_type == 'lattice':
            self.path = self.lattice_planner.plan(ship_pos=ship_pos, goal=goal, obs=obstacles)

        elif self.planner_type == 'predictive':
            occ_map = observation[0]
            footprint = observation[1]
            self.path = self.predictive_planner.plan(ship_pos=ship_pos, goal=goal, occ_map=occ_map, footprint=footprint, conc=conc)


    def act(self, observation, **kwargs):

        # parameters for planners
        ship_pos = kwargs.get('ship_pos', [0, 0, np.pi / 2])
        obstacles = kwargs.get('obstacles', None)
        goal = kwargs.get('goal', None)
        conc = kwargs.get('conc', None)
        action_scale = kwargs.get('action_scale', None)
        
        # plan a path
        if self.path is None:
            self.plan_path(ship_pos, goal, observation, conc, obstacles)

            # setup dp controller to track the planned path
            cx = self.path.T[0]
            cy = self.path.T[1]
            ch = self.path.T[2]
            self.dp = DP(x=ship_pos[0], y=ship_pos[1], yaw=ship_pos[2],
                    cx=cx, cy=cy, ch=ch, **self.lattice_planner.cfg.controller)
            self.dp_state = self.dp.state
        
        # call ideal controller to get angular velocity control
        omega, _ = self.dp.ideal_control(ship_pos[0], ship_pos[1], ship_pos[2])

        # update setpoint
        x_s, y_s, h_s = self.dp.get_setpoint()
        self.dp.setpoint = np.asarray([x_s, y_s, np.unwrap([self.dp_state.yaw, h_s])[1]])

        return omega / action_scale


    def evaluate(self, num_eps: int, model_eps: str ='latest') -> Tuple[List[float], List[float], List[float], str]:
        env = gym.make('ship-ice-v0', cfg=self.cfg)
        env = env.unwrapped

        if self.planner_type == 'lattice':
            alg_name = "Lattice Planning"
        elif self.planner_type == 'predictive':
            alg_name = "Predictive Planning"
        metric = ShipIceMetric(alg_name=alg_name, ship_mass=env.cfg.ship.mass, goal=env.goal)

        for eps_idx in range(num_eps):
            print("Planning Based Progress: ", eps_idx, " / ", num_eps, " episodes")
            observation, info = env.reset()
            metric.reset(info)
            obstacles = info['obs']
            done = truncated = False

            while True:
                action = self.act(observation=(observation / 255).astype(np.float64), ship_pos=info['state'], obstacles=obstacles, 
                                    goal=env.goal,
                                    conc=env.cfg.concentration, 
                                    action_scale=env.max_yaw_rate_step)
                observation, reward, done, truncated, info = env.step(action)
                metric.update(info=info, reward=reward, eps_complete=(done or truncated))
                obstacles = info['obs']
                if done or truncated:
                    break

        env.close()
        metric.plot_scores(save_fig_dir=env.cfg.output_dir)
        return metric.efficiency_scores, metric.effort_scores, metric.rewards, alg_name

    
    def reset(self):
        self.path = None
