# MPU6050 9-DoF Example Printout
import math

from mpu9250_i2c import *

time.sleep(1) # delay necessary to allow mpu9250 to settle

print('recording data')
while 1:
    try:
        ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
        mx,my,mz = AK8963_conv() # read and convert AK8963 magnetometer data
    except:
        continue
    
    pitch = math.atan2(ay, az) * 57.3
    roll = math.atan2(ax, az) * 57.3
    yaw = math.atan2(ax, ay) * 57.3
    
    print('{}'.format('-'*30))
    print('accel [g]: x = {0:2.2f}, y = {1:2.2f}, z {2:2.2f}= '.format(ax,ay,az))
    print('gyro [dps]:  x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f}'.format(wx,wy,wz))
    print('mag [uT]:   x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f}'.format(mx,my,mz))
    print('roll : {0:2.2f}'.format(roll))
    print('pitch : {0:2.2f}'.format(pitch))
    print('yaw : {0:2.2f}'.format(yaw))
    print('{}'.format('-'*30))
    time.sleep(1)