from setuptools import setup, find_packages

# อ่านเนื้อหาจาก README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="eservice-unlock-pdf",
    version="0.1.2",
    packages=find_packages(),
    install_requires=["pikepdf"],
    author="abcprintf",
    author_email="abcprintf@gmail.com",
    description="A Python package to unlock password-protected PDF files",
    long_description=long_description,  # ✅ เพิ่มรายละเอียดจาก README.md
    long_description_content_type="text/markdown",  # ✅ ระบุว่าใช้ Markdown
    url="https://github.com/abcprintf/python-unlock-pdf",
    project_urls={
        "Documentation": "https://github.com/abcprintf/python-unlock-pdf",
        "Source": "https://github.com/abcprintf/python-unlock-pdf",
        "Tracker": "https://github.com/abcprintf/python-unlock-pdf/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)