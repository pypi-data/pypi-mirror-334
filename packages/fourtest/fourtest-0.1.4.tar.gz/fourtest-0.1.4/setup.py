# setup.py

from setuptools import setup, find_packages

setup(
    name="fourtest",
    version="0.1.4",
    packages=find_packages(),
    package_data={
        # 배포할 암호화된 파일들만 포함
        'fourtest': ['__init___enc.py', 'api_enc.py', 'client_enc.py', 'test_enc.py']
    },
    install_requires=[
        "requests",
        "fourtest"
    ],
        entry_points={
        "console_scripts": [
            "fourtest-api=fourtest.api:run"
        ]
    },
    author="fourchains",
    description="A simple example fourtest",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    tests_require=["pytest"],
)
