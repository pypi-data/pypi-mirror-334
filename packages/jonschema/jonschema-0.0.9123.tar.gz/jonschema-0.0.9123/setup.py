from setuptools import setup, find_packages

VERSION = '0.0.9123' 
DESCRIPTION = "Package de validation de toutes données ou formulaires"
LONG_DESCRIPTION = "Il s'agit d'une dependance python qui permettra de gerer la validation de toutes données ou formulaires"

# Setting up
setup(
       # the name must match the folder name 'jon'
        name="jonschema", 
        version=VERSION,
        author="BILONG NTOUBA Célestin",
        author_email="bilongntouba.celestin@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            "pytz;python_version>='2022.1'",
            "typing;python_version>='3.7.4.3'",
            "asyncio;python_version>='3.4.3'",
        ],
        
        keywords=['python', 'jon', 'schema', 'validation'],
        classifiers= [
            # "Headless CMS :: package :: Digibehive",
        ]
)