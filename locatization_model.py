
import numpy as np

# need to import this module to use robot to located itself 

# define numpy arrays for the April tags ([x,y,teta])
origin = np.array([0, 0, 0])
x_axis = np.array([0, 0, 0])
y_axis = np.array([0, 0, 0])
frame = np.array([origin,x_axis,y_axis])
robot_position=np.array([0,0,0])
target_position=np.array([0,0,0])
desired_position=np.array([0,0,0])
enable_control = False

#robot Pose (in robot frame)
x = 0
y = 0
theta = 0


T_Vel = np.array([[1,0,0],[0,1,0],[-1,0,0],[0,-1,0],[0,0,0]])
T1_Vel = T_Vel.T
#print('T1_Vel',T1_Vel)
T_Pose = np.array([[0,0,0],[0.1,0,0],[-0.1,0,0]])
T1_Pose = T_Pose.T
#print('T1_Pose',T1_Pose)
Target_Pose = np.array([[1,1,0]])
#Target_Pose = Target_Pose.T