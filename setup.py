from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()

setup(
    name = 'image_scraper',
    version = 'v0.1.0',
    packages = find_packages(),
    install_requires = parse_requirements('requirements.txt'),
    extras_require = {
        'dev': parse_requirements('dev-requirements.txt')
    },
    entry_points = {
        'console_scripts': [
            'image-scraper=image_scraper.main:main',
        ]
    }
)