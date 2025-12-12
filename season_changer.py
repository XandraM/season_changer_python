import tuke_openlab
from threading import Thread
from tuke_openlab.lights import Color
import time

from seasons import *

env = tuke_openlab.simulation_env("am720fg")
# env= tuke_openlab.production_env()
openlab = tuke_openlab.Controller(env)

# Premenná bude pripojená na moods.lights_enabled
import seasons


def stop_all():
    seasons._enabled = False
    openlab.lights.turn_off()


def start_effect(effect_func):
    seasons._enabled = False
    time.sleep(0.1)             # krátke čakanie, aby sa vlákna stihli ukončiť
    seasons._enabled = True
    Thread(target=effect_func, args=(openlab, lambda: seasons._enabled)).start()


def on_speech(text: str):
    text = text.lower()

    if text in ["stop", "koniec"]:
        send_event("koniec")
        stop_all()
        return

    if text == "jar":
        send_event("jar")
        start_effect(run_spring_pulse)

    elif text == "leto":
        send_event("leto")
        start_effect(run_summer_pulse)

    elif text == "jeseň" or text == "jesen":
        send_event("jesen")
        start_effect(run_autumn_pulse)

    elif text == "zima":
        send_event("zima")
        start_effect(run_winter_pulse)

# env.mqtt.publish("openlab/audio", {"say": "Vyber si ročné obdobie"})
env.mqtt.subscribe_to("openlab/voice/recognition", on_speech)

openlab.voice_recognition.on_recognized(on_speech)

def send_event(value=None):
    env.mqtt.publish("openlab/weather_changer", {"value": value})

# screen ?????? idk
# env.mqtt.publish("openlab/screen/1/https://xandram.github.io/season_changer/")

while True:
    time.sleep(0.1)