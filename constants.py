USB_DETECTION_DELAY_SECONDS = 3
ERROR_CHARACTER = '?'
VALUE_UP = 0
VALUE_DOWN = 1

DEFAULT_USB_DEVICE_LIST = [
    (1504, 4608), # Symbol Technologies, Inc, 2008 Symbol Bar Code Scanner
]

CHARMAP = {
    evdev.ecodes.KEY_1: ['1', '!'],
    evdev.ecodes.KEY_2: ['2', '@'],
    evdev.ecodes.KEY_3: ['3', '#'],
    evdev.ecodes.KEY_4: ['4', '$'],
    evdev.ecodes.KEY_5: ['5', '%'],
    evdev.ecodes.KEY_6: ['6', '^'],
    evdev.ecodes.KEY_7: ['7', '&'],
    evdev.ecodes.KEY_8: ['8', '*'],
    evdev.ecodes.KEY_9: ['9', '('],
    evdev.ecodes.KEY_0: ['0', ')'],
    evdev.ecodes.KEY_MINUS: ['-', '_'],
    evdev.ecodes.KEY_EQUAL: ['=', '+'],
    evdev.ecodes.KEY_TAB: ['\t', '\t'],
    evdev.ecodes.KEY_Q: ['q', 'Q'],
    evdev.ecodes.KEY_W: ['w', 'W'],
    evdev.ecodes.KEY_E: ['e', 'E'],
    evdev.ecodes.KEY_R: ['r', 'R'],
    evdev.ecodes.KEY_T: ['t', 'T'],
    evdev.ecodes.KEY_Y: ['y', 'Y'],
    evdev.ecodes.KEY_U: ['u', 'U'],
    evdev.ecodes.KEY_I: ['i', 'I'],
    evdev.ecodes.KEY_O: ['o', 'O'],
    evdev.ecodes.KEY_P: ['p', 'P'],
    evdev.ecodes.KEY_LEFTBRACE: ['[', '{'],
    evdev.ecodes.KEY_RIGHTBRACE: [']', '}'],
    evdev.ecodes.KEY_A: ['a', 'A'],
    evdev.ecodes.KEY_S: ['s', 'S'],
    evdev.ecodes.KEY_D: ['d', 'D'],
    evdev.ecodes.KEY_F: ['f', 'F'],
    evdev.ecodes.KEY_G: ['g', 'G'],
    evdev.ecodes.KEY_H: ['h', 'H'],
    evdev.ecodes.KEY_J: ['j', 'J'],
    evdev.ecodes.KEY_K: ['k', 'K'],
    evdev.ecodes.KEY_L: ['l', 'L'],
    evdev.ecodes.KEY_SEMICOLON: [';', ':'],
    evdev.ecodes.KEY_APOSTROPHE: ['\'', '"'],
    evdev.ecodes.KEY_BACKSLASH: ['\\', '|'],
    evdev.ecodes.KEY_Z: ['z', 'Z'],
    evdev.ecodes.KEY_X: ['x', 'X'],
    evdev.ecodes.KEY_C: ['c', 'C'],
    evdev.ecodes.KEY_V: ['v', 'V'],
    evdev.ecodes.KEY_B: ['b', 'B'],
    evdev.ecodes.KEY_N: ['n', 'N'],
    evdev.ecodes.KEY_M: ['m', 'M'],
    evdev.ecodes.KEY_COMMA: [',', '<'],
    evdev.ecodes.KEY_DOT: ['.', '>'],
    evdev.ecodes.KEY_SLASH: ['/', '?'],
    evdev.ecodes.KEY_SPACE: [' ', ' '],
}