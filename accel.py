from mpu6050 import mpu6050

sensor = mpu6050(0x68)
acl_data = sensor.get_accel_data()