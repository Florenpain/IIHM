from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ExpSetup(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        layout = self.init()

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle("Setup")
        self.setWindowModality(Qt.ApplicationModal)
        self.setLayout(layout)

    def init(self):

        # selection method
        hLayoutMethods = QHBoxLayout()
        hLayoutMethods.addWidget(QLabel("methods :"))
        self.methods = QComboBox()
        self.methods.addItems(["Highlight", "Bubble", "Rope"])
        hLayoutMethods.addWidget(self.methods)

        # user number
        hLayoutUserNb = QHBoxLayout()
        hLayoutUserNb.addWidget(QLabel("user number :"))
        self.userNb = QSpinBox()
        self.userNb.setValue(1)
        hLayoutUserNb.addWidget(self.userNb)

        # density
        hLayoutDensity = QHBoxLayout()
        hLayoutDensity.addWidget(QLabel("density :"))
        self.density = QComboBox()
        self.density.addItems(["30", "60", "90"])
        hLayoutDensity.addWidget(self.density)

        # Size of targets
        hLayoutTargetsSize = QHBoxLayout()
        hLayoutTargetsSize.addWidget(QLabel("nombre de tailles de cibles :"))
        self.targetSize = QComboBox()
        self.targetSize.addItems(["6", "12", "18"])
        hLayoutTargetsSize.addWidget(self.targetSize)

        # repetitions
        hLayoutRepetitions = QHBoxLayout()
        hLayoutRepetitions.addWidget(QLabel("repetitions :"))
        self.repetitions = QSpinBox()
        self.repetitions.setValue(1)
        self.repetitions.setMinimum(1)
        hLayoutRepetitions.addWidget(self.repetitions)

        # init next button
        nextButton = QPushButton("next", self)
        nextButton.clicked.connect(self.accept)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(hLayoutUserNb)
        mainLayout.addLayout(hLayoutDensity)
        mainLayout.addLayout(hLayoutMethods)
        mainLayout.addLayout(hLayoutTargetsSize)
        mainLayout.addLayout(hLayoutRepetitions)
        mainLayout.addWidget(nextButton)

        return mainLayout

    def launch(self):
        dlg = ExpSetup()
        r = dlg.exec_()
        if r:
            return dlg.getValues()
        return None

    def getValues(self):
        return self.userNb.value(), self.methods.currentText(), self.density.currentText(), self.targetSize.currentText(), self.repetitions.value()
