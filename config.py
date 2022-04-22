import os

import yaml


class Config:
    def __init__(self):
        # Check if is in development mode
        if os.environ.get("FLASK_ENV") == "development":
            config_path = 'configs/config_dev.yaml'
        else:
            config_path = 'configs/config.yaml'

        with open(config_path, 'r') as f:
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
    def db(self):
        return self.config['mysql']['db']

    @property
    def user(self):
        return self.config['mysql']['user']

    @property
    def password(self):
        return self.config['mysql']['password']

    @property
    def ca_path(self):
        # Return None when there's no ca path
        if 'ca_path' in self.config['mysql']:
            return self.config['mysql']['ca_path']

    @property
    def mysql_uri(self):
        return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    @property
    def mysql_connect_args(self):
        return {
            "connect_args": {
                'ssl': {'ca': self.ca_path}
            }
        }

    @property
    def cosmos_uri(self):
        return self.config['cosmos']['cosmos_uri']

    @property
    def cosmos_key(self):
        return self.config['cosmos']['cosmos_key']

    @property
    def cosmos_db(self):
        return self.config['cosmos']['cosmos_db']

    @property
    def cosmos_container(self):
        return self.config['cosmos']['cosmos_container']

    @property
    def blob_uri(self):
        return self.config['blob']['blob_uri']

    @property
    def blob_container(self):
        return self.config['blob']['blob_container']

    @property
    def blob_url(self):
        return self.blob_uri + self.blob_container + "/"
