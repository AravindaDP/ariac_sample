#!/usr/bin/env python
import os
from setuptools import setup

package_name = 'ariac_flexbe_behaviors'

setup(
    name=package_name,
    version='1.3.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='phil',
    maintainer_email='philsplus@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ariac_behavior_sm = ariac_flexbe_behaviors.ariac_behavior_sm',
        ],
    },
)
