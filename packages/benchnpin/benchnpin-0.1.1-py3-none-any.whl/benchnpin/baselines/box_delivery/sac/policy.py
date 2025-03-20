from benchnpin.baselines.base_class import BasePolicy
from benchnpin.baselines.feature_extractors import ResNet18
from benchnpin.common.metrics.task_driven_metric import TaskDrivenMetric
import benchnpin.environments
import gymnasium as gym
from stable_baselines3 import SAC
from stable_baselines3.common.noise import NormalActionNoise
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.callbacks import CheckpointCallback
import os
import numpy as np


class BoxDeliverySAC(BasePolicy):

    def __init__(self, model_name='sac_model', model_path=None, cfg=None) -> None:
        super().__init__()

        if model_path is None:
            self.model_path = os.path.join(os.path.dirname(__file__), 'models/')
        else:
            self.model_path = model_path

        self.model_name = model_name
        self.model = None

        self.cfg = cfg


    def train(self, policy_kwargs=dict(features_extractor_class=ResNet18,
                                        features_extractor_kwargs=dict(features_dim=512),
                                        net_arch=[512, 256]),
            batch_size=64,
            buffer_size=15000,
            learning_starts=1000,
            learning_rate=5e-4,
            gamma=0.97,
            verbose=2,
            total_timesteps=int(2e5), 
            checkpoint_freq=10000,
            resume_training=False) -> None:

        env = gym.make('box-delivery-v0', cfg=self.cfg)
        env = env.unwrapped

        # The noise objects for SAC
        n_actions = env.action_space.shape[-1]
        action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.05 * np.ones(n_actions))

        if resume_training:
            self.model = SAC.load(os.path.join(self.model_path, self.model_name), env=env)
        else:
            self.model = SAC(
                'CnnPolicy', 
                env,
                policy_kwargs=policy_kwargs,
                learning_rate=learning_rate,
                buffer_size=buffer_size,
                learning_starts=learning_starts,
                action_noise=action_noise,
                batch_size=batch_size,
                gamma=gamma,
                train_freq=1,
                gradient_steps=1,
                verbose=verbose,
                tensorboard_log=os.path.join(self.model_path, self.model_name),
                )

        # Save a checkpoint every 1000 steps
        checkpoint_callback = CheckpointCallback(
            save_freq=checkpoint_freq,
            save_path=self.model_path,
            name_prefix=self.model_name,
            save_replay_buffer=False,
            save_vecnormalize=False,
        )

        # Train and save the agent
        self.model.learn(total_timesteps=total_timesteps, callback=checkpoint_callback)
        self.model.save(os.path.join(self.model_path, self.model_name))
        env.close()



    def evaluate(self, num_eps: int, model_eps: str ='latest'):

        if model_eps == 'latest':
            self.model = SAC.load(os.path.join(self.model_path, self.model_name))
        else:
            model_checkpoint = self.model_name + '_' + model_eps + '_steps'
            self.model = SAC.load(os.path.join(self.model_path, model_checkpoint))

        env = gym.make('box-delivery-v0', cfg=self.cfg)
        env = env.unwrapped

        metric = TaskDrivenMetric(alg_name="SAC", robot_mass=env.cfg.agent.mass)

        rewards_list = []
        for eps_idx in range(num_eps):
            print("Progress: ", eps_idx, " / ", num_eps, " episodes")
            obs, info = env.reset()
            metric.reset(info)
            done = truncated = False
            eps_reward = 0.0
            while True:
                action, _ = self.model.predict(obs)
                obs, reward, done, truncated, info = env.step(action)
                eps_reward += reward
                metric.update(info=info, reward=reward, eps_complete=(done or truncated))
                if done or truncated:
                    rewards_list.append(eps_reward)
                    break
        
        env.close()
        metric.plot_scores(save_fig_dir=env.cfg.output_dir)
        return metric.success_rates, metric.efficiency_scores, metric.effort_scores, metric.rewards, f"SAC_{self.model_name}"


    
    def act(self, observation, **kwargs):

        # parameters for planners
        model_eps = kwargs.get('model_eps', None)
        
        # load trained model for the first time
        if self.model is None:

            if model_eps is None:
                self.model = SAC.load(os.path.join(self.model_path, self.model_name))
            else:
                model_checkpoint = self.model_name + '_' + model_eps + '_steps'
                self.model = SAC.load(os.path.join(self.model_path, model_checkpoint))

        action, _ = self.model.predict(observation)
        return action
