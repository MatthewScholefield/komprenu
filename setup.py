from setuptools import setup

setup(
    name='komprenu',
    version='0.1.3',
    description='A text generation library',
    url='http://github.com/MatthewScholefield/komprenu',
    author='Matthew Scholefield',
    author_email='matthew331199@gmail.com',
    license='MIT',
    install_requires=[
        'bitarray',
        'prettyparse',
        'simplejson',
        'tqdm'
    ],
    packages=[
        'komprenu'
    ],
    entry_points={
        'console_scripts': [
            'komprenu-train=komprenu.scripts.train:main',
            'komprenu-train-markov=komprenu.scripts.train_markov:main'
        ]
    },
    zip_safe=True
)
