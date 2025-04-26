from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QHBoxLayout)


class OnOffWidget(QWidget):

    def __init__(self, name):

        super().__init__()

        self.name = name # Name of widget used for searching.
        self.is_on = False # Current state (true=ON, false=OFF)

        self.lbl = QLabel(self.name)    #  The widget label
        self.btn_on = QPushButton("On")     # The ON button
        self.btn_off = QPushButton("Off")   # The OFF button

        self.hbox = QHBoxLayout()       # A horizontal layout to encapsulate the above
        self.hbox.addWidget(self.lbl)   # Add the label to the layout
        self.hbox.addWidget(self.btn_on)    # Add the ON button to the layout
        self.hbox.addWidget(self.btn_off)   # Add the OFF button to the layout
        self.setLayout(self.hbox)

        self.btn_on.clicked.connect(self.on)   # Connect the ON button to the on_clicked method
        self.btn_off.clicked.connect(self.off)

        self.update_button_state()

    
    def off(self):
        self.is_on = False
        self.update_button_state()

    def on(self):
        self.is_on = True 
        self.update_button_state()

    def update_button_state(self):
        """
        Update the appearance of the control buttons (On/Off)
        depending on the current state.
        """
        if self.is_on == True:
            self.btn_on.setStyleSheet("background-color: #4CAF50; color: #fff;")
            self.btn_off.setStyleSheet("background-color: none; color: none;")
        else:
            self.btn_on.setStyleSheet("background-color: none; color: none;")
            self.btn_off.setStyleSheet("background-color: #D32F2F; color: #fff;")

    def show(self):
        """
        Show this widget, and all child widgets.
        """
        for w in [self, self.lbl, self.btn_on, self.btn_off]:
            w.setVisible(True)

    def hide(self):
        """
        Hide this widget, and all child widgets.
        """
        for w in [self, self.lbl, self.btn_on, self.btn_off]:
            w.setVisible(False)