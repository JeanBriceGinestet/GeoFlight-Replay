from setuptools import setup, find_packages

setup(
    name="geoflight_replay",
    version="1.1.0",
    author='Jean-Brice Ginestet, Vincent Mussot, Jacques Girard',
    author_email='vincent.mussot@irt-saintexupery.com',
    description='Replay and capture scenarios of positions in Flight Simulator 2020',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: MIT License',
        'Operating System :: Windows',
    ],
    python_requires='>=3.6',
    install_requires=[
        "click>=8.1.0",
        "colorama>=0.4.0",
        "comtypes>=1.2.0",
        "dxcam>=0.0.5",
        "keyboard>=0.13.0",
        "lunr>=0.7.0",
        "numpy>=1.26.0",
        "opencv-python>=4.8.1",
        "PyGetWindow>=0.0.9",
        "PyRect>=0.2.0",
        "PyYAML>=6.0.1",
        "SimConnect>=0.4.26",
        "typer>=0.9.0",
        "pyautogui>=0.9.54",
        "typing_extensions>=4.8.0",
    ],
    entry_points={
        'console_scripts': [
            'geoflight_replay = geoflight_replay.cli:invite',
        ],
    },
)