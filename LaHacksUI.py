# app.py
from PyQt6 import QtWidgets, uic
import sys
from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QLabel, QPushButton, QScrollArea, QMainWindow,
    QApplication, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
    )
from PyQt6.QtCore import QObject, Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QFont, QColor, QPen

from LaHacksWidgets import OnOffWidget
from LaHacksSearchWidget import DissapearingSearchWidget


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.controls = QWidget()  # Controls container widget.
        self.controlsLayout = QVBoxLayout()   # Controls container layout.
        # List of names, widgets are stored in a dictionary by these keys.
        widget_names = [
            "Lecture 1", "Lecture 2", "Notebook 1", "Notebook 2",
            "Notebook 3", "Notebook 4", "Notebook 5", "Notebook 6"
        ]
        self.widgets = []

        # Iterate the names, creating a new OnOffWidget for
        # each one, adding it to the layout and
        # and storing a reference in the self.widgets list
        for name in widget_names:
            item = OnOffWidget(name)
            self.controlsLayout.addWidget(item)
            self.widgets.append(item)

        spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.controlsLayout.addItem(spacer)
        self.controls.setLayout(self.controlsLayout)

        # Scroll Area Properties.
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.controls)

        # Add the items to VBoxLayout (applied to container widget)
        # which encompasses the whole window.
        container = QWidget()
        containerLayout = QVBoxLayout()

        #Add searchbar widget
        self.searchbar = DissapearingSearchWidget()
        containerLayout.addWidget(self.searchbar)

        containerLayout.addWidget(self.scroll)

        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        self.setGeometry(600, 100, 800, 600)
        self.setWindowTitle('Control Panel')
    
    def keyPressEvent(self, event):
        if event.text().isalnum():
            self.searchbar.showBar()
        elif event.key() == Qt.Key.Key_Escape:
            self.searchbar.hideBar()
        else:
            super().keyPressEvent(event)

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())