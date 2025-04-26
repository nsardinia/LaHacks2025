from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QLineEdit
from PyQt6.QtCore import Qt
import sys

class DissapearingSearchWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.toggle_var = False

        self.search = QLineEdit()
        self.search.setPlaceholderText("Type to search...")

        layout = QVBoxLayout()
        layout.addWidget(self.search)
        self.setLayout(layout)

        # Set focus policy so it can receive key events
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def showBar(self):
            self.show()

    def hideBar(self):
            self.hide()
"""
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.toggle_var = not self.toggle_var
            if self.toggle_var:
                self.hide()
            else:
                self.show()
        else:
            super().keyPressEvent(event)
"""

    