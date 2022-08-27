import json
import os.path


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
                    'accounts': []
                }
                json.dump(default_config, f, indent=4)
                cnf = default_config

    @staticmethod
    def getAPIBase():
        return cnf['api']

    @staticmethod
    def getAccounts():
        return cnf['accounts']