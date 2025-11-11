# coding=utf-8

from os.path import dirname
from os.path import join
from urllib.parse import urljoin

from setuptools import setup
from setuptools.command.install import install

from attribute import __author__
from attribute import __author_email__
from attribute import __description__
from attribute import __project__
from attribute import __urlhome__
from attribute import __version__

__urlcode__ = __urlhome__
__urldocs__ = __urlhome__
__urlbugs__ = urljoin(__urlhome__, "issues")


def all_requirements():
    def read_requirements(path: str):
        with open(path, "r", encoding="utf-8") as rhdl:
            return rhdl.read().splitlines()

    requirements = read_requirements(join(dirname(__file__), "requirements.txt"))  # noqa:E501
    requirements.append(f"{__project__}>={__version__}")
    return requirements


class CustomInstallCommand(install):
    """Customized setuptools install command"""

    def run(self):
        install.run(self)  # Run the standard installation
        # Execute your custom code after installation


setup(
    name=f"{__project__}-attrs",
    version=__version__,
    description=__description__,
    url=__urlhome__,
    author=__author__,
    author_email=__author_email__,
    project_urls={"Source Code": __urlcode__,
                  "Bug Tracker": __urlbugs__,
                  "Documentation": __urldocs__},
    py_modules=["xkits_config_attrs"],
    install_requires=all_requirements(),
    cmdclass={
        "install": CustomInstallCommand,
    }
)
