from setuptools import find_packages, setup
from typing import List



HYPHE_E_D="-e ."
def get_requirements(file_path:str)->list[str] :
    '''
    this function will return the list of requirements
    '''
    requirement = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]
        if HYPHE_E_D in requirements: 
            requirements.remove(HYPHE_E_D)
    return requirements
setup(
    name='mlproject',
    version='0.0.1',
    author='Othmane',
    author_email='preureoth@gmail.com',
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt')
)