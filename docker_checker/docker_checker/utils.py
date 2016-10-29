import ConfigParser
import os


def read_config_from_argv(argv):
    """
    Retrieve config from config file passed in from argv
    """
    if len(argv) != 2:
        print 'Usage: {} CONFIG_FILE'.format(argv[0])
        return None

    # read from config
    config_file = argv[1]
    if not os.path.exists(config_file):
        print 'Config file {} not found'.format(config_file)
        return None

    config = ConfigParser.ConfigParser()
    config.read(config_file)

    return config
