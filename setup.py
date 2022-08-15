from setuptools import find_packages, setup

requirements = [
    'psycopg2-binary',
    'cffi>=1.15.1,<2.0.0',
    'dbfread>=2.0.7,<3.0.0',
    'pandas>=1.4.3,<2.0.0',
    'tqdm>=4.64.0,<5.0.0',
]


setup(
    name="pyreaddbc",
    version="1.0.0",
    packages=find_packages(),
    package_data={"": ["*.c", "*.h", "*.o", "*.so", "*.md", "*.txt"]},
    include_package_data=True,
    zip_safe=False,
    url="https://github.com/osl-incubator/pyreaddbc",
    license="gpl-v3",
    author="Flavio Codeco Coelho",
    author_email="fccoelho@gmail.com",
    description="pyreaddbc",
    long_description="pyreaddbc",
    setup_requires=["cffi>=1.0.0", "setuptools>26.0.0"],
    cffi_modules=["pyreaddbc/_build_readdbc.py:ffibuilder"],
    install_requires=requirements,
    # cmdclass={'install': PostInstall},
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "pre-commit",
            "black",
            "isort",
            "flake8",
            "coverage",
            "wheel",
            "setuptools",
        ]
    },
    test_suite="tests",
    tests_require=["pytest", "flake8"],
)
