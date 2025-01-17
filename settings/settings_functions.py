import sys, os

class Settings(object):
    def __init__(self):
        self.main_directory = ""
        
        if getattr(sys, 'frozen', False): # If started from an executable file
            self.main_directory = os.path.dirname(sys.executable)
        elif __file__: # If started directly
            self.main_directory = os.path.dirname(__file__)

        self.img_directory = os.path.join(self.main_directory, "img")
        self.icon_path = os.path.join(self.img_directory, "Torch_icon.png")
        self.logo_path = os.path.join(self.img_directory, "Torch.png")
    
    # Settings loading function
    def load_settings(self) -> dict:
        settings_dict = {}
        if os.path.exists(os.path.join(self.main_directory, "settings.txt")) == False:
            with open(os.path.join(self.main_directory, "settings.txt"), "w") as settings_file:
                settings_file.write("database_connection_string: mongodb://localhost:27017/\n")
                settings_file.write("username: -\n")
                settings_file.write("password: -")
        with open(os.path.join(self.main_directory, "settings.txt"), "r") as settings_file:
            for line in settings_file:
                settings_dict[line[:line.index(":")].strip()] = line[line.index(":")+1:].strip()
        return settings_dict
    
    # Style loading function
    def load_stylesheet(self) -> str:
        with open(os.path.join(self.main_directory, "style.txt"), "r") as style_file:
            style = style_file.read()
            style = style.replace("check_icon_url", os.path.join(self.img_directory, "check_icon.png"))
            style = style.replace("up_arrow_url", os.path.join(self.img_directory, "up-arrow.png"))
            style = style.replace("down_arrow_url", os.path.join(self.img_directory, "down-arrow.png"))
        return style
    
    # Settings save function
    def save_settings(self, db_connection_string:str, username:str, password:str):
        with open(os.path.join(self.main_directory, "settings.txt"), "w") as settings_file:
            settings_file.write(f"database_connection_string: {db_connection_string}\n")
            settings_file.write(f"username: {username}\n")
            settings_file.write(f"password: {password}")