import sys
import os
import subprocess
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from circular_progress import CircularProgress
from ui_typewriter import Ui_TypeWriter
from ui_splash_screen import Ui_SplashScreen

counter = 0

class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # create splash screen
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)
        self.ui.fontSelected.setText("Font Selected: Free Mono")

        # configure circular progress
        self.progress = CircularProgress()
        self.progress.width = 270
        self.progress.height = 270
        self.progress.value = 0
        self.progress.fontSize = 30
        self.progress.setFixedSize(self.progress.width, self.progress.height)
        self.progress.move(15,15)
        self.progress.addShadow(True)
        self.progress.setParent(self.ui.centralwidget)
        self.progress.show()

        # create timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

        self.show()

        # run font loader
        subprocess.Popen('../build/font-loader ../fonts/FreeMono.ttf', shell=True)

    # counter process for loading font
    def update(self):
        global counter

        self.progress.setValue(counter)

        if counter >= 100:
            self.timer.stop()
            self.main = MainWindow()
            self.main.show()
            counter = 0
            self.close()

        counter += 1

class LoadingWidget(QWidget):
    def __init__(self, fontName):
        QWidget.__init__(self)
        # create splash screen

        # configure circular progress
        self.progress = CircularProgress()
        self.progress.setWindowFlags(Qt.FramelessWindowHint)
        self.progress.setAttribute(Qt.WA_TranslucentBackground)
        self.progress.width = 270
        self.progress.height = 270
        self.progress.value = 0
        self.progress.fontSize = 30
        self.progress.setFixedSize(self.progress.width, self.progress.height)
        self.progress.move(15,15)
        self.progress.addShadow(True)
        self.progress.show()

        # create timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(25)

        self.show()

        # run font loader
        subprocess.Popen('../build/font-loader ' + fontName, shell=True)

    # counter process for loading font
    def update(self):
        global counter

        self.progress.setValue(counter)

        if counter >= 100:
            self.timer.stop()
            self.progress.close()

        counter += 1


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui = Ui_TypeWriter()
        self.ui.setupUi(self)
        self.counter = 0

        # connect navigation buttons
        self.ui.closeButton.clicked.connect(self.close)
        self.ui.minButton.clicked.connect(self.showMinimized)
        self.ui.minButton.clicked.connect(self.showMaximized)

        # connect other buttons
        self.ui.fontButton.clicked.connect(self.uploadFont)

        self.show()

    def changeValue(self, value):
        self.progress.setValue(value)

    def uploadFont(self):
        fontName = QFileDialog.getOpenFileName(QStackedWidget(), 'open file', '/home/garrett/git/font-loader/fonts', 'ttf files  (*.ttf)')

        self.progress = LoadingWidget(fontName[0])
        self.progress.setParent(self.ui.centralwidget)
        
        # load font from file
        id = QFontDatabase.addApplicationFont(str(fontName[0]))
        if id < 0: print("ERROR: failed to load Qt font")

        # update UI
        families = QFontDatabase.applicationFontFamilies(id)
        self.ui.textInput.clear()
        self.ui.textInput.setFont(QFont(families[0], 48))
        self.ui.fontLabel.setText("  " + families[0])

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()

    sys.exit(app.exec_())