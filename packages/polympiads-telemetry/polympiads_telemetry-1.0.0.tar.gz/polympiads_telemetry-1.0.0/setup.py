
import re
import setuptools

install_requires = open("requirements.txt", "r").readlines()
packages = setuptools.find_packages(exclude=["tests"])

def read(f):
    with open(f, encoding='utf-8') as file:
        return file.read()

def read_var (file: str, var_in_regex: str):
    return re.search(f"{var_in_regex} = (.*)", read(file)).group(1)

def read_var_in_conf (var: str):
    return read_var("telemetry/config.py", var)
def read_major ():
    return int( read_var_in_conf("TELEMETRY_VERSION_MAJOR") )
def read_minor ():
    return int( read_var_in_conf("TELEMETRY_VERSION_MINOR") )
def read_patch ():
    return int( read_var_in_conf("TELEMETRY_VERSION_PATCH") )

def read_version ():
    return f"{read_major()}.{read_minor()}.{read_patch()}"

setuptools.setup(
    name = "polympiads_telemetry",
    version = read_version(),
    description = "Polympiads Framework for Telemetry",
    long_description = read("README.md"),
    long_description_content_type='text/markdown',
    url = "https://polympiads.github.io/telemetry",
    install_requires = install_requires,
    author = "Polympiads",
    license = "MIT",
    packages = packages,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: OpenTelemetry',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    project_urls={
        'About Polympiads': 'https://polympiads.ch/',
        'Source': 'https://github.com/polympiads/telemetry'
    }
)
