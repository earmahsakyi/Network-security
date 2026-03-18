from setuptools import find_packages,setup
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path:str)-> List[str]:
    """
    This function returns the list of requirements
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines() ## read each line as requirement
        requirements = [req.replace('\n','') for req in requirements] ## removing \n from the requirements
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT) ## checking and removing the -e . from the requirements list

    return requirements


setup(
    name='Network Security',
    version='0.0.1',
    author='Armah Sakyi',
    author_email='bcsakyi2000@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('./requirements.txt'),

)
