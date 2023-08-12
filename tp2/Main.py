import sys
import json
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit
from PyQt5.QtCore import QRect, Qt, QSize, QPoint, pyqtSignal
from PyQt5.QtGui import QFont, QPainter, QColor, QBrush, QPen, QPainterPath
from Reconnaisseur import *
from typing import List, Tuple
from DTW import *
from Dictionnaire import *

class Key(QWidget):

    def __init__(self, symbol, x, y, width, height, spacing):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.spacing = spacing
        self.point = QPoint(x, y)
        self.size = QSize(width, height)
        self.rect = QRect(self.point, self.size)

    def isOver(self, pos):
        return self.rect.contains(pos)


class KeyboardWidget(QWidget):

    newLetter = pyqtSignal(str)
    newWord = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_keyboard_layout()
        self.pressed_key = None
        self.traces = []
        self.motsToReco = []
        self.dictionnaire = Dictionnaire()
        for mot in self.dictionnaire.mots:
            mot.template = self.wordToStroke(mot.mot, 50)
            print(mot.mot, mot.template)

        
    def load_keyboard_layout(self):
        with open('c:/Users/Flore/OneDrive/Bureau/MasterInfo/IIHM/tp2/keyboard_layout.json', 'r') as f:
            data = json.load(f)
            self.key_width = data['keyWidth']
            self.key_height = data['keyHeight']
            self.key_spacing = data['keySpacing']
            self.nb_reco = data['nbReco']
            self.keys = []
            for key_data in data['keys']:
                symbol = key_data['symbol']
                x = key_data['x'] * (self.key_width + self.key_spacing)
                y = key_data['y'] * (self.key_height + self.key_spacing)
                width = key_data['width'] * self.key_width + (key_data['width'] - 1) * self.key_spacing
                height = self.key_height
                spacing = self.key_spacing
                self.keys.append(Key(symbol, x, y, width, height, spacing))
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(QFont('Arial', self.key_height // 2))
        
        for key in self.keys:
            # painter.setPen(Qt.black)
            painter.setPen(Qt.white)
            painter.drawRect(key.rect)
            if key == self.pressed_key:
                painter.fillRect(key.rect, QBrush(QColor('#00FF00')))
            elif key.isOver(self.mapFromGlobal(QtGui.QCursor.pos())):
                painter.fillRect(key.rect, QBrush(QColor('#080808')))
            else:
                painter.fillRect(key.rect, QBrush(QColor('#808080')))
            painter.drawText(key.rect, Qt.AlignCenter, key.symbol)
            self.update()

        for i in range(len(self.traces)-1):
            painter.setPen(QPen(Qt.black, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.setOpacity(0.1)
            painter.drawLine(self.traces[i][0], self.traces[i][1], self.traces[i+1][0], self.traces[i+1][1])
            self.update()
        
        resampled_stroke = []
        if len(self.traces) > 0:
            resampled_stroke = resample(self.traces, 50)

        for i in range(len(resampled_stroke)-1):
            painter.setPen(QPen(Qt.red, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.setOpacity(1)
            # painter.drawLine(resampled_stroke[i][0], resampled_stroke[i][1], resampled_stroke[i+1][0], resampled_stroke[i+1][1])
            # On dessine les points de la trace
            painter.drawPoint(resampled_stroke[i][0], resampled_stroke[i][1])
            self.update()
   
    def sizeHint(self):
        max_x = max(key.rect.right() for key in self.keys)
        max_y = max(key.rect.bottom() for key in self.keys)
        return QSize(max_x+self.key_spacing, max_y+self.key_spacing)
    
    def mousePressEvent(self, event):
        self.traces = []
        for key in self.keys:
            if key.isOver(event.pos()):
                self.pressed_key = key
                self.update()
                break

    def mouseReleaseEvent(self, event):
        if self.pressed_key.isOver(event.pos()) and self.pressed_key:
            self.newLetter.emit(self.pressed_key.symbol)
        self.findWordsToReco(self.traces, self.nb_reco, self.pressed_key.symbol)
        self.pressed_key = None
        self.update()

    def mouseMoveEvent(self, event):
        self.traces.append((event.pos().x(), event.pos().y()))
        self.update()

    def wordToStroke(self, word:str, d:int):
        # Obtenir la position des touches correspondant aux caractères du mot
        keys_pos = []
        for char in word:
            for key in self.keys:
                if key.symbol == char:
                    keys_pos.append((key.rect.center().x(), key.rect.center().y()))
                    break
        
        # On ajoute des points intermédiaires pour lisser le tracé
        # for i in range(len(keys_pos)-1):
        #     keys_pos += self.points_intermediaires(keys_pos[i], keys_pos[i+1], d)
        
        print(keys_pos)
        # Re-échantillonner le tracé
        return resample(keys_pos, d)
    
    def findWordsToReco(self, stroke:List[Tuple[int, int]], nb_reco:int, firstLetter: str):
        # Récupérer les mots du dictionnaire
        dictionnaire = Dictionnaire()
        self.motsToReco = []

        for mot in dictionnaire.mots :
            if mot.mot[0] == firstLetter :
                dtwDist = DTWDistance(stroke, mot.template)
                #print(mot.mot, dtwDist)
                for motToReco in self.motsToReco :
                    if dtwDist < motToReco[1] :
                        self.motsToReco.remove(motToReco)
                        self.motsToReco.append((mot, dtwDist))
                        break
                if len(self.motsToReco) < nb_reco :
                    self.motsToReco.append((mot, dtwDist))
                else :
                    self.motsToReco.sort(key=lambda x: x[1], reverse=True)
                    self.motsToReco.pop()
        for motToReco in self.motsToReco :
            print(motToReco[0].mot, motToReco[1])
            # self.motsToReco.append(Key(motToReco[0].mot, motToReco[0].mot, QRect(0, 0, 0, 0)))
            self.update()

    def points_intermediaires(self, p1, p2, n):
        # Calculer la différence entre les coordonnées de chaque point
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        # Calculer les pas nécessaires pour atteindre chaque point intermédiaire
        step_x = dx / n
        step_y = dy / n

        # Créer une liste pour stocker les points intermédiaires
        points = []

        # Ajouter chaque point intermédiaire à la liste
        for i in range(n):
            x = p1[0] + (step_x * i)
            y = p1[1] + (step_y * i)
            points.append((x, y))

        # Ajouter le point final à la liste
        points.append(p2)

        # Renvoyer la liste de points intermédiaires
        return points

class Editeur(QWidget):
    # Définition de la classe de la fenêtre principale Editeur
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configuration de l'interface utilisateur
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit)

        self.keyboard_widget = KeyboardWidget()
        layout.addWidget(self.keyboard_widget)

        self.keyboard_widget.newLetter.connect(self.add_letter)
        self.keyboard_widget.newWord.connect(self.add_word)

        self.show()

    def add_letter(self, letter):
        self.line_edit.insert(letter)

    def add_word(self, word):
        self.line_edit.insert(word+" ")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editeur = Editeur()
    sys.exit(app.exec_())
