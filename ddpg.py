# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 22:56:32 2021

@author: Home
"""

import torch
import torch.nn.functional as F
import numpy as np
from agent import Agent


class DDPG:
    def __init__(self, alpha=1e-4, beta=3e-4, gamma=0.95, tau=1e-3,
                 chkpt_dir='/Users/chhuang/dens_speed_offset/model/'):
        self.agent = Agent(alpha=alpha, beta=beta, gamma=gamma, tau=tau, chkpt_dir=chkpt_dir)
        self.device = self.agent.device

    def save_checkpoint(self):
        print('... saving checkpoint ...')
        self.agent.save_models()

    def load_checkpoint(self):
        print('... loading checkpoint ...')
        self.agent.load_models()

    def choose_actions(self, car_D, scooter_D, car_S, scooter_S, std):
        actions = self.agent.choose_action(car_D, scooter_D, car_S, scooter_S, std)
        splits, first_greens = torch.split(actions.clone(), 3, dim=1)
        return splits, first_greens

    def learn(self, memory):
        car_dens, scooter_dens, car_speed, scooter_speed, splits, first_greens, rewards, \
        new_car_dens, new_scooter_dens, new_car_speed, new_scooter_speed = memory.sample_buffer()

        car_D = torch.cat([dens for dens in car_dens])
        scooter_D = torch.cat([dens for dens in scooter_dens])
        car_S = torch.cat([speed for speed in car_speed])
        scooter_S = torch.cat([speed for speed in scooter_speed])
        
        car_D_ = torch.cat([dens for dens in new_car_dens])
        scooter_D_ = torch.cat([dens for dens in new_scooter_dens])
        car_S_ = torch.cat([speed for speed in new_car_speed])
        scooter_S_ = torch.cat([speed for speed in new_scooter_speed])
       
        rewards = torch.tensor(rewards, dtype=torch.float).to(self.device)

        agent_new_splits = []
        agent_new_mu_splits = []
        agent_new_first_greens = []
        agent_new_mu_first_greens = []

        new_pi = self.agent.target_actor(car_D_, scooter_D_, car_S_, scooter_S_).float()
        new_pi_split, new_pi_first_green = torch.split(new_pi.clone(), 3, dim=1)
        agent_new_splits.append(new_pi_split)
        agent_new_first_greens.append(new_pi_first_green)

        pi = self.agent.actor(car_D, scooter_D, car_S, scooter_S).float()
        pi_split, pi_first_green = torch.split(pi.clone(), 3, dim=1)
        agent_new_mu_splits.append(pi_split)
        agent_new_mu_first_greens.append(pi_first_green)

        new_splits = torch.cat([split for split in agent_new_splits], dim=1).float()
        new_first_greens = torch.cat([fg for fg in agent_new_first_greens], dim=1).float()
        
        mu_splits = torch.cat([split for split in agent_new_mu_splits], dim=1).float()
        mu_first_greens = torch.cat([fg for fg in agent_new_mu_first_greens], dim=1).float()
        
        old_splits = torch.cat([split for split in splits]).float()
        old_first_greens = torch.cat([first_green for first_green in first_greens]).float()

        c_loss = []
        a_loss = []
        
        with torch.no_grad():
            critic_value_ = self.agent.target_critic(car_D_, scooter_D_, car_S_, scooter_S_, new_splits, new_first_greens).flatten()
            target = rewards[:, 0] + self.agent.gamma * critic_value_
        
        critic_value = self.agent.critic(car_D, scooter_D, car_S, scooter_S, old_splits, old_first_greens).flatten()
        critic_loss = F.mse_loss(critic_value, target.detach())
        self.agent.critic.optimizer.zero_grad()
        critic_loss.backward(retain_graph=True)
        self.agent.critic.optimizer.step()

        actor_loss = self.agent.critic(car_D, scooter_D, car_S, scooter_S, mu_splits, mu_first_greens).flatten()
        
        torch.autograd.set_detect_anomaly(True)
        actor_loss = -torch.mean(actor_loss)
        self.agent.actor.optimizer.zero_grad()
        actor_loss.backward(retain_graph=True)
        self.agent.actor.optimizer.step()

        self.agent.update_network_parameters()
        
        c_loss.append(critic_loss.detach().cpu().numpy())
        a_loss.append(actor_loss.detach().cpu().numpy())
            
        return c_loss, a_loss
