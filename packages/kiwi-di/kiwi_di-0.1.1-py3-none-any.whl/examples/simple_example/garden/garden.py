from kiwi_di import component

from .flowers import Rose, Tulip


class Sunflower:
    pass


@component
class Garden:

    def __init__(self, rose: Rose, tulip: Tulip, sunflower: Sunflower = Sunflower()):
        self.rose = rose
        self.tulip = tulip
        self.sunflower = sunflower
