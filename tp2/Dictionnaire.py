from typing import List, Tuple
from PyQt5.QtCore import QPoint
from Main import KeyboardWidget

class Mot:
    def __init__(self, mot: str, ):
        self.mot = mot.strip().lower()
        self.template = []
    
class Dictionnaire:
    def __init__(self):
        self.mots = []
        with open("c:/Users/Flore/OneDrive/Bureau/MasterInfo/IIHM/tp2/listeMots.txt", 'r', encoding='utf-8') as f:
            for line in f:
                self.mots.append(Mot(line))