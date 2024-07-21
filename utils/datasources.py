import glob


def get_datasources(path):
    datasources = [file.lstrip(path) for file in glob.glob(f'{path}/*')]
    return [''] + datasources