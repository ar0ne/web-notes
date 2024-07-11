import os.path

from setuptools import find_packages, setup

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
VERSION = "0.0.1"


def get_requirements(env):
    with open(f"requirements/{env}.txt") as fp:
        return [x.strip() for x in fp.read().split("\n") if not x.startswith("#")]


install_requires = get_requirements("base")
dev_requires = get_requirements("dev")

with open(os.path.join(ROOT_PATH, "readme.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dispatch",
    version=VERSION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Netflix, Inc.",
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.12",
    install_requires=install_requires,
    extras_require={"dev": dev_requires},
    zip_safe=False,
    include_package_data=True,
)
