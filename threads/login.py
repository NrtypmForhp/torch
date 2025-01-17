from PyQt6.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot
import pymongo

class Signals(QObject):
    login_status_signal = pyqtSignal(str)
    login_finished_signal = pyqtSignal(dict)

# -*-* Login Thread *-*-

class LoginThread(QRunnable):
    def __init__(self, mongodb_string:str, username:str, password:str, messages:dict):
        super().__init__()
        
        # First settings
        self.mongodb_string = mongodb_string
        self.username = username
        self.password = password
        self.signals = Signals()
        self.messages = messages
    
    @pyqtSlot()
    def run(self):
        # Connection to database check
        self.signals.login_status_signal.emit(self.messages["database_connection_signal"])
        self.dbclient = pymongo.MongoClient(self.mongodb_string)
        try:
            self.dbclient.server_info()
        except:
            self.signals.login_status_signal.emit("")
            self.signals.login_finished_signal.emit({"error": self.messages["database_error"]})
            return
        
        # Username and Password check
        self.signals.login_status_signal.emit(self.messages["user_check_signal"])
        self.db = self.dbclient["torch"]
        col_users = self.db["users"]
        if col_users.count_documents({"username": self.username, "password": self.password}) == 0:
            self.signals.login_status_signal.emit("")
            self.signals.login_finished_signal.emit({"error": self.messages["user_error"]})
            return
        
        # Thread end
        self.signals.login_status_signal.emit("")
        return self.signals.login_finished_signal.emit({"error": "no"})