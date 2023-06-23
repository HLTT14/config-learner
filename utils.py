import jsons


def beautify_json(inp):
    return jsons.dumps(inp, {'indent': 4, 'sort_keys': False})
