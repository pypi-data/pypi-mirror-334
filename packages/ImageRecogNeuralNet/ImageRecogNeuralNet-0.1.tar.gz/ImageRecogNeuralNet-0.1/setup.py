from setuptools import setup, find_packages

setup(
    name="ImageRecogNeuralNet",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scikit-learn",
        "pillow",
    ],
    entry_points={
        'console_scripts': [
            'ImageRecogNeuralNet = ImageRecogNeuralNet:start_ui',
        ],
    },
    author="Sai Mounik",
    description="A simple neural network library with UI for training and recognition",
    python_requires='>=3.9',
)