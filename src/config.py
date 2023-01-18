import ujson


class Config:
    def __init__(self, file_path):
        with open(file_path, 'r') as config_file:
            self.config = ujson.loads(config_file.read())

    def get(self, key: str):
        config = self.config

        for k in key.split('.'):
            if k not in config:
                raise Exception(f'Unknown config value {key}')

            config = config[k]

        if type(config) is dict:
            raise Exception("Config item is not a value")

        return config
