import sys, os

class Messages(object):
    def __init__(self):
        self.main_directory = ""
        
        if getattr(sys, 'frozen', False): # If started from an executable file
            self.main_directory = os.path.dirname(sys.executable)
        elif __file__: # If started directly
            self.main_directory = os.path.dirname(__file__)
    
    # Messages loading
    def load_messages(self, file:str) -> dict:
        with open(os.path.join(self.main_directory, f"{file}.txt"), "r") as message_file:
            messages = {}
            for message in message_file:
                messages[message[:message.index(":")]] = message[message.index(":")+1:].strip()
        return messages