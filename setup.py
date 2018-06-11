#!/usr/bin/env python
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

install_requires = [
    'sense-hat',
    'rtimulib',
]

tests_require = [
    'pytest',
    'sense-emu',
    'pygobject'
]

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    long_description = '\n' + f.read()

about = {}
with open(os.path.join(here, 'pictactoe/__version__.py')) as f:
    exec(f.read(), about)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')
        
        sys.exit()


setup(
    name='pictactoe',
    version=about['__version__'],
    description='TicTacToe for the Sense Hat, playable on LAN',
    long_description=long_description,
    author='Bruno Inec'
    author_email='brunoinec@gmail.com',
    url='https://github.com/Sweenu/pictactoe',
    packages=find_packages(exclude=['tests']),
    entry_points={'console_scripts': ['pictactoe = pictactoe.__main__:main']},
    python_requires='>=3.5.0',
    install_requires=install_requires,
    tests_require=tests_require,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Games/Entertainment',
    ],
    cmdclass={'upload': UploadCommand},
)
