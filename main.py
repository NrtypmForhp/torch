from PyQt6.QtWidgets import (QWidget, QApplication, QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt, QThreadPool
from PyQt6.QtGui import QIcon
import sys
from settings.settings_functions import Settings
from messages.messages_functions import Messages
# Frames
from frames.frame_logo import Logo
from frames.frame_options import Options
from frames.frame_actions import Actions
from frames.frame_sessions import Sessions
# Threads
from threads.login import LoginThread

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Settings
        self.settings_module = Settings()
        self.settings = self.settings_module.load_settings()
        
        # Messages
        self.messages_module = Messages()
        self.messages = self.messages_module.load_messages("main")
        
        # Main settings
        self.setWindowTitle(self.messages["title"])
        self.setMinimumSize(700, 500)
        self.setWindowIcon(QIcon(self.settings_module.icon_path))
        self.lay = QGridLayout(self)
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.setSpacing(0)
        self.setStyleSheet(self.settings_module.load_stylesheet())
        
        # Main frames
        self.flogo = Logo(self, self.settings_module.logo_path)
        self.foptions = Options(self ,self.messages)
        self.factions = Actions(self, self.messages)
        self.fsessions = Sessions(self ,self.messages,
                                  {"messages": self.messages_module.load_messages("session_options"), "settings": self.settings},
                                  {"messages": self.messages_module.load_messages("session_goods"), "settings": self.settings})
        
        self.frame_logo = self.flogo
        self.lay.addWidget(self.frame_logo, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.frame_options = self.foptions
        self.lay.addWidget(self.frame_options, 0, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.frame_actions = self.factions
        self.lay.addWidget(self.frame_actions, 1, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.frame_sessions = self.fsessions
        self.lay.addWidget(self.frame_sessions, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        # *-*-* Thread handling *-*-*
        
        self.thread_pool = QThreadPool.globalInstance()
        
        # *-*-* Signals handling *-*-*
    
        # From frame options
        self.frame_options.signal.connect(self.frame_sessions.replace_session_frame)
        
        # From frame actions
        self.frame_actions.start_session_signal.connect(self.actions_sessions_handling)
        
        # From frame sessions
        # Login Thread
        self.frame_sessions.signal_start_login_thread.connect(self.start_login_thread)
        
        # Autologin handling
        
        if self.settings["username"] != "-" and self.settings["password"] != "-":
            self.frame_sessions.checkbox_autologin_control(True)
            self.start_login_thread(self.settings["database_connection_string"], self.settings["username"], self.settings["password"], True)
        else: self.frame_options.button_options.click()
    
    # Resize functions
    def resizeEvent(self, a0):
        W_width = self.width()
        W_height = self.height()
        width_op = 300
        height_op = 150
        
        try:
            self.frame_logo.setFixedSize(width_op, height_op)
            self.frame_options.setFixedSize(W_width - width_op, height_op)
            self.frame_actions.setFixedSize(width_op, W_height - height_op)
            self.frame_sessions.setFixedSize(W_width - width_op, W_height - height_op)
        except AttributeError: pass
        return super().resizeEvent(a0)
    
    # *-*-* Login *-*-*
    # Start login thread
    def start_login_thread(self, mongodb_st:str, username:str, password:str, auto_login:bool) -> None:
        self.frame_actions.hide_show_buttons(False)
        self.login_thread = LoginThread(mongodb_st, username, password, self.messages_module.load_messages("login"))
        self.login_mongodb_string = mongodb_st
        self.login_username = username
        self.login_password = password
        self.login_auto_login = auto_login
        self.login_thread.signals.login_finished_signal.connect(self.login_finished)
        self.login_thread.signals.login_status_signal.connect(self.frame_sessions.login_status)
        self.thread_pool.start(self.login_thread)
    
    # Login Signals
    def login_finished(self, response:dict) -> None:
        if response["error"] != "no":
            self.frame_actions.hide_show_buttons(False)
            err_msg = QMessageBox(self)
            err_msg.setWindowTitle(self.messages["warning"])
            err_msg.setText(response["error"])
            return err_msg.exec()
        self.frame_actions.hide_show_buttons(True)
        self.frame_options.button_close_actual_session.click()
        # Save options
        if self.login_auto_login == True: self.settings_module.save_settings(self.login_mongodb_string, self.login_username, self.login_password)
        else: self.settings_module.save_settings(self.login_mongodb_string, "-", "-")
        self.settings = {
            "database_connection_string": self.login_mongodb_string,
            "username": self.login_username,
            "password": self.login_password
        }
    
    # *-*-* Actions sessions handling *-*-*
    def actions_sessions_handling(self, session:str, check_if_opened:bool) -> None:
        self.frame_options.start_session(session, check_if_opened)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()