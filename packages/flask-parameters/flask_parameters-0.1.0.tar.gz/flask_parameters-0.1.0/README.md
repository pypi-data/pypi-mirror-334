<h1 align="center">Flask Parameters<br></h1>

<h4 align="center">Inject URL query parameters as arguments into Flask route functions.</h4>

<p align="center">
  <img src="https://img.shields.io/badge/status-active-green" />
  <img src="https://img.shields.io/pypi/pyversions/flask-parameters" />
  <a href="https://pypi.org/project/flask-parameters/"><img src="https://img.shields.io/pypi/v/flask-parameters" /></a>
  <img src="https://img.shields.io/pypi/l/flask-parameters" /><br />
  <img src="https://img.shields.io/github/issues/millarcalder/flask_params" />
  <img src="https://img.shields.io/github/issues-pr/millarcalder/flask_params" />
</p>

<p align="center">
  <a href="http://flask-params-docs.s3-website-ap-southeast-2.amazonaws.com/">Documentation</a> •
  <a href="#key-features">Key Features</a> •
  <a href="#built-using">Built Using</a> •
  <a href="#usage">Usage</a> •
  <a href="#license">License</a>
</p>

## Key Features

 - Inject query parameters into your route functions
 - Type checking based on the signature of the function

## Built Using

 - [Flask](https://flask.palletsprojects.com/)

## Installation

```bash
pip install flask-parameters
```

## Usage

```python
from flask_parameters import Flask

app = Flask(__name__)


@app.route("/foo")
def foo(arg, kwarg = 123) -> dict:
    return {"arg": arg, "kwarg": kwarg}


@app.route("/strict_foo")
def strict_foo(arg: str, kwarg: int = 123) -> dict:
    return {"arg": arg, "kwarg": kwarg}
```

## License

MIT
