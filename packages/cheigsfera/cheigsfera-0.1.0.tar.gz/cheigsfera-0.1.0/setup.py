from setuptools import setup, find_packages

setup(
    name='cheigsfera',
    version='0.1.0',
    description='Пример пакета с зависимостями',
    author='cheigg',
    author_email='egorleuchin99@gmail.com',
    packages=find_packages(),
    python_requires='>=3.6',  # Requires-Python
    install_requires=[
        'requests>=2.25.1',  # Requires-Dist
        'numpy>=1.19.5; python_version<"3.8"',  # Requires-Dist с условием
    ],
    extras_require={
        'dev': ['pytest>=6.0'],  # Provides-Extra
    },
    provides=['my_package'],  # Provides-Dist
    obsoletes=['old_package'],  # Obsoletes-Dist
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],
)