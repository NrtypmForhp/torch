from PyQt6.QtWidgets import (QFrame, QGridLayout, QComboBox, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal

class Options(QFrame):
    # Signals
    signal = pyqtSignal(str)
    def __init__(self, parent, messages:dict):
        super(self.__class__, self).__init__(parent)
        
        # Main settings
        self.lay = QGridLayout(self)
        self.messages = messages
        self.sessions = []
        
        # Session
        self.combobox_actual_session = QComboBox(self)
        self.combobox_actual_session.currentIndexChanged.connect(self.session_index_changed)
        self.lay.addWidget(self.combobox_actual_session, 0, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        
        self.button_close_actual_session = QPushButton(self, text=self.messages["close"])
        self.button_close_actual_session.clicked.connect(self.close_actual_session)
        self.lay.addWidget(self.button_close_actual_session, 0, 1, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        
        self.button_options = QPushButton(self, text=self.messages["options"])
        self.button_options.clicked.connect(lambda: self.start_session("options", True))
        self.lay.addWidget(self.button_options, 0, 2, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
    
    # Resize functions
    def resizeEvent(self, a0):
        W_width = self.width()
        W_height = self.height()
        
        try:
            self.combobox_actual_session.setFixedWidth(W_width - 300)
        except AttributeError: pass
        return super().resizeEvent(a0)
    
    # When the combobox_actual_session change index
    def session_index_changed(self) -> None:
        if len(self.sessions) == 0: return
        session_index = self.combobox_actual_session.currentIndex()
        self.signal.emit(self.sessions[session_index]["type"])
    
    # Function to close actual session
    def close_actual_session(self) -> None:
        if len(self.sessions) == 0: return
        session_index = self.combobox_actual_session.currentIndex()
        self.signal.emit("none")
        self.sessions.pop(session_index)
        self.combobox_actual_session.removeItem(session_index)
    
    # Function to start sessions
    def start_session(self, session_to_start:str, check_if_opened:bool=False) -> None:
        if check_if_opened == True:
            # Control if session is already opened
            for session in self.sessions:
                if session["type"] == session_to_start: return self.combobox_actual_session.setCurrentIndex(self.sessions.index(session))
        self.sessions.append({"type": session_to_start})
        self.combobox_actual_session.addItem(self.messages[session_to_start])
        self.combobox_actual_session.setCurrentText(self.messages[session_to_start])