import pynput.mouse as mouse
import pynput.keyboard as keyboard
from time import sleep
import json


class Macro:

    def __init__(self):
        self.macro_pattern = []
        self.macro_file = 'macro_save.json'
        self.__macro_status = False
        self.__delay = 0
        self.program_working = True
        self.left_clicked = False
        self.macro_power = 1
        self.active_index = 0

        self.mouseC = mouse.Controller()
        self.keyboardC = keyboard.Controller()

        mouse_listener = mouse.Listener(on_click=self.on_click)
        mouse_listener.start()
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        keyboard_listener.start()

    def act_macro(self):
        i = 0
        while self.get_macro_status() and self.left_clicked:
            if i >= len(self.macro_pattern):
                i = 0

            try:
                self.mouseC.move(self.get_macro_power() * int(self.macro_pattern[i][0]),
                             self.get_macro_power() * int(self.macro_pattern[i][1]))
                sleep(float(self.macro_pattern[i][2]))
            except:
                try:
                    self.set_macro_index(0)
                except:
                    self.create_macro_pattern("The macro created automatically. Do not activate macro when you have no macro created.It will print the first character of 'Error'.",
                                              [[-10, 0, 0.02],
                                                [0, 10, 0.02],
                                                [10, 0, 0.02],
                                                [-10, 0, 0.02],
                                                [0, 10, 0.02],
                                                [10, 0, 0.02]])
                    print("The macro created automatically. Do not activate macro when you have no macro created.It will print the first character of 'Error'.")
            i = i + 1

    def create_macro_pattern(self, macro_name, macro_pattern):
        temp = {
            "name": macro_name,
            "activation_key": "",
            "macro_pattern": macro_pattern
        }

        data = self.get_macro_patterns()
        data["macros"].append(temp)

        with open(self.macro_file, "w") as f:
            json.dump(data, f, indent=2)

    def set_macro_pattern(self):
        data = self.get_macro_patterns()
        active_index = self.get_macro_index()
        pattern = data["macros"][active_index]["macro_pattern"]
        for item in pattern:
            self.macro_pattern.append(item)

    def get_macro_patterns(self):
        try:
            with open(self.macro_file, "r") as file:
                data = json.load(file)
        except:
            with open(self.macro_file, "w") as file:
                temp = {
                    "macros": []
                }
                data = json.dump(temp, file, indent=2)
        return data

    def set_preview_macro(self, temp_pattern):
        self.macro_pattern = temp_pattern

    def set_macro_status(self, _status):
        self.__macro_status = _status

    def get_macro_status(self):
        return self.__macro_status

    def set_program_working(self, _closed):
        self.program_working = _closed

    def get_program_working(self):
        return self.program_working

    def set_macro_power(self, _power):
        self.macro_power = _power

    def get_macro_power(self):
        return self.macro_power

    def set_macro_index(self, _index):
        self.active_index = _index
        self.set_macro_pattern()

    def get_macro_index(self):
        return self.active_index

    def on_press(self, key):
        if key == keyboard.Key.f12:
            working = not self.get_macro_status()
            self.set_macro_status(working)

    def on_click(self, x, y, button, pressed):
        if pressed and button == mouse.Button.left:
            self.left_clicked = True
        else:
            self.left_clicked = False

    def mainloop(self):
        while self.get_program_working():
            self.act_macro()


def main():
    mcr = Macro()
    mcr.mainloop()


if __name__ == '__main__':
    main()
