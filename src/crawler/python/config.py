from configloader import ConfigLoader
import os

def load_configuration():
    config_loader = ConfigLoader()
    config_loader.update_from(obj=config_loader, yaml_env='CONFIG_FILE_PATH')
    config_loader.update_from_env_namespace('')
    return config_loader

def elasticsearch_path():
  return os.environ['ELASTICSEARCH_URL']

def logging_config_path():
    return os.environ['CONFIG_LOGGING_PATH']