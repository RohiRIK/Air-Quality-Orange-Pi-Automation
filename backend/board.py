import sys

# pylint: disable=unused-import
from adafruit_blinka.microcontroller.allwinner_h6 import pin
from adafruit_blinka.agnostic import board_id, chip_id

board_id.id = "ORANGE_PI_3_LTS"
chip_id.id = "ALLWINNER_H6"

SCL = pin.PA13
SDA = pin.PA14
