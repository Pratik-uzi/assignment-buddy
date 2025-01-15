from setuptools import setup, find_packages

setup(
    name="assignment-buddy",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'pillow',
        'PyPDF2',
        'python-docx',
        'streamlit',
        'requests',
        'werkzeug',
        'reportlab'
    ],
    author="Pratik Kumar Chakraborty",
    author_email="chakravartypratik377@gmail.com",
    description="Convert PDF and DOCX files to handwritten notes",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Pratik-uzi/assignment-buddy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
) 