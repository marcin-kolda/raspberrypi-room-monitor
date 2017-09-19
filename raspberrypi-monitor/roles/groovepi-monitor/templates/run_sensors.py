import grovepi
import datetime
import time
import logging

from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler("{{workspace}}/logs/sensor_output.log",
                                   when="m",
                                   interval=5,
                                   backupCount=1000)
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())

sound_sensor = 0  # A0
pir_sensor = 8  # D7
grovepi.pinMode(pir_sensor, "INPUT")
grovepi.pinMode(sound_sensor, "INPUT")

while True:
    tick = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    try:
        sound_value = grovepi.analogRead(sound_sensor)
        motion_value = grovepi.digitalRead(pir_sensor)

        logger.info("%s,%s,%s" % (tick, sound_value, motion_value))
        time.sleep(0.3)

    except IOError:
        logger.info("%s,Error" % tick)
