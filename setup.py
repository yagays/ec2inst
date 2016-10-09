# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="ec2inst",
    packages=['ec2inst'],
    version="0.0.1",
    description="AWS EC2 instance console for CLI",
    author="yagays",
    author_email="yanagi.ayase@gmail.com",
    url="https://github.com/yagays/ec2inst",
    install_requires=['requests'],
    keywords=["AWS", "EC2"],
    entry_points={
        'console_scripts': [
            'ec2inst = ec2inst.ec2inst:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
