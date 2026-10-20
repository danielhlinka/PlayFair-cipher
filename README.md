# Playfair Cipher Web App

A simple Flask web app for encrypting and decrypting text using a modified Playfair cipher.

## Features

- Encrypt and decrypt text
- Custom encryption key
- Shows encryption steps and the key square
- Simple web interface

## Requirements

- Python 3.8+
- pip

## Installation

1. Clone the repository:

```bash
git clone [https://github.com/YOUR_USERNAME/playfair-cipher-app.git](https://github.com/YOUR_USERNAME/playfair-cipher-app.git)
cd playfair-cipher-app
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the app

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000/
```

## Usage

1. Enter text and a key.
2. Click **Encrypt** or **Decrypt**.
3. Use the same key to decrypt an encrypted message.

## Create `requirements.txt`

If you need to generate it:

```bash
pip freeze > requirements.txt
```