from .vehicle import Vehicle


class Sensor:

    def __init__(self, parameters):
        self.input = parameters['input']
        self.name = parameters['name']
        self.is_first = parameters['is_first']
        self.current_state = False
        self.last_update_at = None

    def update_state(self, new_state, update_at):
        if new_state != self.current_state:
            self.current_state = new_state
            self.last_update_at = update_at
            if self.current_state:
                self.on_detect()
            return True

        return False

    def on_detect(self):
        if self.is_first:
            return Vehicle()

        return None

    def get_readable_state(self):
        return "ON" if self.current_state else "OFF"
