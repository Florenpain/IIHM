from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from math import sqrt

class NormalCursor(QWidget):
    def __init__(self, targets):
        QWidget.__init__(self)
        self.targets = targets

    def select(self, x, y):
        for target in self.targets:
            distance = self.distance(x, y, target)
            if (distance <= 0):
                target.toSelect = True
            else:
                target.toSelect = False

    def distance(self, cursorx, cursory, target):
        x = (target.x - cursorx) ** 2
        y = (target.y - cursory) ** 2
        return sqrt(x+y) - target.size
