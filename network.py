# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 14:50:40 2021

@author: Home
"""

import os
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class Actor(nn.Module):
    def __init__(self, alpha, name, chkpt_dir):
        super(Actor, self).__init__()
        
        self.chkpt_file = os.path.join(chkpt_dir, name)

        self.fc1 = nn.Linear(12, 100)
        self.bn1 = nn.LayerNorm(100)
        
        self.fc2 = nn.Linear(400, 400)
        self.bn2 = nn.LayerNorm(400)
        
        self.mu = nn.Linear(400, 6)
        
        self.optimizer = optim.Adam(self.parameters(), lr=alpha)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, car_D, scooter_D, car_S, scooter_S):
        torch.autograd.set_detect_anomaly(True)
        x = self.fc1(car_D)
        x = self.bn1(x)
        x = F.relu(x).flatten(1)
        
        y = self.fc1(scooter_D)
        y = self.bn1(y)
        y = F.relu(y).flatten(1)
        
        z = self.fc1(car_S)
        z = self.bn1(z)
        z = F.relu(z).flatten(1)
        
        w = self.fc1(scooter_S)
        w = self.bn1(w)
        w = F.relu(w).flatten(1)
        
        xyzw = torch.cat([x, y, z, w], dim=1)
        xyzw = self.fc2(xyzw)
        xyzw = self.bn2(xyzw)
        xyzw = F.relu(xyzw)
        
        xyzw = self.mu(xyzw)
        xyzw = torch.sigmoid(xyzw)
        return xyzw

    def save_checkpoint(self):
        torch.save(self.state_dict(), self.chkpt_file)

    def load_checkpoint(self):
        self.load_state_dict(torch.load(self.chkpt_file))


class Critic(nn.Module):
    def __init__(self, beta, name, chkpt_dir):
        super(Critic, self).__init__()

        self.chkpt_file = os.path.join(chkpt_dir, name)

        self.fc1 = nn.Linear(12, 100)
        self.bn1 = nn.LayerNorm(100)
        
        self.split_value = nn.Linear(3, 25)
        self.offset_value = nn.Linear(3, 25)
        self.bn = nn.LayerNorm(25)
        
        self.fc2 = nn.Linear(450, 450)
        self.bn2 = nn.LayerNorm(450)
        
        self.q = nn.Linear(450, 1)
        
        self.optimizer = optim.Adam(self.parameters(), lr=beta, weight_decay=0.01)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, car_D, scooter_D, car_S, scooter_S, splits, offsets):
        torch.autograd.set_detect_anomaly(True)
        cd = self.fc1(car_D)
        cd = self.bn1(cd)
        cd = F.relu(cd).flatten(1)
        
        sd = self.fc1(scooter_D)
        sd = self.bn1(sd)
        sd = F.relu(sd).flatten(1)
        
        cs = self.fc1(car_S)
        cs = self.bn1(cs)
        cs = F.relu(cs).flatten(1)
        
        ss = self.fc1(scooter_S)
        ss = self.bn1(ss)
        ss = F.relu(ss).flatten(1)
        
        split_value = self.split_value(splits)
        split_value = self.bn(split_value)
        split_value = F.relu(split_value).flatten(1)
        
        offset_value = self.offset_value(offsets)
        offset_value = self.bn(offset_value)
        offset_value = F.relu(offset_value).flatten(1)
        
        state_action_value = torch.cat([cd, sd, cs, ss, split_value, offset_value], dim=1)
        
        state_action_value = self.fc2(state_action_value)
        state_action_value = self.bn2(state_action_value)
        state_action_value = F.relu(state_action_value)
        
        state_action_value = self.q(state_action_value)
        
        return state_action_value

    def save_checkpoint(self):
        torch.save(self.state_dict(), self.chkpt_file)

    def load_checkpoint(self):
        self.load_state_dict(torch.load(self.chkpt_file))
