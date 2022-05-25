class JoystickConstants:
    """Joystick constants used by USB encoder
    """
    # Joystick axes
    JS_V = 0
    JS_H = 1

    # Joystick states
    DOWN = LEFT = 0
    UP = RIGHT = 255
    MIDDLE = 127

    # Joystick events
    JS_DOWN = 5001
    JS_UP = 5002
    JS_LEFT = 5003
    JS_RIGHT = 5004
    JS_MIDDLE = 5005

class ButtonConstants:
    """Buttons constants used by USB encoder
    """
    # Button pressed states
    BTN_0 = 288
    BTN_1 = 289
    BTN_2 = 290
    BTN_3 = 291
    BTN_4 = 292
    BTN_5 = 293
    BTN_6 = 294
    BTN_7 = 295
    BTN_8 = 296
    BTN_9 = 297
    
    # Button events
    BTN_0_PRESSED = 1000
    BTN_1_PRESSED = 1001
    BTN_2_PRESSED = 1002
    BTN_3_PRESSED = 1003
    BTN_4_PRESSED = 1004
    BTN_5_PRESSED = 1005
    BTN_6_PRESSED = 1006
    BTN_7_PRESSED = 1007
    BTN_8_PRESSED = 1008
    BTN_9_PRESSED = 1009
    
    BTN_PRESSED  = 1
    BTN_RELEASED = 0
