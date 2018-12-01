import sys
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, Qt, QtWidgets
from PyQt5 import sip
from automate import Automate

automate = Automate("lexique5.txt")

class Interface(QtWidgets.QMainWindow):

        def __init__(self):
                super().__init__()
                self.title = 'INTERFACE'
                self.left = 10
                self.top = 10
                self.width = 500
                self.height = 600
                self.initUI()

                self.i=0

        def initUI(self):
                self.setWindowTitle(self.title)
                self.setGeometry(self.left, self.top, self.width, self.height)

                #LABEL 1
                self.l1 = QtWidgets.QLabel(self)
                self.l1.setText("Mots proposés:")
                self.l1.move(20,0)
                self.l1.resize(200,30)

                #TEXTBOX 1
                self.textarea = MyTextEdit(self)
                self.textarea.setReadOnly(True)
                self.textarea.move(20,30)
                self.textarea.resize(260,200)
                self.textarea.setText("Entrez une lettre dans la barre du bas pour obtenir des suggestions")
          

                #LABEL 2
                self.l2 = QtWidgets.QLabel(self)
                self.l2.setText("Entrez votre mot ici:")
                self.l2.move(20,240)
                self.l2.resize(200,30)

                #LINE BOX
                self.textbox = QtWidgets.QLineEdit(self)
                self.textbox.move(20, 270)
                self.textbox.resize(260,20)
                self.textbox.setStyleSheet("border: 1px solid red;")

                self.textbox.textChanged.connect(self.textarea.on_change)
                
                #BOUTON BROWSE
                self.browseButton = QtWidgets.QPushButton(self)
                self.browseButton.setText("Browse")
                self.browseButton.move(290, 30)
                self.browseButton.clicked.connect(self.handleBrowseButton)

                #BARRE D'AFFICHAGE DU FICHIER
                self.filename = QtWidgets.QLineEdit(self)
                self.filename.move(290, 60)
                self.filename.resize(100,20)
                self.filename.setStyleSheet("border: 1px solid red;")

                #DIALOGUE D'ERREUR
                self.error_dialog = QtWidgets.QErrorMessage()

                

        def handleBrowseButton(self):
                self.filePath = QtWidgets.QFileDialog.getOpenFileName(self, "Selectionnez le lexique",)
                self.splitPath = self.filePath[0].split('/')
                self.chosenFile = self.splitPath[len(self.splitPath) - 1]

                self.filename.setText(self.chosenFile)
                try:
                        automate.createAutomate(self.chosenFile)
                        self.filename.setText(self.chosenFile)
                except  TypeError:
                        self.error_dialog.showMessage("TypeERROR Le fichier choisi n'a pas pu être ouvert, choisissez un autre (.TXT).")
                except  IOError:
                        self.error_dialog.showMessage("IOError Le fichier choisi n'a pas pu être ouvert, choisissez un autre (.TXT).")
                

                
                
#Ajout d'un slot pour recevoir l'evenement de changement
#Soit envoyée
class MyTextEdit(QtWidgets.QTextEdit):
        @QtCore.pyqtSlot(str)
        def on_change(self, message):
                self.clear()
                if len(message) == 0:
                        self.insertPlainText("Entrez une lettre dans la barre du bas pour obtenir des suggestions")
                else:
                        try:
                                lexique = automate.findWords(message)
                                for i in lexique:
                                        self.insertPlainText(i + "\n")
                        except IOError:
                                self.insertPlainText("ERREUR : Nom de fichier erroné")
                        except ValueError:
                                self.insertPlainText("ERREUR : Mot cherché n'existe pas dans ce lexique")
                        except TypeError:
                                self.insertPlainText("ERREUR : Mot cherché n'existe pas dans ce lexique")
                        except IndexError:
                                self.insertPlainText("ERREUR : Mot cherché n'existe pas dans ce lexique")

                        


if __name__ == '__main__':


        app = QtWidgets.QApplication(sys.argv)
        ex = Interface()
        ex.show()
        app.exec_()
