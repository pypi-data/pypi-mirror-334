from setuptools import setup, find_packages
import os

def parse_requirements(filename):
    """Load requirements from a requirements file."""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
install_requires = parse_requirements(requirements_path)


setup(
    name="cs2ics",
    version="0.2.0",
    author="GamerNoTitle",
    author_email="GamerNoTitle@outlook.com",
    description="A tool for users to convert their course schedules to iCalendar format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GDUTMeow/cs2ics",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=install_requires,
)