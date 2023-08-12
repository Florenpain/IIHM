from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Target import Target
import csv

from BubbleCursor import BubbleCursor
from RopeCursor import RopeCursor


class BubbleWidget(QWidget):

    def __init__(self):

        QWidget.__init__(self)
        self.targets = []

        with open('src_tp_bubble.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.targets.append(Target(int(row[0]), int(row[1]), int(row[2])))

        self.cursor = BubbleCursor(self.targets)
        # self.cursor = RopeCursor(self.targets)

        # self.cursor.randomSelector().toSelect = True

    def paintEvent(self, event):
        painter = QPainter(self)
        self.cursor.paint(painter)
        for target in self.targets:
            target.paint(painter)

    def mouseMoveEvent(self, event):
        self.cursor.move(event.x(), event.y())
        self.update()
