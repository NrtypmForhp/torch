from PyQt6.QtWidgets import (QFrame, QGridLayout, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class Logo(QFrame):
    def __init__(self, parent, logo_path:str):
        super().__init__(parent)
        
        # Main settings
        self.lay = QGridLayout(self)
        
        # Set up logo
        self.label_logo = QLabel(self)
        img_pixmap = QPixmap(logo_path)
        self.label_logo.setPixmap(img_pixmap)
        self.label_logo.resize(img_pixmap.width(), img_pixmap.height())
        self.lay.addWidget(self.label_logo, 0, 0, Qt.AlignmentFlag.AlignTop)