import json
from os.path import exists


def config(environment):
    configuration = {}
    configuration.update(update_from(f'config.json'))
    configuration.update(update_from(f'config.{environment}.json'))
    return configuration


def update_from(environment_config):
    if exists(environment_config):
        with open(environment_config) as fp:
            return json.load(fp)
    else:
        return {}


if __name__ == "__main__":
    print(config("live"))
