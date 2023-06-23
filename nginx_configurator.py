import crossplane
from jsonpath_ng.ext import parse


class NginxConfigurator:
    def __init__(self, config_file_path):
        self.payload = crossplane.parse(config_file_path, comments=True)

    def set_config_value(self, key, value):
        value = str(value)
        if '/' in key:
            key, value = self._parse_compound_config(key, value)
        jsonpath_expr = parse(f'$..*[?(@.directive == {key})].args')
        if type(value) is not list:
            value = [value]
        jsonpath_expr.update(self.payload, value)
        self._save_config()

    def _get_config_value(self, key):
        return [match.value for match in parse(f'$..*[?(@.directive == "{key}")].args').find(self.payload)][0]

    def get_config_values(self, keys):
        resp = {}
        for key in keys:
            if '/' in key:
                parameter = key.split('/')[1]
                value = self._get_config_value(key.split('/')[0])
                if parameter.isdigit():
                    final_value = value[int(parameter) - 1]
                else:
                    final_value = [p.replace(f"{parameter}=", "") for p in value if parameter in p][0]
            else:
                final_value = self._get_config_value(key)[0]

            final_value = convert_to_int_if_possible(final_value)
            resp[key] = final_value
            #print(f"get_config_values {key}: {final_value}")
        return resp

    def _save_config(self):
        for config in self.payload['config']:
            file_name = config['file']
            with open(file_name, "w") as file:
                file.write(crossplane.build(config['parsed']))

    def _parse_compound_config(self, key, value):
        parameter = key.split('/')[1]
        key = key.split('/')[0]
        old_value = self._get_config_value(key)

        # for configs that have multiple parameters without specific names
        # e.g. output_buffers 2 32k;
        if parameter.isdigit():
            new_value = old_value
            new_value[int(parameter) - 1] = value

        # for configs that have multiple parameters with specified names
        # e.g. open_file_cache max=10000 inactive=5m;
        else:
            new_value = [f'{parameter}={value}' if parameter in p else p for p in old_value]
        return key, new_value


def convert_to_int_if_possible(x):
    if x.isdigit():
        return int(x)
    else:
        return x

