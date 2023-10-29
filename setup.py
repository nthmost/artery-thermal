from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # Run the spacy command after installation
        subprocess.call(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='artery-thermal',
    version='0.1',
    packages=find_packages(),
    install_requires=required,
    cmdclass={
        'install': PostInstallCommand,
    },
    description='Code for printing receipts as art on thermal printer.',
    author='Naomi Most',
    author_email='naomi@nthmost.com',
    url='https://github.com/nthmost/artery-thermal',  # replace with your repository URL
)


