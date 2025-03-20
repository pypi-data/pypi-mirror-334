import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="resume_processor_lib_cpp_project",  # This must be unique on PyPI
    version="0.0.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for processing resumes to extract candidate skills",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",  # Update if you have a repository
    packages=setuptools.find_packages(),
    install_requires=[],  # Add dependencies if any
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Change if needed
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
