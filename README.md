# DDPG Real-Time Traffic Signal Control Method
This project introduces the Deep Deterministic Policy Gradient algorithm to develop a real-time traffic signal control method,
and aims to apply the special traffic flow pattern in Taiwan.
The Deep Deterministic Policy Gradient is one of an algorithm of deep reinforcement learning, which advantage is able to apply to continuous action space.
With this advantage, it may be more flexible to broaden the application to multi-intersection scenarios.

The concept of this traffic signal control algorithm is to adjust the split of each intersection and the offset among all intersections every minute,
trying to get better performance in comparison to the traditional pre-timed signal control method.


## Methodology
In this project, we used the Vissim traffic simulation software to validate our DDPG real-time traffic signal control algorithm.
Also, in the training stage, we used Vissim to simulate the interaction between the ddpg agent and the real traffic environment.
In order to interact to Vissim, we used the **COM Interface** to change the traffic signal in real-time after the ddpg agent computing the new splits and offsets in the next stage.
The control algorithm was written in **Python** and adopted the **PyTorch** framework to build our deep neural network and the ddpg agent.

We built 3 intersections in Vissim as our experimental field, and each of them added motorbike waiting zones **(shown as Figure 1)** and two-stage left turn waiting areas **(shown as Figure 2)**,
catering to the real traffic engineering designation in Taiwan.

We collected the flow and the density data of each link in our road network by Vissim COM API, and took them as the neural network input.
The output layer of the ddpg network contained six neurons, three of which are the arterial green phases(i.e., the splits) in each intersection,
and the rest are the offsets of each intersection.

#### Figure 1
<div align="center">
<img src="https://user-images.githubusercontent.com/81426493/234746198-6a46c05d-f46f-4c0e-8717-3fc957c95389.png">
</div>
<br>

#### Figure 2
<div align="center">
<img src="https://user-images.githubusercontent.com/81426493/234746212-939311c4-f6e7-4ac3-9614-5c56a51a0edc.png">
</div>


## Training
In this project, each episode was represented. To accelerate the training process, we adopted a lower discount factor of 0.6.
According to Ota et al.(2019), we constructed the neural network in a wide and shallow shape.
In other words, the number of layers of the network is fewer, and each layer contains more neurons.
**Figure 3** is the construction of the neural network, and **Figure 4** is the reward curve after training 2000 episodes.

#### Figure 3
<div align="center">
<img src="https://user-images.githubusercontent.com/81426493/234747832-4b83204e-e327-41a9-acf0-132c8f2dc6c6.png">
</div>
<br>

#### Figure 4
<div align="center">
<img src="https://user-images.githubusercontent.com/81426493/234742132-ecfab0e2-512a-4f81-aca0-ef83a8f3ca42.png">
</div>


## Evaluation
To prove our ddpg agent indeed performs better than the traditional methods, we took the simultaneous control method and the Synchro control method into comparison.
The simultaneous method means each intersection operates the same traffic signal phase at the same time. 
The meaning of the Synchro control method in this project is that the signal timing is calculated by the Synchro software,
which is a signal timing optimization software, and is still popular in Taiwan.
We selected the average delay per vehicle as the performance index. We conducted 2 different scenarios to evaluate the robustness of our ddpg agent.

### Scenario 1: Steady Traffic Flow
In this situation, the traffic flow inputted in Vissim was constant every 15 minutes.
**Figure 5 and 6** respectively represent the average delay per car and scooter in each episode. No matter whether the car and the scooter had a lower delay under the control of the ddpg agent.

#### Figure 5 (left) and Figure 6 (right)
<div align="center">
<img src="https://user-images.githubusercontent.com/81426493/234751423-d66321d3-29bb-4da1-8949-403fedf22960.png" width="400" height="280">
<img src="https://user-images.githubusercontent.com/81426493/234751437-16968719-3b42-43a9-bcd9-a22b6cfa6848.png" width="400" height="280">
</div>

### Scenario 2: Unsteady Traffic Flow
We considered the more drastic situation here. We inputted the traffic flow in random every 5 minutes in Vissim.
**Figure 7 and 8** respectively represent the average delay per car and scooter in each episode.
Under this scenario, our ddpg agent still performed better than the other two traditional traffic signal control method.

#### Figure 7 (left) and Figure 8 (right)
<div align="center">
<img src="https://user-images.githubusercontent.com/81426493/234758928-60cfe7dd-a5a4-41fd-8d6d-824c6b1db717.png" width="400" height="280">
<img src="https://user-images.githubusercontent.com/81426493/234758945-a32422a8-5760-49e4-93b2-cf120f933a4e.png" width="400" height="280">
</div>


## Conclusion
In this project, we have proved the availability of the application of the deep deterministic policy gradient in traffic signal control.
No matter whether using the simultaneous signal control method or adopting the optimized timing plans by Synchro,
the ddpg agent can defeat any of them and upgrade the traffic flow efficiency of the urban road network.

Another worth mentioning in this project is that **we reduced the reward discount factor to 0.6, and still possess a better performance.**
The result might be related to the fewer times of interaction between the agent and the environment in each episode.
In our experimental design, each episode represents 60 minutes, and the agent takes action every 1 minute.
In other words, the agent only interacts with the environment only 60 times in each episode.
Therefore, if the agent would like to maximize the total reward in each episode, it might have to take action that can help to get as much reward as it can in each step.
The discovery of this project might be a reference value for the application of the DRL in the traffic signal control field in the future.
