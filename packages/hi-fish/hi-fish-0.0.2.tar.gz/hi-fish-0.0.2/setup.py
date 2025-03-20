import setuptools

setuptools.setup(
    name="hi-fish",
    version="0.0.2",
    author="tom",
    author_email="tom@google.com",
    description="Agent, Copyright@Plutonium",
    entry_points={
        "console_scripts": ["hi=hi.cli:main",]
    },
    license="MIT",
    long_description='Hi',
    long_description_content_type="text/markdown",
    url="https://www.google.com",
    packages=["hi",],
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Utilities",
        "Topic :: Security",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.7",
)
