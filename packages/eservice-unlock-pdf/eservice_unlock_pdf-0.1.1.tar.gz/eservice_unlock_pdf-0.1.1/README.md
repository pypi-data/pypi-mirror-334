## python unlock pdf

### Description
Since I have a pdf file that is locked with a password and I want to open that pdf file without entering the password every time, I want to create a script to unlock the pdf file.

This script is used to unlock a password protected pdf file. It uses the PyPDF2 library to unlock the pdf file. The password is provided as an argument to the script.

### Installation
```bash
// create a virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Usage
```bash
jupyter lab

// run the script
python unlock_pdf.py locked.pdf unlocked.pdf password
```

### Testing
```bash
tox
```

### Build
```bash
python setup.py sdist bdist_wheel

// check the build
twine check dist/*

// install the package
pip install dist/eservice_unlock_pdf-0.1.0-py3-none-any.whl
```

### uploade to pypi
```bash
pip install twine

twine upload dist/*          
```