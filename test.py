import serial 
import numpy as np
from filterpy.kalman import KalmanFilter
import time
import math
import queue

q = queue.Queue()                                                                                                                                                                                                                                                                                                                                                                                                                                  
# 初始化卡尔曼滤波器
kf = KalmanFilter(dim_x=2, dim_z=1)
kf.x = np.array([0., 0.])  # 初始状态
kf.F = np.array([[1., 0.1], [0., 1.]])  # 状态转移矩阵
kf.H = np.array([[1., 0.]])  # 测量函数
kf.P = np.array([[1., 0.], [0., 1.]])  # 协方差矩阵
kf.R = 0.01  # 测量噪声

# 初始化用于计算角度的变量
dt = 0.01  # 时间步长
angle = 0.  # 当前角度
gyro_bias = 0.  # 陀螺仪偏差

try:
	ser = serial.Serial('/dev/ttyUSB1',9600)
except:
	print("Please check the port")
	

print("hello")


gyro_x = 0.0
gyro_y = 0.0 
gyro_z = 0.0

angle = 0.0
while True:
	data = ser.readline().decode('utf-8').strip()
	values = data.split(",")
	if len(values) == 3:
		gyro_x = float(values[0])
		gyro_y = float(values[1])
		gyro_z = float(values[2])
		
		
	# 
	gyro_x -= gyro_bias
	gyro_y -= gyro_bias
	gyro_z -= gyro_bias

	angle = gyro_z * dt 
	
	#print("ANgle:" ,angle)
    # Kalman on Angle
	kf.predict()
	kf.update(np.array([angle]))
	angle = kf.x[0]

    # 使用卡尔曼滤波器输出调整陀螺仪偏差
	gyro_bias = kf.x[1]
	
	#angle = angle * 180.0 / math.pi
	print('angle_x: %.2f deg, gyro_bias: %.2f deg/s' % (angle * 180.0 / math.pi, gyro_bias * 180.0 / math.pi))
	
	
	time.sleep(0.01)



    


