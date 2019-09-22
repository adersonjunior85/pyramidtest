from setuptools import setup
requires = [
    'pyramid',
    'pyramid_chameleon',
    'pymongo',
    'waitress',
]
setup(
    name='apptest',
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = apptest:main'
        ],
    }
)
