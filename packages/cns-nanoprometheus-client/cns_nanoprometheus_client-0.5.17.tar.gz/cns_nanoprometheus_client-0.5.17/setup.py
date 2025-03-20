from setuptools import setup, find_packages

setup(
    name="cns-nanoprometheus-client",
    version="0.5.17",
    description="Python client for Nanoprometheus metrics",
    author="Roman Skvara",
    author_email="skvara.roman@gmail.com",
    license="MIT",
    license_files=["LICENSE"],
    packages=find_packages(),
    url='https://github.com/opicevopice/cns-nanoprometheus-client',
    install_requires=["requests_html", "lxml_html_clean"],
    entry_points={
        "console_scripts": [
            "cns-nano-init = cns_nanoprometheus_client:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
