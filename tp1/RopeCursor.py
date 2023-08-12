from BubbleCursor import BubbleCursor
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class RopeCursor(BubbleCursor):
    def __init__(self, targets):
        BubbleCursor.__init__(self, targets)

    def paint(self, painter):
        if (self.closest != None):
            painter.setPen(QPen(self.defaultColor, 2))
            painter.drawLine(self.x, self.y, self.closest.x, self.closest.y)