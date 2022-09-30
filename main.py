
from pynput.keyboard import Controller as KBController, Key
from pynput.mouse import Controller as MouseController, Button
from pynput import mouse, keyboard

# Constants
MK = "Mouse-Keyboard"
KM = "Keyboard-Mouse"
KK = "Keyboard-Keyboard"
MM = "Mouse-Mouse"
MF = "Mouse-Function"
KF = "Keyboard-Function"


class Hotkey_Handler:
    def __init__(self):
        self.DEBUG_PRINT_KEY_PRESSED = False
        self.DEBUG_PRINT_SETUP = True
        self.Mouse = MouseController()
        self.Keyboard = KBController()
        self.listener_kb = None
        self.listener_mouse = None
        self.hotkeys = {
            MK:{},
            KM:{},
            KK:{},
            MM:{},
            MF:{},
            KF:{},
        }

    def add_hotkey(self, detect, execute, execute_type=KK):
        """Adds a hotkey to the hotkey list.
        
        Hotkeys do not currently block the pressed key. This means that if you press a hotkey, the initial key will still be pressed. This is an option I intend to add in the future
        
        Args:
            detect:
                Accepts: `keyboard.Key.*`, `keyboard.Keycode(char="*")`, `mouse.Button.*`
                Description: The key / button to detect.
            execute:
                Accepts: `keyboard.Key.*`, `keyboard.Keycode(char="*")`, `mouse.Button.*`, `function`
                Description: The key / button / function to do.
            execute_type: 
                Accepts: `MK`, `KM`, `KK`, `MM`, `MF`, `KF`: 
                Description: The type of hotkey. Defaults to KK. K represents Keyboard, M represents Mouse, F represents Function.
        """
        if not isinstance(detect, str): detect = str(detect)
        if callable(execute): pass
        elif not isinstance(execute, str): execute = str(execute)
        if self.DEBUG_PRINT_SETUP: print(f"{str(detect).ljust(99)[:10]} ➔  {(str(execute)[:17] + '...') if len(str(execute)) > 20 else str(execute).ljust(99)[:20]} | ({str(execute_type)})")
        self.hotkeys[execute_type][detect] = execute
        
    def _mouse_press(self, x, y, button, pressed):
        """Mouse pressed event handler"""
        if pressed==True and self.DEBUG_PRINT_KEY_PRESSED: print(button)

        for item in self.hotkeys[MK]:
            if str(button) == item and pressed == True:
                self.Keyboard.tap(eval(f"{self.hotkeys[MK][item]}"))
                break
        for item in self.hotkeys[MM]:
            if str(button) == item and pressed == True:
                self.Mouse.click(eval(f"{self.hotkeys[MM][item]}"))
                break
        for item in self.hotkeys[MF]:
            if str(button) == item and pressed == True:
                self.hotkeys[MF][item]()
                break

    def _kb_press(self, key):
        """Keyboard pressed event handler"""
        try: key = key.char
        except: pass

        if self.DEBUG_PRINT_KEY_PRESSED: print(key)

        for item in self.hotkeys[KM]:
            if str(key) == item:
                self.Mouse.click(eval(f"{self.hotkeys[KM][item]}"))
                break
        for item in self.hotkeys[KK]:
            if str(key) == item:
                self.Keyboard.tap(eval(f"{self.hotkeys[KK][item]}"))
                break
        for item in self.hotkeys[KF]:
            if str(key) == item:
                self.hotkeys[KF][item]()
                break
        
    def start_detached(self):
        """Starts the hotkey handler in detached mode. This means that the hotkey handler will run in the background and will not block the main thread. This is useful for GUIs."""
        if self.DEBUG_PRINT_SETUP: print("\nStarted! Running in Detached mode.")
        self.listener_kb = keyboard.Listener(
            on_press=self._kb_press)
        self.listener_kb.start()

        self.listener_mouse = mouse.Listener(
            on_click=self._mouse_press)
        self.listener_mouse.start()

    def start(self):
        """Starts the hotkey handler in attached mode. This means that the hotkey handler will run in the foreground and will block the main thread. This is useful for CLI programs."""
        if self.DEBUG_PRINT_SETUP: print("\nStarted! Running in Attached mode.")
        self.listener_kb = keyboard.Listener(
            on_press=self._kb_press)
        self.listener_kb.start()

        with mouse.Listener(
                on_click=self._mouse_press) as self.listener_mouse:
            self.listener_mouse.join()

    def stop(self):
        """Stops the hotkey handler"""
        self.listener_mouse.stop()
        self.listener_kb.stop()

    def get_hotkeys(self):
        """Returns the hotkey dictionary"""
        return self.hotkeys

if __name__ == "__main__":
    #def helloWorld():
    #    print("Hello, World!")
    #def printData():
    #    print(c.get_hotkeys())

    c = Hotkey_Handler()
    #c.add_hotkey(mouse.Button.x1, keyboard.Key.f15, execute_type=MK)
    #c.add_hotkey(mouse.Button.x2, keyboard.KeyCode(char="a"), execute_type=MK)
    #c.add_hotkey(mouse.Button.x1, mouse.Button.x2, execute_type=MM)
    #c.add_hotkey(mouse.Button.x2, helloWorld, execute_type=MF)
    #c.add_hotkey(keyboard.Key.enter, mouse.Button.x1, execute_type=KM)
    #c.add_hotkey(keyboard.Key.shift, keyboard.Key.f15, execute_type=KK)
    #c.add_hotkey(keyboard.Key.esc, printData, execute_type=KF)
    
    c.start()
