from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal

class SOptions(QFrame):
    # Signals
    signal_start_login_thread = pyqtSignal(str, str, str, bool)
    def __init__(self, parent, messages:dict, settings:dict):
        super(self.__class__, self).__init__(parent)
        
        # Main settings
        self.lay = QVBoxLayout(self)
        self.messages = messages
        self.settings = settings
        
        # Title
        self.label_options = QLabel(self, text=self.messages["options"])
        self.label_options.setAccessibleName("session_title")
        self.lay.addWidget(self.label_options, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.lineedit_database_string = QLineEdit(self)
        self.lineedit_database_string.setPlaceholderText(self.messages["database_options_placeholder"])
        self.lineedit_database_string.setText(self.settings["database_connection_string"])
        self.lay.addWidget(self.lineedit_database_string, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.lineedit_username = QLineEdit(self)
        self.lineedit_username.setPlaceholderText(self.messages["username_options_placeholder"])
        if self.settings["username"] != "-": self.lineedit_username.setText(self.settings["username"])
        self.lay.addWidget(self.lineedit_username, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.lineedit_password = QLineEdit(self)
        self.lineedit_password.setPlaceholderText(self.messages["password_options_placeholder"])
        self.lineedit_password.setEchoMode(QLineEdit.EchoMode.Password)
        if self.settings["password"] != "-": self.lineedit_password.setText(self.settings["password"])
        self.lay.addWidget(self.lineedit_password, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.checkbox_autologin = QCheckBox(self, text=self.messages["auto_login"])
        self.lay.addWidget(self.checkbox_autologin, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.button_save_options = QPushButton(self, text=self.messages["save_options"])
        self.button_save_options.clicked.connect(lambda: self.start_login_thread(self.lineedit_database_string.text(), self.lineedit_username.text(), self.lineedit_password.text()))
        self.lay.addWidget(self.button_save_options, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.label_response = QLabel(self)
        self.lay.addWidget(self.label_response, alignment=Qt.AlignmentFlag.AlignCenter)
    
    # Resize functions
    def resizeEvent(self, a0):
        W_width = self.width()
        W_height = self.height()
        
        try:
            # Options
            self.lineedit_database_string.setFixedWidth(W_width - 50)
            self.lineedit_username.setFixedWidth(W_width - 50)
            self.lineedit_password.setFixedWidth(W_width - 50)
        except AttributeError: pass
        return super().resizeEvent(a0)
    
    # Start login thread
    def start_login_thread(self, mongodb_st:str, username:str, password:str):
        if mongodb_st == "" or username == "" or password == "":
            err_msg = QMessageBox(self)
            err_msg.setWindowTitle(self.messages["warning"])
            err_msg.setText(self.messages["options_field_warning_message"])
            return err_msg.exec()
        self.signal_start_login_thread.emit(mongodb_st, username, password, self.checkbox_autologin.isChecked())
    
    # Login status set
    def login_status_set(self, status:str) -> None:
        self.label_response.setText(status)