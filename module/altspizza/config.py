import json
import os.path
import logger

logger = logger.Logger("AltsPizzaConfig")
class AltsPizzaConfig:
    global cnf

    def __init__(self):
        global cnf
        if os.path.isfile('data/alts.pizza.json'):
            with open('data/alts.pizza.json') as f:
                cnf = json.load(f)
        else:
            with open('data/alts.pizza.json', 'w') as f:
                default_config = {
                    'api': 'https://altspizza.herokuapp.com',
                    'reset': '',
                    'accounts': []
                }
                json.dump(default_config, f, indent=4)
                cnf = default_config

    @staticmethod
    def get_data():
        return cnf

    @staticmethod
    def get_current_reset():
        return cnf['reset']

    @staticmethod
    def get_api_base():
        return cnf['api']

    @staticmethod
    def get_accounts():
        return cnf['accounts']

    @staticmethod
    def save_config(data):
        logger.info('Saving alts.pizza.json')
        with open('data/alts.pizza.json', 'w+') as f:
            json.dump(data, f, indent=4)
