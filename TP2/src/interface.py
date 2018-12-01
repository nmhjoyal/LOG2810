import sys
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, Qt, QtWidgets
from PyQt5 import sip
from automate import Automate



class Interface(QtWidgets.QMainWindow):

        def __init__(self):
                super().__init__()
                self.title = 'INTERFACE'
                self.left = 10
                self.top = 10
                self.width = 450
                self.height = 285
                self.initUI()
                self.i=0

        def initUI(self):
                self.setWindowTitle(self.title)
                self.setGeometry(self.left, self.top, self.width, self.height)

                #LABEL 1 // Mot proposé
                self.l1 = QtWidgets.QLabel(self)
                self.l1.setText("Mots proposés:")
                self.l1.move(20,5)
                self.l1.resize(200,30)

                #TEXTBOX 1 // Liste de mots dans le lexiques
                self.textarea = MyTextEdit(self)
                self.textarea.setReadOnly(True)
                self.textarea.move(20,30)
                self.textarea.resize(260,200)
                self.textarea.insertPlainText("Entrez une lettre dans la barre du bas pour obtenir des suggestions")
                self.textarea.setStyleSheet("border: 1px solid black;")

                #LABEL 2 // Entrez votre mot
                self.l2 = QtWidgets.QLabel(self)
                self.l2.setText("Entrez votre mot:")
                self.l2.move(20,230)
                self.l2.resize(200,30)

                #LINE BOX //Input mot à rechercher
                self.textbox = QtWidgets.QLineEdit(self)
                self.textbox.move(20, 255)
                self.textbox.resize(160,20)
                self.textbox.setStyleSheet("border: 1px solid red;")

                self.textbox.textChanged.connect(self.textarea.on_change)

                #LABEL 3 // fichier choisi
                self.l3 = QtWidgets.QLabel(self)
                self.l3.setText("Lexique:")
                self.l3.move(290,155)
                self.l3.resize(200,30)

                #BARRE D'AFFICHAGE DU FICHIER
                self.filename = QtWidgets.QLineEdit(self)
                self.filename.move(290, 180)
                self.filename.resize(150,20)
                self.filename.setStyleSheet("background-color:lightGray; color: black;")
                self.filename.setDisabled(True)
                
                #BOUTON BROWSE
                self.browseButton = QtWidgets.QPushButton(self)
                self.browseButton.setText("Choisir lexique")
                self.browseButton.move(290, 200)
                self.browseButton.resize(150,30)
                self.browseButton.clicked.connect(self.handleBrowseButton)

                #DIALOGUE D'ERREUR
                self.error_dialog = QtWidgets.QErrorMessage()

                

        def handleBrowseButton(self):
                self.filePath = QtWidgets.QFileDialog.getOpenFileName(self, "Selectionnez le lexique",)
                self.splitPath = self.filePath[0].split('/')
                self.chosenFile = self.splitPath[len(self.splitPath) - 1]

                self.filename.setText(self.chosenFile)
                try:
                        self.automate = Automate(self.chosenFile)
                        self.filename.setText(self.chosenFile)
                except  TypeError:
                        self.error_dialog.showMessage("TypeERROR Le fichier choisi n'a pas pu être ouvert, choisissez un autre (.TXT).")
                except  IOError:
                        self.error_dialog.showMessage("IOError Le fichier choisi n'a pas pu être ouvert, choisissez un autre (.TXT).")
                

                
                

class MyTextEdit(QtWidgets.QTextEdit):
        def __init__(self, parent):
                if not isinstance(parent, QtWidgets.QMainWindow):
                        raise TypeError('parent must be a MainWindow')
                super(MyTextEdit, self).__init__(parent)

        @QtCore.pyqtSlot(str)
        def on_change(self, message):
                self.clear()
                if len(message) == 0:
                        self.insertPlainText("Entrez une lettre dans la barre du bas pour obtenir des suggestions")
                else:
                        try:
                                lexique = self.parent().automate.findWords(message)
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
                        except AttributeError:
                                self.insertPlainText("ERREUR : Le fichier choisi n'est pas un lexique, en choisir un autre.")
                        


if __name__ == '__main__':


        app = QtWidgets.QApplication(sys.argv)
        ex = Interface()
        ex.show()
        app.exec_()
