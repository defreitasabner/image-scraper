from setuptools import setup, find_packages
import json

def parse_pipfile_lock(filename, dev = False):
    with open(filename, 'r') as file:
        lock_data = json.load(file)
    dependencies = []
    dep_type = 'develop' if dev else 'default'
    for package, details in lock_data[dep_type].items():
        if 'version' in details:
            dependencies.append(f"{package}{details['version']}")
        elif 'git' in details:
            dependencies.append(f"{package} @ git+{details['git']}@{details['ref']}")
        elif 'path' in details:
            dependencies.append(f"{package} @ file://{details['path']}")
    return dependencies

setup(
    name = 'image_scraper',
    version = 'v0.1.0',
    author = 'Abner Freitas',
    author_email = 'defreitasabner@gmail.com',
    packages = find_packages(),
    install_requires = parse_pipfile_lock('Pipfile.lock'),
    extras_require = {
        'dev': parse_pipfile_lock('Pipfile.lock', dev = True)
    },
    entry_points = {
        'console_scripts': [
            'image-scraper=image_scraper.main:main',
        ]
    }
)