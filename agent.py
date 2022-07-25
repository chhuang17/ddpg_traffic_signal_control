# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 18:36:37 2021

@author: Home
"""

import torch
from numpy.random import normal
from network import Actor, Critic


class Agent:
    def __init__(self, chkpt_dir, alpha=1e-4, beta=3e-4, gamma=0.95, tau=1e-3):
        self.gamma = gamma
        self.tau = tau
        self.agent_name = 'ddpg_agent'
        self.actor = Actor(alpha, chkpt_dir=chkpt_dir, name=self.agent_name+'_actor.pth')
        self.critic = Critic(beta, chkpt_dir=chkpt_dir, name=self.agent_name+'_critic.pth')
        self.target_actor = Actor(alpha, chkpt_dir=chkpt_dir, name=self.agent_name+'_target_actor.pth')
        self.target_critic = Critic(beta, chkpt_dir=chkpt_dir, name=self.agent_name+'_target_critic.pth')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.update_network_parameters(tau=1)

    def choose_action(self, car_D, scooter_D, car_S, scooter_S, std):
        acts = self.actor(car_D, scooter_D, car_S, scooter_S).float()
        noise = normal(0, std, 6)
        noise = torch.from_numpy(noise).unsqueeze(0).float().to(self.device)
        actions = acts.clone() + noise
        return actions.detach()
    
    def update_network_parameters(self, tau=None):
        if tau is None:
            tau = self.tau

        target_actor_params = self.target_actor.named_parameters()
        actor_params = self.actor.named_parameters()

        target_actor_state_dict = dict(target_actor_params)
        actor_state_dict = dict(actor_params)
        for name in actor_state_dict:
            actor_state_dict[name] = tau * actor_state_dict[name].clone() + \
                                     (1 - tau) * target_actor_state_dict[name].clone()

        self.target_actor.load_state_dict(actor_state_dict)

        target_critic_params = self.target_critic.named_parameters()
        critic_params = self.critic.named_parameters()

        target_critic_state_dict = dict(target_critic_params)
        critic_state_dict = dict(critic_params)
        for name in critic_state_dict:
            critic_state_dict[name] = tau * critic_state_dict[name].clone() + \
                                      (1 - tau) * target_critic_state_dict[name].clone()

        self.target_critic.load_state_dict(critic_state_dict)

    def save_models(self):
        self.actor.save_checkpoint()
        self.target_actor.save_checkpoint()
        self.critic.save_checkpoint()
        self.target_critic.save_checkpoint()

    def load_models(self):
        self.actor.load_checkpoint()
        self.target_actor.load_checkpoint()
        self.critic.load_checkpoint()
        self.target_critic.load_checkpoint()
