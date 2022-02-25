from json import load
from logging import error

def getConfiguration(config_name):
    with open('config.json') as config_file:
        configuration = load(config_file)
        try:
            return configuration[config_name]
        except KeyError:
            error("Unknown configuration key: " + config_name)
            return None
