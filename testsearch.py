from PyQt6 import QtWidgets 
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLineEdit, 
                            QVBoxLayout, QWidget, QLabel, QListWidget)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QKeyEvent
import sys

class SearchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Create search bar (initially hidden)
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Type to search...")
        
        container = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.search_bar)

        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        self.setGeometry(600, 100, 800, 600)
        self.setWindowTitle('Search Bar')
#       self.search_bar.hide()
#       self.search_bar.setClearButtonEnabled(True)
        
    
app = QtWidgets.QApplication(sys.argv)
w = SearchWindow()
w.show()
sys.exit(app.exec())
