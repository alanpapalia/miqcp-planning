import numpy as np
import random
import vtolParam as P

class vtolObstacles:
    def __init__(self, P, start = [0, 0], goal = [5, 5]):
        # max and min size of simulation world
        self.sim_x_max = goal[0] + 1 # P.L
        self.sim_x_min = start[0] # 0
        self.sim_y_max = goal[1] + 1 # P.L
        self.sim_y_min = start[1] # 0
        
        # size of the obstacle
        self.obs_size_max = 1.5;
        self.obs_size_min = 0.5;
        
        # quadcopter size
        self.robot_size_x = 1.0
        self.robot_size_y = 1.0
        
        # goal point and starting point
        self.goal = goal
        self.start = start
        # print("obs class init")
        
    def check_if_inside(self, obs, pt):
        # Check if pt is inside obstacle augmented of the size of the robot
        x_min = obs[0][0] - self.robot_size_x/2.0 
        y_min = obs[0][1] - self.robot_size_y/2.0
        x_max = obs[1][0] - self.robot_size_x/2.0
        y_max = obs[1][0] - self.robot_size_y/2.0
        
        if pt[0] >= x_min and pt[0] <= x_max:
            return True
        if pt[1] >= y_min and pt[1] <= y_max:
            return True
        return False
        
    def check_feasible(self, candidate_obs):
        # checks if an obstacle is in the starting point or arrival point
        if not self.check_if_inside(candidate_obs, self.goal) and not self.check_if_inside(candidate_obs, self.start):
            return True
        return False
        
    def generate_random_coords(self):
        # randomly generate size of the obstacle
        obs_size_x = random.uniform(self.obs_size_min, self.obs_size_max)
        obs_size_y = random.uniform(self.obs_size_min, self.obs_size_max)
        
        # randomly guess bottom left coordinate of the object
        x_min = random.uniform(self.sim_x_min, self.sim_x_max - obs_size_x)
        y_min = random.uniform(self.sim_y_min, self.sim_y_max - obs_size_y)
        x_max = x_min + obs_size_x
        y_max = y_min + obs_size_y
        obstacle = ((x_min, y_min), (x_max, y_max))
        #print("Obstacle: [(x_min, y_min), (x_max, y_max)]: ", obstacle)
        return obstacle
    
    def get_new_random(self):
        # Try to generate an obstacle and check if is 
        # in the starting are or final 
        max_attempts = 1000;
        while(max_attempts > 0):
            candidate_obs = self.generate_random_coords()
            if self.check_feasible(candidate_obs):
                return candidate_obs
            max_attempts -= 1
        print("Unable to generate a feasible obstacle!")
