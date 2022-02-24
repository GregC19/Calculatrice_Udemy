from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QSizePolicy
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6 import QtCore

# 1er arg : y, 2 arg : x, 3 et 4eme arg : taille bouton
BUTTONS = {
    "C": (1, 0, 1, 1),
    "/": (1, 3, 1, 1),
    "7": (2, 0, 1, 1),
    "8": (2, 1, 1, 1),
    "9": (2, 2, 1, 1),
    "x": (2, 3, 1, 1),
    "4": (3, 0, 1, 1),
    "5": (3, 1, 1, 1),
    "6": (3, 2, 1, 1),
    "-": (3, 3, 1, 1),
    "1": (4, 0, 1, 1),
    "2": (4, 1, 1, 1),
    "3": (4, 2, 1, 1),
    "+": (4, 3, 1, 1),
    "0": (5, 0, 1, 1),
    ".": (5, 2, 1, 1),
    "=": (5, 3, 1, 1)
}
OPERATIONS = ["+", "-", "/", "x"]

class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculatrice")
        self.setStyleSheet("""
            background-color: rgb(20,20,20);
            color: rgb(220,220,220);
            font-size: 18 px;
        """)
        self.buttons = {} # Dictionnaire qui contient les boutons

        self.main_layout = QGridLayout(self)
        self.main_layout.setSpacing(0) # Enloève les espaces entre les boutons
        self.main_layout.setContentsMargins(0,0,0,0) # Enlève les marges

        self.le_result = QLineEdit("0") #le = ligne_edit
        self.le_result.setMinimumHeight(50)
        self.le_result.setAlignment(QtCore.Qt.AlignRight) # Pour aligner le text à droite
        self.le_result.setEnabled(False)
        self.le_result.setStyleSheet("""
            border: none;
            border-bottom: 2px solid rgb(30,30,30);
            padding: 0 8px;
            font-size: 24px;
            font-weight: bold;
        """)
        self.main_layout.addWidget(self.le_result, 0, 0, 1, 4)

        for button_text, button_position in BUTTONS.items():
            button = QPushButton(button_text)
            button.setMinimumSize(48,48)
            button.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding) # Permet de définir ce qui se passe pour la forme des boutons quand on modifie la taille de fenêtre, deux arguments : longueur et largeur
            self.main_layout.addWidget(button, *button_position) # * : unpacking, évite de mettre un tuple en argument, la on prend les 4 d'un coup^
            button.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    font: bold;
                    background-color: {'#1e1e2d' if button_text in OPERATIONS else 'none'}
                }}
                QPushButton:pressed {{background-color: '#f31d58';}}
            
            """)
            if button_text not in ["=", "C"]:
                button.clicked.connect(self.number_or_operation_pressed)
            self.buttons[button_text] = button

        self.buttons["C"].clicked.connect(self.clear_result)
        self.buttons["="].clicked.connect(self.compute_result)
        self.buttons["="].setStyleSheet("background-color: #f31d58;")
        self.connect_keyboard_shortcuts()

    @property # on créé une propriété pour récupérer directement la valeur / Plus besoin de self.le_result.text juste de self.result maintenant
    def result(self):
        return self.le_result.text()

    def compute_result(self):
        try:
            #eval() # eval : permet d'évaluer une chaine de caractère comme du code python
            result = eval(self.result.replace("x","*")) # Aussi on remplace "x" par "*" pour la signe multiplé est "*" en python
        except SyntaxError:
            return

        self.le_result.setText(str(result))

    def clear_result(self):
        self.le_result.setText("0")

    def number_or_operation_pressed(self):
        if self.sender().text() in OPERATIONS: # Si l'utilisateur veut effectuer une opération
            if self.result[-1] in OPERATIONS or (self.result=="0" and self.sender().text()!="-"): # Pas deux signes opératoires de suite ni commencer par une operation (sauf pour '-' les chiffres négatifs)
                return

        #self.sender() #sender : magic, récupère le text du bouton qui a envoyé le signal
        if self.result == "0": # Si 0 est affiché dans la ligne edit, on l'efface quand on clique sur un bouton
            self.le_result.clear()

        self.le_result.setText(self.result+self.sender().text()) # On affiche dans le ligne edit la valeur déjà présente et celle du bouton qui a été utilisée

    def remove_last_character(self): # Supprime le dernier caractère si on a plus d'un caractère
        if len(self.result)>1:
            self.le_result.setText(self.result[:-1])
        else:
            self.le_result.setText("0")

    def connect_keyboard_shortcuts(self):
        for button_text, button in self.buttons.items():
            QShortcut(QKeySequence(button_text), self, button.clicked.emit) # QKeySequence : correspond au text du bouton, emit : simule le clic sur le bouton : permet de profiter directement des méthodes déjà déclarées

        QShortcut(QKeySequence("Return"), self, self.compute_result) # Dès que l'on fait entrée, on calcule le résultat
        QShortcut(QKeySequence(QtCore.Qt.Key_Backspace), self, self.remove_last_character) # On efface avec la touche backspace


app = QApplication()
win = Calculator()
win.show()
app.exec_()