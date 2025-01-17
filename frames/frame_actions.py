from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal

class Actions(QFrame):
    # Insert session name and "already opened" check
    start_session_signal = pyqtSignal(str, bool)
    def __init__(self, parent, messages:dict):
        super(self.__class__, self).__init__(parent)
        
        # Main settings
        self.lay = QVBoxLayout(self)
        self.messages = messages
        
        # Goods Action
        self.button_frame_actions_goods = QPushButton(self, text=self.messages["goods"])
        self.button_frame_actions_goods.clicked.connect(lambda: self.start_session_signal.emit("goods", True))
        self.button_frame_actions_goods.hide()
        self.lay.addWidget(self.button_frame_actions_goods, alignment=Qt.AlignmentFlag.AlignCenter)
    
    # Buttons hide or show
    def hide_show_buttons(self, show:bool):
        if show == True:
            self.button_frame_actions_goods.show()
        else:
            self.button_frame_actions_goods.hide()