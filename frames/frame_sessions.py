from PyQt6.QtWidgets import (QFrame, QGridLayout, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal
# Sessions frames
from frames.sessions.options import SOptions
from frames.sessions.goods import SGoods

class Sessions(QFrame):
    # Signals
    signal_start_login_thread = pyqtSignal(str, str, str, bool)
    def __init__(self, parent, messages:dict, options_dict:dict, goods_dict:dict):
        super(self.__class__, self).__init__(parent)
        
        # Main settings
        self.lay = QGridLayout(self)
        self.messages = messages
        
        # Options Session
        self.scrollarea_sessions_options = QScrollArea(self)
        
        self.frame_sessions_options = SOptions(self , options_dict["messages"], options_dict["settings"])
        self.lay.addWidget(self.frame_sessions_options, 0, 0, Qt.AlignmentFlag.AlignTop)
        
        self.scrollarea_sessions_options.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollarea_sessions_options.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollarea_sessions_options.setWidgetResizable(True)
        self.scrollarea_sessions_options.setWidget(self.frame_sessions_options)
        self.scrollarea_sessions_options.hide()
        
        # Goods Session
        self.scrollarea_sessions_goods = QScrollArea(self)
        
        self.frame_sessions_goods = SGoods(self, goods_dict["messages"])
        self.lay.addWidget(self.frame_sessions_goods, 0, 0, Qt.AlignmentFlag.AlignTop)
        
        self.scrollarea_sessions_goods.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollarea_sessions_goods.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollarea_sessions_goods.setWidgetResizable(True)
        self.scrollarea_sessions_goods.setWidget(self.frame_sessions_goods)
        self.scrollarea_sessions_goods.hide()
        
        # *-*-* Signals handling *-*-*
        # Start login thread from options frame
        self.frame_sessions_options.signal_start_login_thread.connect(self.start_login_thread)
    
    # Resize functions
    def resizeEvent(self, a0):
        W_width = self.width()
        W_height = self.height()
        
        try:
            # Options Session
            self.scrollarea_sessions_options.setFixedSize(W_width, W_height)
            self.frame_sessions_options.setMinimumSize(W_width, W_height)
            # Goods Session
            self.scrollarea_sessions_goods.setFixedSize(W_width, W_height)
            self.frame_sessions_goods.setMinimumSize(W_width, W_height)
        except AttributeError: pass
        return super().resizeEvent(a0)
    
    # Cleaning and replacing of the sessions frame
    def replace_session_frame(self, frame:str="none") -> None:
        # Cleaning
        self.scrollarea_sessions_options.hide()
        self.scrollarea_sessions_goods.hide()
        if frame == "options": self.scrollarea_sessions_options.show()
        if frame == "goods": self.scrollarea_sessions_goods.show()
    
    # Start login thread
    def start_login_thread(self, mongodb_st:str, username:str, password:str, auto_login:bool) -> None:
        self.signal_start_login_thread.emit(mongodb_st, username, password, auto_login)
    
    # Login status connection
    def login_status(self, status:str) -> None:
        self.frame_sessions_options.login_status_set(status)
        
    # Autologin checkbox control for options frame in sessions
    def checkbox_autologin_control(self, check:bool):
        self.frame_sessions_options.checkbox_autologin.setChecked(check)