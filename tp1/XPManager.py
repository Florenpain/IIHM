from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from BubbleWidget import *
from NormalWidget import *


class XPManager():
    def __init__(self, userNb, method, density, targetSize, repetitions):
        self.targetSize = []
        self.density = []
        self.currentUserNb = userNb
        self.method = method
        self.currentDensity = density
        self.currentTargetSize = targetSize
        self.currentRepetitions = repetitions

    def choiceCursor(self):
        fileBubble = "assets/bubble" + self.currentDensity + "x" + self.currentTargetSize + ".csv"
        fileSelectedTarget = "assets/selected" + self.currentDensity + "x" + self.currentTargetSize + ".csv"
        if self.method == "Highlight":
            return NormalWidget(fileBubble, fileSelectedTarget, self.currentUserNb, self.method, self.currentDensity,
                                self.currentTargetSize)
        elif self.method == "Rope":
            return BubbleWidget("Rope", fileBubble, fileSelectedTarget, self.currentUserNb, self.method,
                                self.currentDensity, self.currentTargetSize)
        else:
            return BubbleWidget("Bubble", fileBubble, fileSelectedTarget, self.currentUserNb, self.method,
                                self.currentDensity, self.currentTargetSize)
