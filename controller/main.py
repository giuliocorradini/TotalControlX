import board
from digitalio import DigitalInOut, Direction
import adafruit_character_lcd.character_lcd as character_lcd
import asyncio
from time import sleep
import paho.mqtt.client as mqtt
import logging
from keyboard import Keyboard
import threading
import requests

mqtt_topic = "totalcontrolx"

class ThreadedLCD():
    def __init__(self):
        self.lock = threading.RLock()
        self.__driver = character_lcd.Character_LCD_Mono(
            DigitalInOut(board.D22),
            DigitalInOut(board.D17),
            DigitalInOut(board.D25),
            DigitalInOut(board.D24),
            DigitalInOut(board.D23),
            DigitalInOut(board.D18),
            16,
            2
        )
        self.__driver.clear()

    def print(self, message: str):
        br = message.find("\n")
        if br > 16:
            message = f"{message[:16]}\n{message[16:]}"
        
        with self.lock:
            self.__driver.clear()
            self.update(message)

    def update(self, data: str):
        with self.lock:
            self.__driver.message = data


class SpotifyUpdater(threading.Thread):
    def run():
        end_song_timer = 0

        while True:
            sleep(end_song_timer if end_song_timer < 30 else 30)


keyboard = Keyboard(9)
lcd = ThreadedLCD()

def configure_leds():
    red = DigitalInOut(board.D12)
    red.direction = Direction.OUTPUT
    red.value = 0

    yellow = DigitalInOut(board.D5)
    yellow.direction = Direction.OUTPUT
    yellow.value = 0

    green = DigitalInOut(board.D6)
    green.direction = Direction.OUTPUT
    green.value = 0

    return red, yellow, green


def remote_call_pass(mqttc, button, topic="totalcontrolx"):
    def x(action):
        lcd.print(f"{action} {button}") #transform in another decorator
        mqttc.publish(topic, payload=f"{action} {button}")
    return x

def main():
    leds = configure_leds()

    client = mqtt.Client()
    client.connect("192.168.178.20", 21883)
    client.loop_start()

    logging.info("Connected")

    keyboard.switch(0)(
    remote_call_pass(client, 0))

    keyboard.switch(1)(
    remote_call_pass(client, 1))

    keyboard.switch(2)(
    remote_call_pass(client, 2))

    keyboard.switch(3)(
    remote_call_pass(client, 3))

    keyboard.switch(4)(
    remote_call_pass(client, 4))

    keyboard.switch(5)(
    remote_call_pass(client, 5))

    keyboard.switch(6)(
    remote_call_pass(client, 6))

    keyboard.switch(7)(
    remote_call_pass(client, 7))

    @keyboard.switch(8)
    def manage_config(action):
        pass
    
    while True:
        keyboard.check_buttons()
        sleep(0.1)


if __name__ == '__main__':
    main()
