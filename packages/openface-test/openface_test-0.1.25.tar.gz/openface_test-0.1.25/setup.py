from setuptools import setup, find_packages

setup(
    name='openface-test',
    version='0.1.25',
    packages=find_packages(include=['openface', 'openface.*']),
    include_package_data=True,  # Include data files in the package
    package_data={
        'openface': ['**/*'],  # Include all files in the openface directory
    },
    install_requires=[
        'click==8.1.7',
        'huggingface_hub==0.21.0',
        'imageio==2.34.2',
        'matplotlib==3.10.1',
        'numpy==1.26.4',
        'opencv_contrib_python==4.11.0.86',
        'opencv_python==4.11.0.86',
        'pandas==2.2.3',
        'Pillow==9.4.0',
        'scipy==1.13',
        'seaborn==0.13.2',
        'scikit-image',  # No specific version provided
        'tensorboardX==2.6.2.2',
        'timm==1.0.15',
        'torch',  # No specific version provided
        'torchvision',  # No specific version provided
        'tqdm==4.66.2',
    ],
    entry_points={
        'console_scripts': [
            'openface=openface.cli:cli',  # Register the CLI command
        ],
    },
)