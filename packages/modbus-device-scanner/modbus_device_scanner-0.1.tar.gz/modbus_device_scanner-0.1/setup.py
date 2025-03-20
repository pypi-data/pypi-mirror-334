from setuptools import setup, find_packages

setup(
    name='modbus_device_scanner',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'ipaddress>=1.0.23',
        'argparse>=1.4.0',
    ],
    entry_points={
        'console_scripts': [
            'modbus_device_scanner=modbus_device_scanner.modbus_device_scanner:main',
        ],
    },
    author='Karmavir',
    author_email='karmavirj@protonmail.com',
    description='A package to scan for Modbus TCP devices on a network',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kvjoshi/modbus_device_scanner',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)