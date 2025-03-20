# -*- coding: utf-8 -*-
import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires = [x.strip() for x in fobj.readlines() if x.strip()]


setup(
    name="openai-simple-embeddings",
    version="0.1.2",
    description="基于OPENAI兼容API接口的embeddings服务封装，以解决langchain_community.vectorstores在使用bge-m3/bge-reranker-v2-m3等模型提供的OPENAI兼容API接口服务时遇到的兼容性问题。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="rRR0VrFP",
    maintainer="rRR0VrFP",
    license="Apache License, Version 2.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["openai-simple-embeddings"],
    packages=find_packages("."),
    install_requires=requires,
    zip_safe=False,
    include_package_data=True,
)
