import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from BubbleWidget import BubbleWidget
from NormalWidget import NormalWidget
from ExpSetup import ExpSetup
from tp1.XPManager import XPManager


def main(args):
    application = QApplication(sys.argv)

    # Pour tester la 7e etape du tp1, utiliser le NormalWidget
    # widget = NormalWidget()
    # widget = BubbleWidget()

    mainWindow = QMainWindow()
    mainWindow.setWindowTitle("Bubble cursor")
    mainWindow.resize(1024, 800)
    # mainWindow.setCentralWidget(widget)

    mainWindow.dialog = ExpSetup()
    userNb, method, density, targetSize, repetitions = mainWindow.dialog.launch()
    manager = XPManager(userNb, method, density, targetSize, repetitions)
    mainWindow.setCentralWidget(manager.choiceCursor())

    mainWindow.show()
    sys.exit(application.exec_())


if __name__ == "__main__":
    main(sys.argv)

