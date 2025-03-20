import yaml

def get_dynamic_default_arg(config, desired_arg, dynamic_defaults):
    parameters = dynamic_defaults[desired_arg].__code__.co_varnames
    parameter_values = [config[arg] for arg in parameters]
    return dynamic_defaults[desired_arg](*parameter_values)

def build_true_configuration(args, dynamic_defaults, logger, config_filepath=None):
    # arguments defined at the command line take precedence over config file variables
    config = {}
    if config_filepath:
        config = read_config_file(config_filepath, logger)

    dict_args = vars(args)
    for arg in dict_args:
        if dict_args[arg] is not None:
            config[arg] = dict_args[arg]

    # handle for dynamic defaults if no value is set
    for arg in dynamic_defaults:
        if not config.get(arg):
            config[arg] = get_dynamic_default_arg(config, arg)

    return config

def strip_sensitive_arguments(config, sensitive_args):
    return {k: v for k, v in config.items() if k not in sensitive_args}

def guarantee_requirements_met(config, logger, required_args, special_requirements):
    # config is the config object after assigning arg values to the config file values

    # first iterate over required arguments
    for argument in required_args:
        if not config.get(argument):
            logger.error(f'\n\nRequired argument "{argument}" not found. Exiting...')
            exit(0)

    # then iterate over the special requirements
    for argument in special_requirements:
        value = config.get(argument)
        for requirement_obj in special_requirements[argument]:
            if not requirement_obj['requirement'](value):
                logger.error(f'\n\nSpecial requirement "{requirement_obj["name"]}" was not met for the argument "{argument}". Exiting...')
                exit(0)

def read_config_file(filepath, logger):
    try:
        with open(filepath, 'r') as stream:
            try:
                config = yaml.safe_load(stream)
                return config
            except yaml.YAMLError as exc:
                print(exc)
                logger.error('\n\nYAML Error. Exiting...')
                exit(0)
    except FileNotFoundError:
        logger.exception('Config file not found. Proceeding with defaults')
        return {}