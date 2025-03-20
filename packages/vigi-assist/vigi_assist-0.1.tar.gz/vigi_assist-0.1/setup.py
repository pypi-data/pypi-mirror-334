from setuptools import setup, find_packages

setup(
    name="vigi-assist",  # Package name
    version="0.1",  # Version of the package
    packages=find_packages(),
    install_requires=[  # Add any dependencies you might have
        "google-generativeai",
        "requests",  # example of an external dependency
    ],
    entry_points={  # If you have a command-line tool, define it here
        'console_scripts': [
            'ai-cmd = aicmd.main:main',  # Make sure this points to the correct function in your package
        ],
    },
    author="Your Name",  # Replace with your actual name
    author_email="your_email@example.com",  # Replace with your email
    description="A brief description of what your package does",  # Short description
    long_description=open('README.md').read(),  # Read the long description from your README file
    long_description_content_type="text/markdown",  # Specify that README is in markdown format
    url="https://github.com/yourusername/your-repo",  # Replace with your actual project URL
    license="MIT",  # Replace with your actual license, if different
    classifiers=[  # PyPI classifiers to categorize your package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
)
