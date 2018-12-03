import sys
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, Qt, QtWidgets
from PyQt5 import sip
from automate import Automate



class Interface(QtWidgets.QMainWindow):

        def __init__(self):
                super().__init__()
                self.title = 'INTERFACE LEXIQUE'
                self.left = 10
                self.top = 10
                self.width = 450
                self.height = 285
                self.i=0
                self.checked = 0

                self.initUI()

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
                self.l2.setText("Écrire ici:")
                self.l2.move(20,230)
                self.l2.resize(200,30)

                #LINE BOX //Input mot à rechercher
                self.textbox = QtWidgets.QLineEdit(self)
                self.textbox.move(20, 255)
                self.textbox.resize(130,20)
                self.textbox.setStyleSheet("border: 1px solid red;")

                #LABEL 3 // fichier choisi
                self.l3 = QtWidgets.QLabel(self)
                self.l3.setText("Lexique:")
                self.l3.move(290,5)
                self.l3.resize(200,30)

                #BARRE D'AFFICHAGE DU PATH
                self.filename = QtWidgets.QLineEdit(self)
                self.filename.move(290, 30)
                self.filename.resize(150,20)
                self.filename.setStyleSheet("background-color:lightGray; color: black;")
                self.filename.setDisabled(True)
                
                #BOUTON BROWSE
                self.browseButton = QtWidgets.QPushButton(self)
                self.browseButton.setText("Choisir lexique")
                self.browseButton.move(290, 50)
                self.browseButton.resize(150,30)

                #DIALOGUE D'ERREUR
                self.error_dialog = QtWidgets.QErrorMessage()

                #LABEL 3 // LABEL LEXIQUE 1 (NB USAGES)
                self.l3 = QtWidgets.QLabel(self)
                self.l3.setText("(1)Nb usages")
                self.l3.move(155,230)
                self.l3.resize(200,30)

                #TEXTLINE LABEL 1 (NB UTILISÉ)
                self.labelTimesUsed = QtWidgets.QLineEdit(self)
                self.labelTimesUsed.move(250, 235)
                self.labelTimesUsed.resize(30,20)
                self.labelTimesUsed.setStyleSheet("background-color:lightGray; color: black;")
                self.labelTimesUsed.setDisabled(True)
                self.labelTimesUsed.setAlignment(QtCore.Qt.AlignCenter)

                #Assigner fontsize au TEXTLINE
                f = self.labelTimesUsed.font()
                f.setPointSize(10)
                self.labelTimesUsed.setFont(f)

                #LABEL 4 // LABEL LEXIQUE 2 (5 DERNIERS)
                self.l4 = QtWidgets.QLabel(self)
                self.l4.setText("(2)5 derniers?")
                self.l4.move(155,250)
                self.l4.resize(200,30)

                #TEXTLINE LABEL 2 (5 derniers mots ou non)
                self.labelLastFive = QtWidgets.QLineEdit(self)
                self.labelLastFive.move(250, 255)
                self.labelLastFive.resize(30,20)
                self.labelLastFive.setStyleSheet("background-color:lightGray; color: black;")
                self.labelLastFive.setDisabled(True)
                self.labelLastFive.setAlignment(QtCore.Qt.AlignCenter)

                #Assigner fontsize au TEXTLINE
                f = self.labelLastFive.font()
                f.setPointSize(10)
                self.labelLastFive.setFont(f)

                #CHECKBOX POUR AFFICHER LABELS
                self.checkShowLabels = QtWidgets.QCheckBox("Afficher labels", self)
                self.checkShowLabels.move(290, 255)
                self.checkShowLabels.resize(160,20)

                ##CONNEXIONS
                self.textbox.textChanged.connect(self.textarea.on_change)
                self.browseButton.clicked.connect(self.handleBrowseButton)
                self.checkShowLabels.stateChanged.connect(self.textarea.on_change)


        def handleBrowseButton(self):
                self.filePath = QtWidgets.QFileDialog.getOpenFileName(self, "Selectionnez le lexique",)
                self.splitPath = self.filePath[0].split('/')
                self.chosenFile = self.splitPath[len(self.splitPath) - 1]
                try:
                        self.automate = Automate(self.chosenFile)
                        self.filename.setText(self.chosenFile)
                except  TypeError:
                        self.error_dialog.showMessage("TypeERROR Le fichier choisi n'a pas pu être ouvert, choisissez un autre (.TXT).")
                except  IOError:
                        self.error_dialog.showMessage("IOError Le fichier choisi n'a pas pu être ouvert, choisissez un autre (.TXT).")

        def hideLabels(self):
                self.labelTimesUsed.setText("")
                self.labelLastFive.setText("")

                                
                

class MyTextEdit(QtWidgets.QTextEdit):
        def __init__(self, parent):
                if not isinstance(parent, QtWidgets.QMainWindow):
                        raise TypeError('parent must be a MainWindow')
                super(MyTextEdit, self).__init__(parent)

        @QtCore.pyqtSlot()
        def on_change(self):
                message = self.parent().textbox.text()
                
                self.clear()
                self.insertPlainText(message + "\n") ## REMOVE
                if len(message) == 0:
                        self.insertPlainText("Entrez une lettre dans la barre du bas pour obtenir des suggestions")
                        self.parent().labelTimesUsed.setText("")
                        self.parent().labelLastFive.setText("")
                else:
                        try:
                                automate = self.parent().automate
                                # lexique = automate.findWords(message)
                                lexique = automate.findWords("abces abces")
                                for i in lexique:
                                        self.insertPlainText(i + "\n")
                                if self.parent().checkShowLabels.isChecked():
                                        self.parent().labelTimesUsed.setText(str(automate.getLabel()[0]))
                                        if automate.getLabel()[1]:
                                                self.parent().labelLastFive.setText("Oui")
                                        else:
                                                self.parent().labelLastFive.setText("Non")
                                else:
                                        self.parent().hideLabels()

                        except IOError:
                                self.insertPlainText("ERREUR : Nom de fichier erroné")
                                self.parent().hideLabels()
                        except ValueError:
                                self.insertPlainText("ERREUR : Mot cherché n'existe pas dans ce lexique")
                                self.parent().hideLabels()
                        except TypeError:
                                self.insertPlainText("ERREUR : Mot cherché n'existe pas dans ce lexique")
                                self.parent().hideLabels()
                        except IndexError:
                                self.insertPlainText("ERREUR : Mot cherché n'existe pas dans ce lexique")
                                self.parent().hideLabels()
                        except AttributeError:
                                self.insertPlainText("ERREUR : Le fichier choisi n'est pas un lexique, en choisir un autre.")
                                self.parent().hideLabels()

if __name__ == '__main__':


        app = QtWidgets.QApplication(sys.argv)
        ex = Interface()
        ex.show()
        app.exec_()
