def increase_parameter(space, observation, parameter_name):
    parameter_value = observation[parameter_name]
    space_upper_bound = space.n - 1

    if parameter_value < space_upper_bound:
        new_value = parameter_value + 1
        is_valid = True
    else:
        new_value = parameter_value
        is_valid = False

    return parameter_name, new_value, is_valid


def decrease_parameter(space, observation, parameter_name):
    parameter_value = observation[parameter_name]
    space_lower_bound = 0

    if parameter_value > space_lower_bound:
        new_value = parameter_value - 1
        is_valid = True
    else:
        new_value = parameter_value
        is_valid = False

    return parameter_name, new_value, is_valid


def toggle_parameter(space, observation, parameter_name):
    parameter_value = observation[parameter_name]
    new_value = 1 - parameter_value
    return parameter_name, new_value, True


functions = {
    'increase': lambda space, observation, parameter: increase_parameter(space, observation, parameter),
    'decrease': lambda space, observation, parameter: decrease_parameter(space, observation, parameter),
    'toggle': lambda space, observation, parameter: toggle_parameter(space, observation, parameter)
}


def suggest_change(action, space, observation):
    parameter = action.split('__')[0]
    func_name = action.split('__')[1]
    func = functions[func_name]
    return func(space[parameter], observation, parameter)
