from enum import IntFlag, auto


class OSI(IntFlag):
    NONE = 0
    PHYSICAL = auto()
    DATA_LINK = auto()
    NETWORK = auto()
    TRANSPORT = auto()
    SESSION = auto()
    PRESENTATION = auto()
    APPLICATION = auto()

    def __str__(self):
        return self.name

    def __sub__(self, other):
        return self.__class__(super(OSI, self).__sub__(other))

    def __add__(self, other):
        return self.__class__(super(OSI, self).__sub__(other))
