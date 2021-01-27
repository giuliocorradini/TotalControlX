import board
from digitalio import DigitalInOut, Direction, Pull
import logging

class Switch:
    def __init__(self):
        self.state = 0
        self.long_counter = 0

        self.callback = None

    def fsm(self, input):
        if self.state == 0:
            if input:
                self.state = 1

        if self.state == 1:
            if self.long_counter == 0:
                self.callback("press")

            if not input:
                self.callback("release")
                self.long_counter = 0
                self.state = 0
            else:
                if self.long_counter > 10:
                    self.long_counter = 0
                    self.callback("long_press")
                    self.state = 2
                else:
                    self.long_counter += 1

        if self.state == 2:
            if not input:
                self.callback("release")
                self.state = 0



class Keyboard:
    def __init__(self, btn_num):
        self.n = btn_num
        self.keys = [Switch() for _ in range(btn_num)]

        self.matrix_out = [
            DigitalInOut(board.D13),
            DigitalInOut(board.D19),
            DigitalInOut(board.D26)
        ]
        for out in self.matrix_out:
            out.direction = Direction.OUTPUT
            out.value = False

        self.matrix_in = [
            DigitalInOut(board.D16),
            DigitalInOut(board.D20),
            DigitalInOut(board.D21)
        ]
        for inp in self.matrix_in:
            inp.direction = Direction.INPUT
            inp.pull = Pull.DOWN


    def check_buttons(self,):
        for i, out in enumerate(self.matrix_out):
            out.value = True
            for j, inp in enumerate(self.matrix_in):
                self.keys[i*3+j].fsm(inp.value)
            out.value = False


    def switch(self, number: int):
        if number >= self.n:
            raise ValueError("Invalid button number")

        def inner(func):    #the wrapper
            def layer(action):
                func(action)
            logging.debug(f"registered {number}")
            self.keys[number].callback = layer
            return layer
                    
        return inner
