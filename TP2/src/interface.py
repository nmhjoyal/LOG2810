import sys
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, Qt, QtWidgets
from PyQt5 import sip
from automate import Automate
import re

charFin = [" ", ",", ":", ";", "."]

#############################################################################
## COMME IL EST IMPOSSIBLE DE REMETTRE UN FICHIER .EXE DANS NOTRE ARCHIVE, ##
# POUR QUE L'INTERFACE FONCTIONNE, INSTALLER PYQT5                          #
#############################################################################

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
                self.automate = Automate("lexique6.txt")
                self.initUI()
                self.shouldShowLabels = False

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
                self.textbox = MyLineEdit(self)
                self.textbox.move(20, 255)
                self.textbox.resize(130,20)
                self.textbox.setStyleSheet("border: 1px solid red;")

                #LABEL 3 // fichier choisi
                self.l3 = QtWidgets.QLabel(self)
                self.l3.setText("Lexique:")
                self.l3.move(290,5)
                self.l3.resize(200,30)

                #BARRE D'AFFICHAGE DU FICHIER
                self.filename = QtWidgets.QLineEdit(self)
                self.filename.move(290, 30)
                self.filename.resize(150,20)
                self.filename.setText("lexique6.txt")
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

                #LABEL 1 // Mot proposé
                self.l5 = QtWidgets.QLabel(self)
                self.l5.setText("Instructions:\n 1. Choisissez un lexique \n situé dans le même \n dossier qu'interface.py \n 2. Entrez votre mot puis \n appuyez ENTER pour \n le choisir")
                self.l5.move(290,70)
                self.l5.resize(150,130)

                f = self.l5.font()
                f.setPointSize(9)
                self.l5.setFont(f)
                
                ##CONNEXIONS
                self.browseButton.clicked.connect(self.handleBrowseButton)
                self.checkShowLabels.stateChanged.connect(self.handleLabelCheckBox)
                self.textbox.installEventFilter(self)
                self.textbox.keyPressed.connect(self.textarea.on_change)

        #Gestionnaire du bouton browse
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
        
        #Choisit s'il faut que les labels soient ajoutés ou retirés
        def handleLabelCheckBox(self):
                if self.checkShowLabels.isChecked() and self.shouldShowLabels:
                        self.showLabels()
                else:
                        self.hideLabels()

        #Affiche les labels selon l'etat courant de la machine
        def showLabels(self):
                labels = self.automate.getLabel()
                self.labelTimesUsed.setText(str(labels[0]))
                if self.automate.getLabel()[1]:
                        self.labelLastFive.setText("Oui")
                else:
                        self.labelLastFive.setText("Non")

        #Cache les labels 
        def hideLabels(self):
                self.labelTimesUsed.setText("")
                self.labelLastFive.setText("")

#Classe QLineEdit réimplémentée pour réimplémenter keyPressEvent
class MyLineEdit(QtWidgets.QLineEdit):
        keyPressed = QtCore.pyqtSignal(int)
        def keyPressEvent(self, event):
                super(MyLineEdit, self).keyPressEvent(event)
                self.keyPressed.emit(event.key())
     

#Classe QTextEdit réimplémentée pour supporter on_change
class MyTextEdit(QtWidgets.QTextEdit):
        def __init__(self, parent):
                if not isinstance(parent, QtWidgets.QMainWindow):
                        raise TypeError('parent must be a MainWindow')
                super(MyTextEdit, self).__init__(parent)

        @QtCore.pyqtSlot(int)
        def on_change(self, key):
                texte = self.parent().textbox.text()      
                mots = re.findall(r"[\w']+",texte) #OBTIENT UN TABLEAU DE TOUS LES MOTS
  
                #On vide textarea avant de réajouter tous les mots
                self.clear()
                #S'il n'y a aucune possibilité de mot, alors on affiche un message incitant à écrire
                if len(mots) == 0:
                        self.insertPlainText("Entrez une lettre dans la barre du bas pour obtenir des suggestions")
                        self.shouldShowLabels = False
                        self.parent().hideLabels()
                #il y a possibilité de mot, donc qu'il n'est pas de longueur 0, on essaie
                else:
                        try:
                                motCourant =  mots[len(mots)-1] #OBTIENT LE DERNIER MOT ENTRÉ
                                dernierChar = texte[len(texte)-1] 
                                automate = self.parent().automate
                                if key != 16777220: #Si pas enter, on n'update pas le label
                                        lexique = automate.findWordsWithoutUpdate(motCourant)
                                        if (lexique[0] == motCourant): #Si le motCourant est un mot dans le lexique, 
                                                self.parent().shouldShowLabels = True
                                                self.parent().handleLabelCheckBox()
                                        else:
                                                self.parent().shouldShowLabels = False #Pas un mot dans le lexique, donc pas d'affichage de lebals
                                else: #Si ENTER est appuyé
                                        lexique = automate.findWords(motCourant)
                                
                                #On ajoute tous les mots retrouvés dans textarea
                                for i in lexique:
                                        self.insertPlainText(i + "\n")
                                
                                #Determine si les caractères qui annoncent la fin d'un mot sont présents (" ", ",", ...)
                                if (dernierChar in charFin):
                                        #On n'affiche pas les labels car le mot n'est plus courant
                                        self.parent().shouldShowLabels = False
                                        self.clear()
                 
                                self.parent().handleLabelCheckBox()

                        except IOError:
                                self.insertPlainText("Nom de fichier erroné")
                                self.parent().hideLabels()
                        except (ValueError,IndexError):
                                self.insertPlainText("Le mot cherché n'existe pas dans ce lexique")
                                self.parent().hideLabels()
                        except AttributeError:
                                self.insertPlainText("ERREUR : Le fichier choisi n'est pas un lexique, en choisir un autre.")
                                self.parent().hideLabels()


if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        ex = Interface()
        ex.show()
        app.exec_()
