import sys
import tomllib

import requests

if __name__ == '__main__':
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
        current_version = data['poetry']['version']

    pypi_versions = requests.get('https://pypi.org/pypi/cloudeasy/json').json()['releases']['keys']
    if current_version in pypi_versions:
        print(f"{current_version} is already released and cannot be reused")
        sys.exit(1)
    else:
        print("Check passed")
        sys.exit(0)
