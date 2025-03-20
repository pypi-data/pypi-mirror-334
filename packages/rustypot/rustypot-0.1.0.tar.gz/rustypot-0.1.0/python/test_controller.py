import rustypot
import time
import numpy as np

controller = rustypot.FeetechController("/dev/ttyACM1", 1000000, 100, [1], [32], [0])
controller.set_new_target([0])  
time.sleep(2)

update_freq = 50
F = 0.5
A = 40
try:
    while True:
        new_target = A*np.sin(2*np.pi*F*time.time())
        # controller.set_new_target([new_target])  
        # print(controller.get_present_position())
        # print(controller.get_current_speed())
        time.sleep(1/update_freq)
except KeyboardInterrupt:
    controller.freeze()
    time.sleep(1)