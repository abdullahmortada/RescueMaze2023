import time, math
while True:
    try: 
        from mpu9250_i2c import *
        break
    except:
        continue
import numpy as np
from scipy.integrate import cumtrapz
import RPi.GPIO as GPIO


def get_magneto():
    while True:
        try:
            mx,my,mz = AK8963_conv() # read and convert gyro data
            break
        except:
            continue
    return mx,my,mz


def magneto_cal(cal_size):
    print("-"*50)
    print('Magneto Calibrating - Keep the IMU Steady')
    [get_magneto() for ii in range(0,cal_size)] # clear buffer before calibration
    mpu_array = []
    magneto_offsets = [0.0,0.0,0.0]
    while True:
        try:
            mx,my,mz = get_magneto() # get gyro vals
        except:
            continue

        mpu_array.append([mx,my,mz])

        if np.shape(mpu_array)[0]==cal_size:
            for qq in range(0,3):
                magneto_offsets[qq] = np.mean(np.array(mpu_array)[:,qq]) # average
            break
    print('Magneto Calibration Complete')
    return magneto_offsets

def getHeading():
    while True:
        try:
            ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
            mx,my,mz = AK8963_conv() # read and convert AK8963 magnetometer data
        except:
            continue
        
        return math.atan2(my, mx) * 180 / np.pi


def get_gyro():
    _,_,_,wx,wy,wz = mpu6050_conv() # read and convert gyro data
    return wx,wy,wz

def gyro_cal(cal_size):
    print("-"*50)
    print('Gyro Calibrating - Keep the IMU Steady')
    [get_gyro() for ii in range(0,cal_size)] # clear buffer before calibration
    mpu_array = []
    gyro_offsets = [0.0,0.0,0.0]
    while True:
        try:
            wx,wy,wz = get_gyro() # get gyro vals
        except:
            continue

        mpu_array.append([wx,wy,wz])

        if np.shape(mpu_array)[0]==cal_size:
            for qq in range(0,3):
                gyro_offsets[qq] = np.mean(np.array(mpu_array)[:,qq]) # average
            break
    print('Gyro Calibration Complete')
    return gyro_offsets
    

def getAngle(gyro_offsets):
    
    data,t_vec = [],[]
    t0 = time.time()
    integ1_array = [0]
    while True:
        data.append(get_gyro())
        t_vec.append(time.time()-t0)
        #samp_rate = np.shape(data)[0]/(t_vec[-1]-t_vec[0]) # sample rate
        rot_axis = 2 # axis being rotated (2 = z-axis)
        data_offseted = np.array(data)[:,rot_axis]-gyro_offsets[rot_axis]
        integ1_array = cumtrapz(data_offseted,x=t_vec)
        if len(integ1_array) > 0:
            print(integ1_array[-1])
            if 85 <= integ1_array[-1] <= 95:
                break


def main():
    offsets = gyro_cal(500)
    getAngle(offsets)
    
main()

