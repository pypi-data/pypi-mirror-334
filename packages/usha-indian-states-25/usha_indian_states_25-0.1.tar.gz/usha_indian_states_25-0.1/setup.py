from setuptools import setup, find_packages

setup(
    name="usha_indian_states_25",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["django"],
    license="MIT",
    description="A Django app that provides Indian state choices as a model and form field.",
    author="Usha",
    author_email="ushampro93441@gmail.com",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
    ],
)
