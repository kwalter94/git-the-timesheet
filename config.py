import configparser
import json
import os
import os.path


HOME_DIR_PATH = os.path.expanduser('~')
GIT_CONFIG_PATH = os.path.join(HOME_DIR_PATH, '.gitconfig')
APP_CONFIG_PATH = os.path.join(HOME_DIR_PATH, '.git-the-timesheet', 'config.json')

CONFIG_INDENT_LEVEL = 2

def load_config():
    def load_git_config():
        with open(GIT_CONFIG_PATH) as config_file:
            config = configparser.ConfigParser()
            config.read_file(config_file)
            return {
                'username': config['user'].get('name') or os.environ['USER'],
                'email': config['user'].get('email'),
                'repos': [
                    {
                        'path': '/sample_path',
                        'username': 'some repo specific username if any'
                    }
                ]
            }
    
    def load_app_config():
        with open(APP_CONFIG_PATH) as config_file:
            return json.loads(config_file.read())

    if os.path.exists(APP_CONFIG_PATH):
        return load_app_config()

    return load_git_config()

def save_config(config):
    with open(APP_CONFIG_PATH, 'w') as config_file:
        config_file.write(json.dumps(config, indent=CONFIG_INDENT_LEVEL))
