from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import importlib

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # Check if the spacy model is already installed
        model_installed = False
        try:
            importlib.import_module("en_core_web_sm")
            model_installed = True
        except ImportError:
            pass

        # If the model is not installed, download it
        if not model_installed:
            subprocess.call(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])


with open('requirements.txt') as f:
    required = f.read().splitlines()

print(required)

setup(
    name='artery-thermal',
    version='0.1',
    packages=find_packages(),
    install_requires=required,
    cmdclass={
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'artery=artery:main',
            'generate_experience=experience_generator:main'
        ],
    },
    description='Code for printing receipts as art on thermal printer.',
    author='Naomi Most',
    author_email='naomi@nthmost.com',
    url='https://github.com/nthmost/artery-thermal',  # replace with your repository URL
)


