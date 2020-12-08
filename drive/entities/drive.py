import time
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException
from pymodbus.register_read_message import ReadInputRegistersResponse
from drive.constants.turck import HOST, PORT

class Drive:
    client = None
    queue = []

    def __init__(self, sensors):
        self.sensors = sensors
        self.connect_modbus()
        
    def connect_modbus(self):
        try:
            self.client = ModbusClient(HOST, port=PORT)
            print("Opening modbus connection...")
            self.client.connect()
            print("Connection opened")
        except ConnectionException:
            print("Impossible to connect")

    def close_modbus(self):
        print("Closing modbus connection...")
        self.client.close()
        print("Connection closed")

    def add_vehicle(self, vehicle):
        self.queue.append(vehicle)

    def read_registers(self, sc):
        if self.client.is_socket_open():
            t = time.time_ns()
            regs = self.client.read_input_registers(0,1)
            if isinstance(regs, ReadInputRegistersResponse) and regs:
                registers = regs.registers
                if (isinstance(registers, list) and len(registers) > 0):
                    inputs = self.pad_inputs(self.hex_to_binary(registers[0]))
                    inputs = self.parse_input_status(inputs)
                    if len(inputs):
                        for sensor in self.sensors:
                            if sensor.input < len(inputs):
                                updated = sensor.update_state(inputs[sensor.input], t)
                                if updated:
                                    self.send_message(sensor, t)
            try:
                sc.enter(0.5, 1, self.read_registers, (sc, ))
            except:
                print("stop")
        else:
            print("Connection to address '" + HOST + "' could not be made")

    def hex_to_binary(self, hex_code):
        bin_code = bin(hex_code)[2:]
        padding = (4 - len(bin_code) % 4) % 4
        return '0' * padding + bin_code

    def pad_inputs(self, inputs):
        return inputs.zfill(8)

    def parse_input_status(self, inputs):
        inputs = inputs[::-1]
        coils = []
        for i in range(len(inputs)):
            coils.append(inputs[i] == '1')
        return coils

    def send_message(self, sensor, timestamp):
        t = time.localtime(timestamp / 1000000000)
        print("[" + time.strftime("%m/%d/%Y %H:%M:%S", t) + "] : Detection on channel (" + str(sensor.input) + ") : " + sensor.get_readable_state())