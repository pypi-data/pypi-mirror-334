import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-aspect-vpc-stateful-cidr-block-assigner",
    "version": "0.0.9",
    "description": "CDK Aspect to alter the Amazon VPC subnet CIDR blocks assignment to respect existing CIDR blocks when updating a CDK Vpc construct",
    "license": "Apache-2.0",
    "url": "https://github.com/fibert/cdk-aspect-vpc-stateful-cidr-block-assigner.git",
    "long_description_content_type": "text/markdown",
    "author": "Dor Fibert<dorfib@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/fibert/cdk-aspect-vpc-stateful-cidr-block-assigner.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_aspect_vpc_stateful_cidr_block_assigner",
        "cdk_aspect_vpc_stateful_cidr_block_assigner._jsii"
    ],
    "package_data": {
        "cdk_aspect_vpc_stateful_cidr_block_assigner._jsii": [
            "cdk-aspect-vpc-stateful-cidr-block-assigner@0.0.9.jsii.tgz"
        ],
        "cdk_aspect_vpc_stateful_cidr_block_assigner": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.178.1, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.109.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
