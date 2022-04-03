import yaml


class Config:
    def __init__(self):
        with open('configs/config.yaml', 'r') as f:
            try:
                self.config = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(exc)

    @property
    def host(self):
        return self.config['mysql']['host']

    @property
    def port(self):
        return self.config['mysql']['port']

    @property
    def user(self):
        return self.config['mysql']['user']

    @property
    def password(self):
        return self.config['mysql']['password']

    @property
    def ca_path(self):
        return self.config['mysql']['ca_path']
