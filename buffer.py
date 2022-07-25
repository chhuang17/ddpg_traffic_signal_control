import numpy as np
from collections import deque


class ReplayBuffer:
    def __init__(self, max_size, batch_size, n_agents):
        self.mem_size = max_size
        self.mem_counter = 0
        self.batch_size = batch_size
        self.n_agents = n_agents

        # global memory
        self.car_D_memory = deque(maxlen=self.mem_size)
        self.scooter_D_memory = deque(maxlen=self.mem_size)
        self.car_S_memory = deque(maxlen=self.mem_size)
        self.scooter_S_memory = deque(maxlen=self.mem_size)

        self.new_car_D_memory = deque(maxlen=self.mem_size)
        self.new_scooter_D_memory = deque(maxlen=self.mem_size)
        self.new_car_S_memory = deque(maxlen=self.mem_size)
        self.new_scooter_S_memory = deque(maxlen=self.mem_size)
        
        self.split_memory = deque(maxlen=self.mem_size)
        self.first_green_memory = deque(maxlen=self.mem_size)
        
        self.reward_memory = np.zeros((self.mem_size, self.n_agents))

    def store_transition(self, car_D, scooter_D, car_S, scooter_S, splits, first_greens, reward,
                         car_D_, scooter_D_, car_S_, scooter_S_):        
        if self.mem_counter >= self.mem_size:
            self.car_D_memory.popleft()
            self.scooter_D_memory.popleft()
            self.car_S_memory.popleft()
            self.scooter_S_memory.popleft()

            self.new_car_D_memory.popleft()
            self.new_scooter_D_memory.popleft()
            self.new_car_S_memory.popleft()
            self.new_scooter_S_memory.popleft()
            
            self.split_memory.popleft()
            self.first_green_memory.popleft()
            
            self.car_D_memory.append(car_D)
            self.scooter_D_memory.append(scooter_D)
            self.car_S_memory.append(car_S)
            self.scooter_S_memory.append(scooter_S)

            self.new_car_D_memory.append(car_D_)
            self.new_scooter_D_memory.append(scooter_D_)
            self.new_car_S_memory.append(car_S_)
            self.new_scooter_S_memory.append(scooter_S_)
            
            self.split_memory.append(splits)
            self.first_green_memory.append(first_greens)
            
            temp_rewards = np.zeros((self.mem_size, self.n_agents))
            temp_rewards[0:-1, :] = self.reward_memory[1:, :]
            temp_rewards[-1] = reward
            self.reward_memory = temp_rewards        
        else:
            index = self.mem_counter % self.mem_size
            
            self.car_D_memory.append(car_D)
            self.scooter_D_memory.append(scooter_D)
            self.car_S_memory.append(car_S)
            self.scooter_S_memory.append(scooter_S)

            self.new_car_D_memory.append(car_D_)
            self.new_scooter_D_memory.append(scooter_D_)
            self.new_car_S_memory.append(car_S_)
            self.new_scooter_S_memory.append(scooter_S_)
            
            self.split_memory.append(splits)
            self.first_green_memory.append(first_greens)
            
            self.reward_memory[index] = reward
        
        self.mem_counter += 1

    def sample_buffer(self):
        max_mem = min(self.mem_counter, self.mem_size)
        batch = np.random.choice(max_mem, self.batch_size, replace=False)

        car_dens = []
        scooter_dens = []
        car_speed = []
        scooter_speed = []
        
        new_car_dens = []
        new_scooter_dens = []
        new_car_speed = []
        new_scooter_speed = []
        
        splits = []
        first_greens = []
        
        rewards = self.reward_memory[batch]

        for idx in range(self.batch_size):
            car_dens.append(self.car_D_memory[batch[idx]])
            scooter_dens.append(self.scooter_D_memory[batch[idx]])
            car_speed.append(self.car_S_memory[batch[idx]])
            scooter_speed.append(self.scooter_S_memory[batch[idx]])
            
            new_car_dens.append(self.new_car_D_memory[batch[idx]])
            new_scooter_dens.append(self.new_scooter_D_memory[batch[idx]])
            new_car_speed.append(self.new_car_S_memory[batch[idx]])
            new_scooter_speed.append(self.new_scooter_S_memory[batch[idx]])
            
            splits.append(self.split_memory[batch[idx]])
            first_greens.append(self.first_green_memory[batch[idx]])

        return car_dens, scooter_dens, car_speed, scooter_speed, splits, first_greens, rewards, \
               new_car_dens, new_scooter_dens, new_car_speed, new_scooter_speed

    def ready(self):
        if self.mem_counter >= self.batch_size:
            return True
