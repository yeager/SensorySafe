from setuptools import setup, find_packages

setup(
    name="sensorysafe",
    version="1.0.0",
    description="Kartapp som visar sensoriskt belastande platser för autistiska personer",
    author="SensorySafe",
    license="GPL-3.0",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "PyGObject>=3.42",
    ],
    entry_points={
        "console_scripts": [
            "sensorysafe=sensorysafe.main:main",
        ],
    },
    data_files=[
        ("share/applications", ["data/se.sensorysafe.app.desktop"]),
    ],
)
