from setuptools import setup, find_packages

requirements = []
build_requirements = requirements + ['build', 'twine']
test_requirements = requirements + ['flake8', 'coverage', 'tox', 'mypy']    # 'mypy',
dev_requirements = test_requirements + build_requirements + []

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='sat_config_reader',
    version='0.0.1',

    author="Markus",
    author_email="markus2110@gmail.com",
    description="""Package to read config files""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["config", "reader", "ini files"],
    url="https://gitlab.com/markus2110-public/python/packages/config-reader",

    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'build': build_requirements,
        'test': test_requirements,
        'dev': dev_requirements,
    },

    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Utilities"
    ],
    python_requires='>=3.9,<3.13'
)
