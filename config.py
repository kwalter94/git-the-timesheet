import configparser
import json
import os
import os.path


HOME_DIR_PATH = os.path.expanduser('~')
GIT_CONFIG_FILE_PATH = os.path.join(HOME_DIR_PATH, '.gitconfig')
MAIN_CONFIG_FILE_PATH = os.path.join(HOME_DIR_PATH, '.git-the-timesheet', 'config.json')

class ConfigLoader:
    def __init__(self, config_file_path=MAIN_CONFIG_FILE_PATH):
        self.git_config = self.read_ini_config(GIT_CONFIG_FILE_PATH)
        self.main_config = self.read_json_config(config_file_path)

    def load(self):
        return {
            'username': self.main_config['username'] or self.git_config['name'],
            'email': self.main_config['email'] or self.git_config['email'],
            'repos': self.main_config['repos']
        }

    def read_ini_config(self, path):
        config = configparser.ConfigParser()
        config.read(path)

        return config

    def read_json_config(self, path):
        with open(path) as config_file:
            return json.load(config_file)


CONFIG_INDENT_LEVEL = 2


class ConfigWriter:
    def __init__(self, config, path=MAIN_CONFIG_FILE_PATH):
        self.config = config
        self.path = path

    def write(self):
        with open(self.path, 'w') as config_file:
            json.dump(self.config, config_file, indent=CONFIG_INDENT_LEVEL)
