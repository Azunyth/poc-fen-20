from drive.entities.drive import Drive
from drive.constants.turck import SENSORS
from drive.entities.sensor import Sensor
import sched, time


def init_sensors():
    sensors = []
    for i in range(len(SENSORS)):
        sensors.append(Sensor(SENSORS[i]))
    return sensors

def run():
    drive = Drive(init_sensors())
    s = sched.scheduler(time.time, time.sleep)
    try:
        s.enter(0.5, 1, drive.read_registers, (s,))
        s.run()
    except:
        drive.close_modbus()

if __name__ == "__main__":
    run()