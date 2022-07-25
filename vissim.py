# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 16:13:09 2021

@author: Home
"""

import win32com.client as com
import os
import numpy as np
import random


class Vissim:
    def __init__(self, Filename):
        # 讀檔
        self.Vissim = com.gencache.EnsureDispatch('Vissim.Vissim')
        self.Vissim.LoadNet(Filename)

        # 以最快速度模擬
        self.Vissim.Simulation.SetAttValue('UseMaxSimSpeed', True)

        # Simulation parameters
        self.time = 0
        
        self.offset_1 = 0
        self.offset_2 = 0
        self.offset_3 = 0
        
        self.first_green_1 = 0
        self.first_green_2 = 0
        self.first_green_3 = 0

        # 最小綠燈時間
        self.min_green_time = 5

        # 初始時制計畫
        self.plans = {'1': [39, 21], '2': [39, 21], '3': [39, 21]}
        self.cycles = {'1': sum(self.plans['1']), '2': sum(self.plans['2']),
                       '3': sum(self.plans['3'])}

    def reset(self):
        self.time = 0
        
        self.offset_1 = 0
        self.offset_2 = 0
        self.offset_3 = 0
        
        self.first_green_1 = 0
        self.first_green_2 = 0
        self.first_green_3 = 0
        
        self.plans = {'1': [39, 21], '2': [39, 21], '3': [39, 21]}
        self.cycles = {'1': sum(self.plans['1']), '2': sum(self.plans['2']),
                       '3': sum(self.plans['3'])}

    def set_randseed(self, seed):
        self.random_seed = seed
        self.Vissim.Simulation.SetAttValue('Randseed', self.random_seed)

    def quickmode(self, activate):
        self.Vissim.Graphics.CurrentNetworkWindow.SetAttValue('QuickMode', activate)
        
    def set_vehcomp(self, artl_vehcomp, st_vehcomp):
        arterial = [1, 4]
        street = [2, 3, 5, 6, 7, 8]
        for i in arterial:
            self.Vissim.Net.VehicleInputs.ItemByKey(i).SetAttValue('VehComp(1)', artl_vehcomp)
            self.Vissim.Net.VehicleInputs.ItemByKey(i).SetAttValue('VehComp(2)', artl_vehcomp)
            self.Vissim.Net.VehicleInputs.ItemByKey(i).SetAttValue('VehComp(3)', artl_vehcomp)
            self.Vissim.Net.VehicleInputs.ItemByKey(i).SetAttValue('VehComp(4)', artl_vehcomp)
            self.Vissim.Net.VehicleInputs.ItemByKey(i).SetAttValue('VehComp(5)', artl_vehcomp)
        for j in street:
            self.Vissim.Net.VehicleInputs.ItemByKey(j).SetAttValue('VehComp(1)', st_vehcomp)
            self.Vissim.Net.VehicleInputs.ItemByKey(j).SetAttValue('VehComp(2)', st_vehcomp)
            self.Vissim.Net.VehicleInputs.ItemByKey(j).SetAttValue('VehComp(3)', st_vehcomp)
            self.Vissim.Net.VehicleInputs.ItemByKey(j).SetAttValue('VehComp(4)', st_vehcomp)
            self.Vissim.Net.VehicleInputs.ItemByKey(j).SetAttValue('VehComp(5)', st_vehcomp)
    
    def random_veh_input_each_15_min(self, episode):
        population = [i for i in range(400, 2401, 50)]
        
        arterial = [1, 4]
        street = [2, 3, 5, 6, 7, 8]
        
        for i in range(len(arterial)):
            random.seed(episode * arterial[i])
            while True:
                artl_input = random.choices(population, k=4)
                if sum(artl_input) == 6400:
                    break
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(1)', 1600)
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(2)', artl_input[0])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(3)', artl_input[1])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(4)', artl_input[2])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(5)', artl_input[3])
        
        for i in range(len(street)):
            random.seed(episode * street[i])
            while True:
                street_input = random.choices(population, k=4)
                if sum(street_input) == 3200:
                    break
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(1)', 800)
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(2)', street_input[0])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(3)', street_input[1])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(4)', street_input[2])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(5)', street_input[3])
    
    def random_veh_input_each_10_min(self, episode):
        population = [i for i in range(400, 2401, 50)]
        
        arterial = [1, 4]
        street = [2, 3, 5, 6, 7, 8]
        
        for i in range(len(arterial)):
            random.seed(episode * arterial[i])
            while True:
                artl_input = random.choices(population, k=6)
                if sum(artl_input) == 9600:
                    break
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(1)', 1600)
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(2)', artl_input[0])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(3)', artl_input[1])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(4)', artl_input[2])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(5)', artl_input[3])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(6)', artl_input[4])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(7)', artl_input[5])
        
        for i in range(len(street)):
            random.seed(episode * street[i])
            while True:
                street_input = random.choices(population, k=6)
                if sum(street_input) == 4800:
                    break
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(1)', 800)
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(2)', street_input[0])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(3)', street_input[1])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(4)', street_input[2])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(5)', street_input[3])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(6)', street_input[4])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(7)', street_input[5])
    
    def random_veh_input_each_5_min(self, episode):
        population = [i for i in range(400, 2401, 50)]
        
        arterial = [1, 4]
        street = [2, 3, 5, 6, 7, 8]
        
        for i in range(len(arterial)):
            random.seed(episode * arterial[i])
            while True:
                artl_input = random.choices(population, k=12)
                if sum(artl_input) == 19200:
                    break
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(1)', 1600)
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(2)', artl_input[0])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(3)', artl_input[1])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(4)', artl_input[2])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(5)', artl_input[3])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(6)', artl_input[4])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(7)', artl_input[5])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(8)', artl_input[6])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(9)', artl_input[7])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(10)', artl_input[8])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(11)', artl_input[9])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(12)', artl_input[10])
            self.Vissim.Net.VehicleInputs.ItemByKey(arterial[i]).SetAttValue('Volume(13)', artl_input[11])
        
        for i in range(len(street)):
            random.seed(episode * street[i])
            while True:
                street_input = random.choices(population, k=12)
                if sum(street_input) == 9600:
                    break
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(1)', 800)
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(2)', street_input[0])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(3)', street_input[1])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(4)', street_input[2])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(5)', street_input[3])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(6)', street_input[4])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(7)', street_input[5])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(8)', street_input[6])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(9)', street_input[7])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(10)', street_input[8])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(11)', street_input[9])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(12)', street_input[10])
            self.Vissim.Net.VehicleInputs.ItemByKey(street[i]).SetAttValue('Volume(13)', street_input[11])
    
    def set_signal_program(self, program_no):
        self.Vissim.Net.SignalControllers.ItemByKey(1).SetAttValue('ProgNo', program_no)
        self.Vissim.Net.SignalControllers.ItemByKey(2).SetAttValue('ProgNo', program_no)
        self.Vissim.Net.SignalControllers.ItemByKey(3).SetAttValue('ProgNo', program_no)
    
    def warm_up(self, WarmUpTime):
        self.Vissim.Simulation.SetAttValue('SimBreakAt', WarmUpTime)
        self.Vissim.Simulation.RunContinuous()
        self.time = WarmUpTime

    def break_time(self, Time):
        self.Vissim.Simulation.SetAttValue('SimBreakAt', Time)
        self.Vissim.Simulation.RunContinuous()
        self.time = Time

    def run_single_step(self):
        self.Vissim.Simulation.RunSingleStep()
    
    def stop_simulation(self):
        self.Vissim.Simulation.Stop()

    def del_pre_simulation(self):
        for simRun in self.Vissim.Net.SimulationRuns:
            self.Vissim.Net.SimulationRuns.RemoveSimulationRun(simRun)

    def close(self):
        self.Vissim = None

    def get_all_states(self):
        links = [101, 102, 103, 104,
                 201, 202, 203, 204,
                 301, 302, 303, 304]
        car_D = np.zeros(len(links))
        scooter_D = np.zeros(len(links))
        car_S = np.zeros(len(links))
        scooter_S = np.zeros(len(links))
        for i in range(len(links)):
            link_data = self.Vissim.Net.Links.ItemByKey(links[i])
            car_D[i] += float(link_data.AttValue('Concatenate:LinkEvalSegs\Density(Current, Last, 10)'))
            scooter_D[i] += float(link_data.AttValue('Concatenate:LinkEvalSegs\Density(Current, Last, 70)'))
            if link_data.AttValue('Concatenate:LinkEvalSegs\Speed(Current, Last, 10)') == '':
                car_S[i] += 50
            elif link_data.AttValue('Concatenate:LinkEvalSegs\Speed(Current, Last, 70)') == '':
                scooter_S[i] += 50
            else:
                car_S[i] += float(link_data.AttValue('Concatenate:LinkEvalSegs\Speed(Current, Last, 10)'))
                scooter_S[i] += float(link_data.AttValue('Concatenate:LinkEvalSegs\Speed(Current, Last, 70)'))
        
        return car_D, scooter_D, car_S, scooter_S

    def update_timing_plans(self, split_factors, first_green_factors):
        # update_first_timing_plan
        if self.cycles['1'] * split_factors[0] < self.min_green_time + 5:
            self.plans['1'][0] = self.min_green_time + 5
            self.plans['1'][1] = self.cycles['1'] - (self.min_green_time + 5)
        elif self.cycles['1'] * split_factors[0] > self.cycles['1'] - (self.min_green_time + 5):
            self.plans['1'][0] = self.cycles['1'] - (self.min_green_time + 5)
            self.plans['1'][1] = self.min_green_time + 5
        else:
            self.plans['1'][0] = round(self.cycles['1'] * split_factors[0])
            self.plans['1'][1] = self.cycles['1'] - round(self.cycles['1'] * split_factors[0])
        
        # update_second_timing_plan
        if self.cycles['2'] * split_factors[1] < self.min_green_time + 5:
            self.plans['2'][0] = self.min_green_time + 5
            self.plans['2'][1] = self.cycles['2'] - (self.min_green_time + 5)
        elif self.cycles['2'] * split_factors[1] > self.cycles['2'] - (self.min_green_time + 5):
            self.plans['2'][0] = self.cycles['2'] - (self.min_green_time + 5)
            self.plans['2'][1] = self.min_green_time + 5
        else:
            self.plans['2'][0] = round(self.cycles['2'] * split_factors[1])
            self.plans['2'][1] = self.cycles['2'] - round(self.cycles['2'] * split_factors[1])
            
        # update_third_timing_plan
        if self.cycles['3'] * split_factors[2] < self.min_green_time + 5:
            self.plans['3'][0] = self.min_green_time + 5
            self.plans['3'][1] = self.cycles['3'] - (self.min_green_time + 5)
        elif self.cycles['3'] * split_factors[2] > self.cycles['3'] - (self.min_green_time + 5):
            self.plans['3'][0] = self.cycles['3'] - (self.min_green_time + 5)
            self.plans['3'][1] = self.min_green_time + 5
        else:
            self.plans['3'][0] = round(self.cycles['3'] * split_factors[2])
            self.plans['3'][1] = self.cycles['3'] - round(self.cycles['3'] * split_factors[2])
        
        # adjust offsets
        self.first_green_1 = min(int(round((self.plans['1'][1] - 5) * first_green_factors[0])), self.plans['1'][1] - 5)
        self.first_green_2 = min(int(round((self.plans['2'][1] - 5) * first_green_factors[1])), self.plans['2'][1] - 5)
        self.first_green_3 = min(int(round((self.plans['3'][0] - 5) * first_green_factors[2])), self.plans['3'][0] - 5)
        if self.first_green_1 <= 0:
            self.first_green_1 = self.plans['1'][1] - 5
        if self.first_green_2 <= 0:
            self.first_green_2 = self.plans['2'][1] - 5
        if self.first_green_3 <= 5:
            self.first_green_3 = self.plans['3'][0] - 5
    

    def execute_new_timing_plans(self, time):
        self.time = time
        
        SignalController_1 = self.Vissim.Net.SignalControllers.ItemByKey(1)
        SignalController_2 = self.Vissim.Net.SignalControllers.ItemByKey(2)
        SignalController_3 = self.Vissim.Net.SignalControllers.ItemByKey(3)

        # 設定各路口號誌燈頭
        # 1
        West_East_1 = SignalController_1.SGs.ItemByKey(1)
        North_South_1 = SignalController_1.SGs.ItemByKey(2)

        # 2
        West_East_2 = SignalController_2.SGs.ItemByKey(1)
        North_South_2 = SignalController_2.SGs.ItemByKey(2)
        
        # 3
        West_East_3 = SignalController_3.SGs.ItemByKey(1)
        North_South_3 = SignalController_3.SGs.ItemByKey(2)
        

        # 以下是代理預測之綠燈時間
        green_1_0 = self.plans['1'][0] - 5
        green_1_1 = self.plans['1'][1] - 5

        green_2_0 = self.plans['2'][0] - 5
        green_2_1 = self.plans['2'][1] - 5

        green_3_0 = self.plans['3'][0] - 5
        green_3_1 = self.plans['3'][1] - 5

        # 建立綠燈時間字典
        green_time = {'1': [green_1_0, green_1_1],
                      '2': [green_2_0, green_2_1],
                      '3': [green_3_0, green_3_1]}

        # 全紅時間&黃燈時間
        amber = 3
        all_red = 2

        # 判斷當前時相，並控制號誌燈頭
        current_phase_1 = 1
        current_phase_2 = 1
        current_phase_3 = 0

        # 判斷當前時相後，分別建立count table 與 break time table
        count_table = [self.first_green_1, self.first_green_2, self.first_green_3]
        
        break_time_table = [0 for i in range(len(count_table))]
        for i in range(len(break_time_table)):
            break_time_table[i] = count_table[i] + self.time
        
        # 創立一個暫存空間(切換點相同時使用)
        temp = []

        # 檢查break time table是否有相同元素
        def check_other_min(break_time_table):
            same = False
            for i in range(len(break_time_table)):
                for j in range(i):
                    if break_time_table[i] == break_time_table[j] == min(break_time_table):
                        same = True
                        break
            return same
        
        # 當break time table所有元素皆大於10000時即完成一個時間階段
        def end_timestep(break_time_table):
            end = False
            x = 0
            for i in range(len(break_time_table)):
                if break_time_table[i] >= 10000:
                    x += 1
                else:
                    continue
            if x == 3:
                end = True
            return end
        

        # 以下是號誌運作迴圈，經過一個時階後即跳出迴圈
        # 更新時制計畫後再依據新的時制計畫運行號誌
        end = end_timestep(break_time_table)
        while not end:
            # 1
            if break_time_table[0] == min(break_time_table):
                if current_phase_1 == 0:
                    West_East_1.SetAttValue('SigState', 'GREEN')
                    North_South_1.SetAttValue('SigState', 'RED')
                    same = check_other_min(break_time_table)
                    if same == False:
                        if len(temp) == 0:
                            self.break_time(break_time_table[0])
                            current_phase_1 += 0.5
                            count_table[0] += amber
                            break_time_table[0] += amber
                            West_East_1.SetAttValue('SigState', 'AMBER')
                            continue
                        else:
                            temp.clear()
                            current_phase_1 += 0.5
                            count_table[0] += amber
                            break_time_table[0] += amber
                            West_East_1.SetAttValue('SigState', 'AMBER')
                            continue
                    elif same == True:
                        if len(temp) == 0:
                            self.break_time(break_time_table[0])
                            current_phase_1 += 0.5
                            West_East_1.SetAttValue('SigState', 'AMBER')
                            count_table[0] += amber
                            break_time_table[0] += amber
                            temp.append(break_time_table[0])
                            continue
                        else:
                            current_phase_1 += 0.5
                            West_East_1.SetAttValue('SigState', 'AMBER')
                            count_table[0] += amber
                            break_time_table[0] += amber 
                            temp.append(break_time_table[0])
                            continue
                elif current_phase_1 == 0.5:
                    West_East_1.SetAttValue('SigState', 'AMBER')
                    same = check_other_min(break_time_table)
                    if same == False:
                        if len(temp) == 0:
                            self.break_time(break_time_table[0])
                            current_phase_1 += 0.3
                            count_table[0] += all_red
                            break_time_table[0] += all_red
                            West_East_1.SetAttValue('SigState', 'RED')
                            continue
                        else:
                            temp.clear()
                            current_phase_1 += 0.3
                            count_table[0] += all_red
                            break_time_table[0] += all_red
                            West_East_1.SetAttValue('SigState', 'RED')
                            continue
                    elif same == True:
                        if len(temp) == 0:
                            self.break_time(break_time_table[0])
                            current_phase_1 += 0.3
                            West_East_1.SetAttValue('SigState', 'RED')
                            count_table[0] += all_red
                            break_time_table[0] += all_red
                            temp.append(break_time_table[0])
                            continue
                        else:
                            current_phase_1 += 0.3
                            West_East_1.SetAttValue('SigState', 'RED')
                            count_table[0] += all_red
                            break_time_table[0] += all_red
                            temp.append(break_time_table[0])
                            continue
                elif current_phase_1 == 0.8:
                    West_East_1.SetAttValue('SigState', 'RED')
                    same = check_other_min(break_time_table)
                    if same == False:
                        if len(temp) == 0:
                            self.break_time(break_time_table[0])
                            current_phase_1 += 0.2
                            count_table[0] += green_time['1'][1]
                            break_time_table[0] += green_time['1'][1]
                            West_East_1.SetAttValue('SigState', 'RED')
                            North_South_1.SetAttValue('SigState', 'GREEN')
                            if count_table[0] >= 60:
                                break_time_table[0] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                        else:
                            temp.clear()
                            current_phase_1 += 0.2
                            count_table[0] += green_time['1'][1]
                            break_time_table[0] += green_time['1'][1]
                            West_East_1.SetAttValue('SigState', 'RED')
                            North_South_1.SetAttValue('SigState', 'GREEN')
                            if count_table[0] >= 60:
                                break_time_table[0] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                    elif same == True:
                        if len(temp) == 0:
                            self.break_time(break_time_table[0])
                            current_phase_1 += 0.2
                            West_East_1.SetAttValue('SigState', 'RED')
                            North_South_1.SetAttValue('SigState', 'GREEN')
                            count_table[0] += green_time['1'][1]
                            break_time_table[0] += green_time['1'][1]
                            temp.append(break_time_table[0])
                            if count_table[0] >= 60:
                                break_time_table[0] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                        else:
                            current_phase_1 += 0.2
                            West_East_1.SetAttValue('SigState', 'RED')
                            North_South_1.SetAttValue('SigState', 'GREEN')
                            count_table[0] += green_time['1'][1]
                            break_time_table[0] += green_time['1'][1]
                            temp.append(break_time_table[0])
                            if count_table[0] >= 60:
                                break_time_table[0] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                elif current_phase_1 == 1:
                    West_East_1.SetAttValue('SigState', 'RED')
                    North_South_1.SetAttValue('SigState', 'GREEN')
                    same = check_other_min(break_time_table)
                    if same == False:
                        if len(temp) == 0:
                            self.break_time(break_time_table[0])
                            current_phase_1 += 0.5
                            count_table[0] += amber
                            break_time_table[0] += amber
                            North_South_1.SetAttValue('SigState', 'AMBER')
                            continue
                        else:
                            temp.clear()
                            current_phase_1 += 0.5
                            count_table[0] += amber
                            break_time_table[0] += amber
                            North_South_1.SetAttValue('SigState', 'AMBER')
                            continue
                    elif same == True:
                        if len(temp) == 0:
                            self.break_time(break_time_table[0])
                            current_phase_1 += 0.5
                            North_South_1.SetAttValue('SigState', 'AMBER')
                            count_table[0] += amber
                            break_time_table[0] += amber
                            temp.append(break_time_table[0])
                            continue
                        else:
                            current_phase_1 += 0.5
                            North_South_1.SetAttValue('SigState', 'AMBER')
                            count_table[0] += amber
                            break_time_table[0] += amber
                            temp.append(break_time_table[0])
                            continue
                elif current_phase_1 == 1.5:
                    North_South_1.SetAttValue('SigState', 'AMBER')
                    same = check_other_min(break_time_table)
                    if same == False:
                        if len(temp) == 0:
                            self.break_time(break_time_table[0])
                            current_phase_1 += 0.3
                            count_table[0] += all_red
                            break_time_table[0] += all_red
                            North_South_1.SetAttValue('SigState', 'RED')
                            continue
                        else:
                            temp.clear()
                            current_phase_1 += 0.3
                            count_table[0] += all_red
                            break_time_table[0] += all_red
                            North_South_1.SetAttValue('SigState', 'RED')
                            continue
                    elif same == True:
                        if len(temp) == 0:
                            self.break_time(break_time_table[0])
                            current_phase_1 += 0.3
                            North_South_1.SetAttValue('SigState', 'RED')
                            count_table[0] += all_red
                            break_time_table[0] += all_red
                            temp.append(break_time_table[0])
                            continue
                        else:
                            current_phase_1 += 0.3
                            North_South_1.SetAttValue('SigState', 'RED')
                            count_table[0] += all_red
                            break_time_table[0] += all_red
                            temp.append(break_time_table[0])
                            continue
                elif current_phase_1 == 1.8:
                    North_South_1.SetAttValue('SigState', 'RED')
                    same = check_other_min(break_time_table)
                    if same == False:
                        if len(temp) == 0:
                            self.break_time(break_time_table[0])
                            current_phase_1 -= 1.8
                            count_table[0] += green_time['1'][0]
                            break_time_table[0] += green_time['1'][0]
                            West_East_1.SetAttValue('SigState', 'GREEN')
                            North_South_1.SetAttValue('SigState', 'RED')
                            if count_table[0] >= 60:
                                break_time_table[0] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                        else:
                            temp.clear()
                            current_phase_1 -= 1.8
                            count_table[0] += green_time['1'][0]
                            break_time_table[0] += green_time['1'][0]
                            West_East_1.SetAttValue('SigState', 'GREEN')
                            North_South_1.SetAttValue('SigState', 'RED')
                            if count_table[0] >= 60:
                                break_time_table[0] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                    elif same == True:
                        if len(temp) == 0:
                            self.break_time(break_time_table[0])
                            current_phase_1 -= 1.8
                            West_East_1.SetAttValue('SigState', 'GREEN')
                            North_South_1.SetAttValue('SigState', 'RED')
                            count_table[0] += green_time['1'][0]
                            break_time_table[0] += green_time['1'][0]
                            temp.append(break_time_table[0])
                            if count_table[0] >= 60:
                                break_time_table[0] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                        else:
                            current_phase_1 -= 1.8
                            West_East_1.SetAttValue('SigState', 'GREEN')
                            North_South_1.SetAttValue('SigState', 'RED')
                            count_table[0] += green_time['1'][0]
                            break_time_table[0] += green_time['1'][0]
                            temp.append(break_time_table[0])
                            if count_table[0] >= 60:
                                break_time_table[0] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
            # 2
            if break_time_table[1] == min(break_time_table):
                if current_phase_2 == 0:
                    West_East_2.SetAttValue('SigState', 'GREEN')
                    North_South_2.SetAttValue('SigState', 'RED')
                    same = check_other_min(break_time_table)
                    if same == False:
                        if len(temp) == 0:
                            self.break_time(break_time_table[1])
                            current_phase_2 += 0.5
                            count_table[1] += amber
                            break_time_table[1] += amber
                            West_East_2.SetAttValue('SigState', 'AMBER')
                            continue
                        else:
                            temp.clear()
                            current_phase_2 += 0.5
                            count_table[1] += amber
                            break_time_table[1] += amber
                            West_East_2.SetAttValue('SigState', 'AMBER')
                            continue
                    elif same == True:
                        if len(temp) == 0:
                            self.break_time(break_time_table[1])
                            current_phase_2 += 0.5
                            West_East_2.SetAttValue('SigState', 'AMBER')
                            count_table[1] += amber
                            break_time_table[1] += amber
                            temp.append(break_time_table[1])
                            continue
                        else:
                            current_phase_2 += 0.5
                            West_East_2.SetAttValue('SigState', 'AMBER')
                            count_table[1] += amber
                            break_time_table[1] += amber 
                            temp.append(break_time_table[1])
                            continue
                elif current_phase_2 == 0.5:
                    West_East_2.SetAttValue('SigState', 'AMBER')
                    same = check_other_min(break_time_table)
                    if same == False:
                        if len(temp) == 0:
                            self.break_time(break_time_table[1])
                            current_phase_2 += 0.3
                            count_table[1] += all_red
                            break_time_table[1] += all_red
                            West_East_2.SetAttValue('SigState', 'RED')
                            continue
                        else:
                            temp.clear()
                            current_phase_2 += 0.3
                            count_table[1] += all_red
                            break_time_table[1] += all_red
                            West_East_2.SetAttValue('SigState', 'RED')
                            continue
                    elif same == True:
                        if len(temp) == 0:
                            self.break_time(break_time_table[1])
                            current_phase_2 += 0.3
                            West_East_2.SetAttValue('SigState', 'RED')
                            count_table[1] += all_red
                            break_time_table[1] += all_red
                            temp.append(break_time_table[1])
                            continue
                        else:
                            current_phase_2 += 0.3
                            West_East_2.SetAttValue('SigState', 'RED')
                            count_table[1] += all_red
                            break_time_table[1] += all_red
                            temp.append(break_time_table[1])
                            continue
                elif current_phase_2 == 0.8:
                    West_East_2.SetAttValue('SigState', 'RED')
                    same = check_other_min(break_time_table)
                    if same == False:
                        if len(temp) == 0:
                            self.break_time(break_time_table[1])
                            current_phase_2 += 0.2
                            count_table[1] += green_time['2'][1]
                            break_time_table[1] += green_time['2'][1]
                            West_East_2.SetAttValue('SigState', 'RED')
                            North_South_2.SetAttValue('SigState', 'GREEN')
                            if count_table[1] >= 60:
                                break_time_table[1] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                        else:
                            temp.clear()
                            current_phase_2 += 0.2
                            count_table[1] += green_time['2'][1]
                            break_time_table[1] += green_time['2'][1]
                            West_East_2.SetAttValue('SigState', 'RED')
                            North_South_2.SetAttValue('SigState', 'GREEN')
                            if count_table[1] >= 60:
                                break_time_table[1] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                    elif same == True:
                        if len(temp) == 0:
                            self.break_time(break_time_table[1])
                            current_phase_2 += 0.2
                            West_East_2.SetAttValue('SigState', 'RED')
                            North_South_2.SetAttValue('SigState', 'GREEN')
                            count_table[1] += green_time['2'][1]
                            break_time_table[1] += green_time['2'][1]
                            temp.append(break_time_table[1])
                            if count_table[1] >= 60:
                                break_time_table[1] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                        else:
                            current_phase_2 += 0.2
                            West_East_2.SetAttValue('SigState', 'RED')
                            North_South_2.SetAttValue('SigState', 'GREEN')
                            count_table[1] += green_time['2'][1]
                            break_time_table[1] += green_time['2'][1]
                            temp.append(break_time_table[1])
                            if count_table[1] >= 60:
                                break_time_table[1] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                elif current_phase_2 == 1:
                    West_East_2.SetAttValue('SigState', 'RED')
                    North_South_2.SetAttValue('SigState', 'GREEN')
                    same = check_other_min(break_time_table)
                    if same == False:
                        if len(temp) == 0:
                            self.break_time(break_time_table[1])
                            current_phase_2 += 0.5
                            count_table[1] += amber
                            break_time_table[1] += amber
                            North_South_2.SetAttValue('SigState', 'AMBER')
                            continue
                        else:
                            temp.clear()
                            current_phase_2 += 0.5
                            count_table[1] += amber
                            break_time_table[1] += amber
                            North_South_2.SetAttValue('SigState', 'AMBER')
                            continue
                    elif same == True:
                        if len(temp) == 0:
                            self.break_time(break_time_table[1])
                            current_phase_2 += 0.5
                            North_South_2.SetAttValue('SigState', 'AMBER')
                            count_table[1] += amber
                            break_time_table[1] += amber
                            temp.append(break_time_table[1])
                            continue
                        else:
                            current_phase_2 += 0.5
                            North_South_2.SetAttValue('SigState', 'AMBER')
                            count_table[1] += amber
                            break_time_table[1] += amber
                            temp.append(break_time_table[1])
                            continue
                elif current_phase_2 == 1.5:
                    North_South_2.SetAttValue('SigState', 'AMBER')
                    same = check_other_min(break_time_table)
                    if same == False:
                        if len(temp) == 0:
                            self.break_time(break_time_table[1])
                            current_phase_2 += 0.3
                            count_table[1] += all_red
                            break_time_table[1] += all_red
                            North_South_2.SetAttValue('SigState', 'RED')
                            continue
                        else:
                            temp.clear()
                            current_phase_2 += 0.3
                            count_table[1] += all_red
                            break_time_table[1] += all_red
                            North_South_2.SetAttValue('SigState', 'RED')
                            continue
                    elif same == True:
                        if len(temp) == 0:
                            self.break_time(break_time_table[1])
                            current_phase_2 += 0.3
                            North_South_2.SetAttValue('SigState', 'RED')
                            count_table[1] += all_red
                            break_time_table[1] += all_red
                            temp.append(break_time_table[1])
                            continue
                        else:
                            current_phase_2 += 0.3
                            North_South_2.SetAttValue('SigState', 'RED')
                            count_table[1] += all_red
                            break_time_table[1] += all_red
                            temp.append(break_time_table[1])
                            continue
                elif current_phase_2 == 1.8:
                    North_South_2.SetAttValue('SigState', 'RED')
                    same = check_other_min(break_time_table)
                    if same == False:
                        if len(temp) == 0:
                            self.break_time(break_time_table[1])
                            current_phase_2 -= 1.8
                            count_table[1] += green_time['2'][0]
                            break_time_table[1] += green_time['2'][0]
                            West_East_2.SetAttValue('SigState', 'GREEN')
                            North_South_2.SetAttValue('SigState', 'RED')
                            if count_table[1] >= 60:
                                break_time_table[1] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                        else:
                            temp.clear()
                            current_phase_2 -= 1.8
                            count_table[1] += green_time['2'][0]
                            break_time_table[1] += green_time['2'][0]
                            West_East_2.SetAttValue('SigState', 'GREEN')
                            North_South_2.SetAttValue('SigState', 'RED')
                            if count_table[1] >= 60:
                                break_time_table[1] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                    elif same == True:
                        if len(temp) == 0:
                            self.break_time(break_time_table[1])
                            current_phase_2 -= 1.8
                            West_East_2.SetAttValue('SigState', 'GREEN')
                            North_South_2.SetAttValue('SigState', 'RED')
                            count_table[1] += green_time['2'][0]
                            break_time_table[1] += green_time['2'][0]
                            temp.append(break_time_table[1])
                            if count_table[1] >= 60:
                                break_time_table[1] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                        else:
                            current_phase_2 -= 1.8
                            West_East_2.SetAttValue('SigState', 'GREEN')
                            North_South_2.SetAttValue('SigState', 'RED')
                            count_table[1] += green_time['2'][0]
                            break_time_table[1] += green_time['2'][0]
                            temp.append(break_time_table[1])
                            if count_table[1] >= 60:
                                break_time_table[1] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
            # 3
            if break_time_table[2] == min(break_time_table):
                if current_phase_3 == 0:
                    West_East_3.SetAttValue('SigState', 'GREEN')
                    North_South_3.SetAttValue('SigState', 'RED')
                    same = check_other_min(break_time_table)
                    if same == False:
                        if len(temp) == 0:
                            self.break_time(break_time_table[2])
                            current_phase_3 += 0.5
                            count_table[2] += amber
                            break_time_table[2] += amber
                            West_East_3.SetAttValue('SigState', 'AMBER')
                            continue
                        else:
                            temp.clear()
                            current_phase_3 += 0.5
                            count_table[2] += amber
                            break_time_table[2] += amber
                            West_East_3.SetAttValue('SigState', 'AMBER')
                            continue
                    elif same == True:
                        if len(temp) == 0:
                            self.break_time(break_time_table[2])
                            current_phase_3 += 0.5
                            West_East_3.SetAttValue('SigState', 'AMBER')
                            count_table[2] += amber
                            break_time_table[2] += amber
                            temp.append(break_time_table[2])
                            continue
                        else:
                            current_phase_3 += 0.5
                            West_East_3.SetAttValue('SigState', 'AMBER')
                            count_table[2] += amber
                            break_time_table[2] += amber 
                            temp.append(break_time_table[2])
                            continue
                elif current_phase_3 == 0.5:
                    West_East_3.SetAttValue('SigState', 'AMBER')
                    same = check_other_min(break_time_table)
                    if same == False:
                        if len(temp) == 0:
                            self.break_time(break_time_table[2])
                            current_phase_3 += 0.3
                            count_table[2] += all_red
                            break_time_table[2] += all_red
                            West_East_3.SetAttValue('SigState', 'RED')
                            continue
                        else:
                            temp.clear()
                            current_phase_3 += 0.3
                            count_table[2] += all_red
                            break_time_table[2] += all_red
                            West_East_3.SetAttValue('SigState', 'RED')
                            continue
                    elif same == True:
                        if len(temp) == 0:
                            self.break_time(break_time_table[2])
                            current_phase_3 += 0.3
                            West_East_3.SetAttValue('SigState', 'RED')
                            count_table[2] += all_red
                            break_time_table[2] += all_red
                            temp.append(break_time_table[2])
                            continue
                        else:
                            current_phase_3 += 0.3
                            West_East_3.SetAttValue('SigState', 'RED')
                            count_table[2] += all_red
                            break_time_table[2] += all_red
                            temp.append(break_time_table[2])
                            continue
                elif current_phase_3 == 0.8:
                    West_East_3.SetAttValue('SigState', 'RED')
                    same = check_other_min(break_time_table)
                    if same == False:
                        if len(temp) == 0:
                            self.break_time(break_time_table[2])
                            current_phase_3 += 0.2
                            count_table[2] += green_time['3'][1]
                            break_time_table[2] += green_time['3'][1]
                            West_East_3.SetAttValue('SigState', 'RED')
                            North_South_3.SetAttValue('SigState', 'GREEN')
                            if count_table[2] >= 60:
                                break_time_table[2] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                        else:
                            temp.clear()
                            current_phase_3 += 0.2
                            count_table[2] += green_time['3'][1]
                            break_time_table[2] += green_time['3'][1]
                            West_East_3.SetAttValue('SigState', 'RED')
                            North_South_3.SetAttValue('SigState', 'GREEN')
                            if count_table[2] >= 60:
                                break_time_table[2] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                    elif same == True:
                        if len(temp) == 0:
                            self.break_time(break_time_table[2])
                            current_phase_3 += 0.2
                            West_East_3.SetAttValue('SigState', 'RED')
                            North_South_3.SetAttValue('SigState', 'GREEN')
                            count_table[2] += green_time['3'][1]
                            break_time_table[2] += green_time['3'][1]
                            temp.append(break_time_table[2])
                            if count_table[2] >= 60:
                                break_time_table[2] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                        else:
                            current_phase_3 += 0.2
                            West_East_3.SetAttValue('SigState', 'RED')
                            North_South_3.SetAttValue('SigState', 'GREEN')
                            count_table[2] += green_time['3'][1]
                            break_time_table[2] += green_time['3'][1]
                            temp.append(break_time_table[2])
                            if count_table[2] >= 60:
                                break_time_table[2] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                elif current_phase_3 == 1:
                    West_East_3.SetAttValue('SigState', 'RED')
                    North_South_3.SetAttValue('SigState', 'GREEN')
                    same = check_other_min(break_time_table)
                    if same == False:
                        if len(temp) == 0:
                            self.break_time(break_time_table[2])
                            current_phase_3 += 0.5
                            count_table[2] += amber
                            break_time_table[2] += amber
                            North_South_3.SetAttValue('SigState', 'AMBER')
                            continue
                        else:
                            temp.clear()
                            current_phase_3 += 0.5
                            count_table[2] += amber
                            break_time_table[2] += amber
                            North_South_3.SetAttValue('SigState', 'AMBER')
                            continue
                    elif same == True:
                        if len(temp) == 0:
                            self.break_time(break_time_table[2])
                            current_phase_3 += 0.5
                            North_South_3.SetAttValue('SigState', 'AMBER')
                            count_table[2] += amber
                            break_time_table[2] += amber
                            temp.append(break_time_table[2])
                            continue
                        else:
                            current_phase_3 += 0.5
                            North_South_3.SetAttValue('SigState', 'AMBER')
                            count_table[2] += amber
                            break_time_table[2] += amber
                            temp.append(break_time_table[2])
                            continue
                elif current_phase_3 == 1.5:
                    North_South_3.SetAttValue('SigState', 'AMBER')
                    same = check_other_min(break_time_table)
                    if same == False:
                        if len(temp) == 0:
                            self.break_time(break_time_table[2])
                            current_phase_3 += 0.3
                            count_table[2] += all_red
                            break_time_table[2] += all_red
                            North_South_3.SetAttValue('SigState', 'RED')
                            continue
                        else:
                            temp.clear()
                            current_phase_3 += 0.3
                            count_table[2] += all_red
                            break_time_table[2] += all_red
                            North_South_3.SetAttValue('SigState', 'RED')
                            continue
                    elif same == True:
                        if len(temp) == 0:
                            self.break_time(break_time_table[2])
                            current_phase_3 += 0.3
                            North_South_3.SetAttValue('SigState', 'RED')
                            count_table[2] += all_red
                            break_time_table[2] += all_red
                            temp.append(break_time_table[2])
                            continue
                        else:
                            current_phase_3 += 0.3
                            North_South_3.SetAttValue('SigState', 'RED')
                            count_table[2] += all_red
                            break_time_table[2] += all_red
                            temp.append(break_time_table[2])
                            continue
                elif current_phase_3 == 1.8:
                    North_South_3.SetAttValue('SigState', 'RED')
                    same = check_other_min(break_time_table)
                    if same == False:
                        if len(temp) == 0:
                            self.break_time(break_time_table[2])
                            current_phase_3 -= 1.8
                            count_table[2] += green_time['3'][0]
                            break_time_table[2] += green_time['3'][0]
                            West_East_3.SetAttValue('SigState', 'GREEN')
                            North_South_3.SetAttValue('SigState', 'RED')
                            if count_table[2] >= 60:
                                break_time_table[2] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                        else:
                            temp.clear()
                            current_phase_3 -= 1.8
                            count_table[2] += green_time['3'][0]
                            break_time_table[2] += green_time['3'][0]
                            West_East_3.SetAttValue('SigState', 'GREEN')
                            North_South_3.SetAttValue('SigState', 'RED')
                            if count_table[2] >= 60:
                                break_time_table[2] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                    elif same == True:
                        if len(temp) == 0:
                            self.break_time(break_time_table[2])
                            current_phase_3 -= 1.8
                            West_East_3.SetAttValue('SigState', 'GREEN')
                            North_South_3.SetAttValue('SigState', 'RED')
                            count_table[2] += green_time['3'][0]
                            break_time_table[2] += green_time['3'][0]
                            temp.append(break_time_table[2])
                            if count_table[2] >= 60:
                                break_time_table[2] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
                        else:
                            current_phase_3 -= 1.8
                            West_East_3.SetAttValue('SigState', 'GREEN')
                            North_South_3.SetAttValue('SigState', 'RED')
                            count_table[2] += green_time['3'][0]
                            break_time_table[2] += green_time['3'][0]
                            temp.append(break_time_table[2])
                            if count_table[2] >= 60:
                                break_time_table[2] += 10000
                                end = end_timestep(break_time_table)
                                if end == True:
                                    break
                            continue
        
        decision_point = [i for i in range(900, 4501, 60)]
        for p in range(len(decision_point)):
            if self.time not in decision_point:
                if decision_point[p] < self.time <= decision_point[p+1]:
                    self.break_time(decision_point[p+1])
                    
    # 輸出號誌運作：新的時制計畫
    def get_timing_plans(self):
        return self.plans
    
    # 輸出號誌運作：新的週期
    def get_cycles(self):
        return self.cycles
    
    # 輸出號誌運作：新的時差
    def get_offsets(self):
        self.offset_1 = min(self.first_green_1 + 5, self.plans['1'][1])
        self.offset_2 = min(self.first_green_2 + 5, self.plans['2'][1])
        if self.first_green_3 == self.plans['3'][0] - 5:
            self.offset_3 = 0
        else:
            self.offset_3 = self.cycles['3'] - (self.plans['3'][0] - 5 - self.first_green_3)
        return [self.offset_1, self.offset_2, self.offset_3]
    
    """ 以下是reward function考慮項目 """
    # (+): Total throughput
    def get_total_throughput(self):
        throughput_car = np.zeros(1)
        throughput_scooter = np.zeros(1)
        data_collection = self.Vissim.Net.DataCollectionMeasurements.ItemByKey(50)
        throughput_car[0] += data_collection.AttValue('Vehs(Current, Last, 10)')
        throughput_scooter[0] += data_collection.AttValue('Vehs(Current, Last, 70)')
        return throughput_car, throughput_scooter
    
    # (-): Total queue length
    def get_total_queue_length(self):
        total_queue_length = np.zeros(1)
        q_counter = self.Vissim.Net.QueueCounters
        # 1
        total_queue_length[0] += q_counter.ItemByKey(1).AttValue('QLen(Current, Last)') + \
                                 q_counter.ItemByKey(3).AttValue('QLen(Current, Last)') + \
                                 q_counter.ItemByKey(5).AttValue('QLen(Current, Last)') + \
                                 q_counter.ItemByKey(7).AttValue('QLen(Current, Last)') + \
                                 q_counter.ItemByKey(9).AttValue('QLen(Current, Last)') + \
                                 q_counter.ItemByKey(11).AttValue('QLen(Current, Last)') + \
                                 q_counter.ItemByKey(13).AttValue('QLen(Current, Last)') + \
                                 q_counter.ItemByKey(15).AttValue('QLen(Current, Last)') + \
                                 q_counter.ItemByKey(17).AttValue('QLen(Current, Last)') + \
                                 q_counter.ItemByKey(19).AttValue('QLen(Current, Last)') + \
                                 q_counter.ItemByKey(21).AttValue('QLen(Current, Last)') + \
                                 q_counter.ItemByKey(23).AttValue('QLen(Current, Last)')
        
        return total_queue_length
    
    
    """以下是求取各項績效指標"""
    # 求各流向旅行時間
    def get_travel_time(self):
        travtime_meas = self.Vissim.Net.VehicleTravelTimeMeasurements
        detectors = [111, 112, 113, 121, 122, 123, 131, 132, 133, 141, 142, 143,
                     211, 212, 213, 221, 222, 223, 231, 232, 233, 241, 242, 243,
                     311, 312, 313, 321, 322, 323, 331, 332, 333, 341, 342, 343]
        travtime_car = np.zeros(len(detectors))
        travtime_scooter = np.zeros(len(detectors))
        for i in range(len(detectors)):
            travtime_car[i] += travtime_meas.ItemByKey(detectors[i]).AttValue('TravTm(Current,Avg,10)')
            travtime_scooter[i] += travtime_meas.ItemByKey(detectors[i]).AttValue('TravTm(Current,Avg,70)')
        return travtime_car, travtime_scooter
        
    # 求整體路網總旅行時間(分汽車與機車)
    def get_total_travel_time(self):
        performance = self.Vissim.Net.VehicleNetworkPerformanceMeasurement
        travtmtot_car = performance.AttValue('TravTmTot(Current, Avg, 10)')
        travtmtot_scooter = performance.AttValue('TravTmTot(Current, Avg, 70)')
        return travtmtot_car, travtmtot_scooter
    
    # 求整體路網平均旅行時間(分汽車與機車)
    def get_avg_travel_time(self):
        performance = self.Vissim.Net.VehicleNetworkPerformanceMeasurement
        travtmtot_car = performance.AttValue('TravTmTot(Current, Avg, 10)')
        num_cars = performance.AttValue('VehArr(Current, Avg, 10)')
        travtmtot_scooter = performance.AttValue('TravTmTot(Current, Avg, 70)')
        num_scooters = performance.AttValue('VehArr(Current, Avg, 70)')
        travtm_car = travtmtot_car / num_cars
        travtm_scooter = travtmtot_scooter / num_scooters
        return travtm_car, travtm_scooter
    
    # 求所有路口近端流向等候車隊長度
    def get_each_queue_length(self):
        q_counter = self.Vissim.Net.QueueCounters
        detectors = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]
        each_queue_length = np.zeros(len(detectors))
        for i in range(len(detectors)):
            each_queue_length[i] += q_counter.ItemByKey(detectors[i]).AttValue('QLen(Current, Avg)')
        return each_queue_length
    
    # 求平均每車停等次數(分汽車與機車)
    def get_avg_num_stops(self):
        performance = self.Vissim.Net.VehicleNetworkPerformanceMeasurement
        num_stops_car = performance.AttValue('StopsAvg(Current, Avg, 10)')
        num_stops_scooter = performance.AttValue('StopsAvg(Current, Avg, 70)')
        return num_stops_car, num_stops_scooter
    
    # 求整體路網總停等次數(分汽車與機車)
    def get_total_num_stops(self):
        performance = self.Vissim.Net.VehicleNetworkPerformanceMeasurement
        stopstot_car = performance.AttValue('StopsTot(Current, Avg, 10)')
        stopstot_scooter = performance.AttValue('StopsTot(Current, Avg, 70)')
        return stopstot_car, stopstot_scooter
    
    # 求平均每車延滯時間(分汽車與機車)
    def get_avg_delay(self):
        performance = self.Vissim.Net.VehicleNetworkPerformanceMeasurement
        delay_car = performance.AttValue('DelayAvg(Current, Avg, 10)')
        delay_scooter = performance.AttValue('DelayAvg(Current, Avg, 70)')
        return delay_car, delay_scooter
    
    # 求整體路網總延滯時間(分汽車與機車)
    def get_total_delay(self):
        performance = self.Vissim.Net.VehicleNetworkPerformanceMeasurement
        delaytot_car = performance.AttValue('DelayTot(Current, Avg, 10)')
        delaytot_scooter = performance.AttValue('DelayTot(Current, Avg, 70)')
        return delaytot_car, delaytot_scooter
    
    def get_delayrel(self):
        links = [101, 201, 301,
                 103, 203, 303]
        delayrel_car = np.zeros(len(links))
        delayrel_scooter = np.zeros(len(links))
        for i in range(len(links)):
            link_data = self.Vissim.Net.Links.ItemByKey(links[i])
            delayrel_percent_car = link_data.AttValue('Concatenate:LinkEvalSegs\DelayRel(Current, Avg, 10)')
            delayrel_percent_scooter = link_data.AttValue('Concatenate:LinkEvalSegs\DelayRel(Current, Avg, 70)')
            delayrel_car[i] += float(delayrel_percent_car.strip('%'))
            delayrel_scooter[i] += float(delayrel_percent_scooter.strip('%'))        
        return delayrel_car, delayrel_scooter
    
    def get_all_delayrel(self):
        links = [101, 102, 103, 104,
                 201, 202, 203, 204,
                 301, 302, 303, 304]
        delayrel_car = np.zeros(len(links))
        delayrel_scooter = np.zeros(len(links))
        for i in range(len(links)):
            link_data = self.Vissim.Net.Links.ItemByKey(links[i])
            delayrel_percent_car = link_data.AttValue('Concatenate:LinkEvalSegs\DelayRel(Current, Avg, 10)')
            delayrel_percent_scooter = link_data.AttValue('Concatenate:LinkEvalSegs\DelayRel(Current, Avg, 70)')
            delayrel_car[i] += float(delayrel_percent_car.strip('%'))
            delayrel_scooter[i] += float(delayrel_percent_scooter.strip('%'))        
        return delayrel_car, delayrel_scooter
