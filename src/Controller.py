import evdev
from servo import Servomotor
from HardwareConstants import ButtonConstants, JoystickConstants
import threading
import time

class Controller(ButtonConstants, JoystickConstants):
    """USB encoder class

    This class handles the "Joystick"* USB encoder to manage joystick and buttons events

    *"Joystick" is the name of the USB encoder, but both joysticks and buttons are connected to it.
    """
    #Joystick axes
    JS_V = 0
    JS_H = 1

    def __init__(self):
        ButtonConstants.__init__(self)
        JoystickConstants.__init__(self)
        self.servo = Servomotor()
        self.device = self.get_joystick_device()
        self.js_state = JoystickConstants.JS_MIDDLE
        t = threading.Thread(target=self.update_servomotors)
        t.setDaemon(True)
        t.start()

    def update_servomotors(self):
        """Update servomotors

        To be used as separate thread to move servos based on joystick state
        """
        while 1:
            self.servo.update_servo(self.js_state)
            time.sleep(0.00001) 

    def get_joystick_device(self):
        """Find USB encoder device

        Lists evdev devices list to find "Joystick" device
        """
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if 'Joystick' in device.name:
                return device
        raise SystemError("Could not find Joystick device, make sure the USB controller is correctly plugged")
        
    def read_event(self):
        """Read USB encoder events

        Poll encoder until event or timeout
        """
        n_reads, max_reads = 0, 1000
        event = None

        while n_reads < max_reads and event is None:
            event = self.convert_to_named_event(self.device.read_one())
            n_reads += 1
        return event

    def convert_to_named_event(self, event):
        """Convert encoder event to specific constant as found in HardwareConstants

        Positional argument:
        event -- USB encoder event
        """
        if event is None:
            return
        if event.type == evdev.ecodes.EV_ABS:
            if event.code == self.JS_H:
                if event.value == self.LEFT:
                    self.js_state = self.JS_LEFT
                elif event.value == self.RIGHT:
                    self.js_state = self.JS_RIGHT
                elif event.value == self.MIDDLE:
                    self.js_state = self.JS_MIDDLE
                self.servo.update_servo(self.js_state)

            elif event.code == self.JS_V:
                if event.value == self.DOWN:
                    self.js_state = self.JS_DOWN
                elif event.value == self.UP:
                    self.js_state = self.JS_UP
                elif event.value == self.MIDDLE:
                    self.js_state = self.JS_MIDDLE
                self.servo.update_servo(self.js_state)
            
        elif event.type == evdev.ecodes.EV_KEY:
            if event.code == self.BTN_0:
                if event.value == self.BTN_PRESSED:
                    return self.BTN_0_PRESSED

            if event.code == self.BTN_1:
                if event.value == self.BTN_PRESSED:
                    return self.BTN_1_PRESSED

            if event.code == self.BTN_2:
                if event.value == self.BTN_PRESSED:
                    return self.BTN_2_PRESSED

            if event.code == self.BTN_3:
                if event.value == self.BTN_PRESSED:
                    return self.BTN_3_PRESSED

            if event.code == self.BTN_4:
                if event.value == self.BTN_PRESSED:
                    return self.BTN_4_PRESSED

            if event.code == self.BTN_5:
                if event.value == self.BTN_PRESSED:
                    return self.BTN_5_PRESSED

            if event.code == self.BTN_6:
                if event.value == self.BTN_PRESSED:
                    return self.BTN_6_PRESSED

            if event.code == self.BTN_7:
                if event.value == self.BTN_PRESSED:
                    return self.BTN_7_PRESSED

            if event.code == self.BTN_8:
                if event.value == self.BTN_PRESSED:
                    return self.BTN_8_PRESSED

            if event.code == self.BTN_9:
                if event.value == self.BTN_PRESSED:
                    return self.BTN_9_PRESSED
