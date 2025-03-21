bwreceive
=========

bwreceive is a wrapper around [bw-cli](https://github.com/bitwarden/clients/releases) to display bitwarden send password from a custom bwsend:// url containing both the bitwarden url and the password to access it

Usage
-----

The expected format of the URL is `bwsend://<bitwarden url>?<send password>`

```
bwreceive --help
usage: bwreceive [-h] [-V] [-l {ERROR,WARNING,INFO,DEBUG}] url

Bitwarden Send opener

positional arguments:
  url                   example: bwsend://<send-url>?<send-password>

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
                        

Download bitwarden-cli from https://github.com/bitwarden/clients/releases/ and install it in your PATH for this script to work
```

Development
-----------

Setup environment, this will install all dependencies as well as the package itself in your virtual environment.

```bash
python -m venv venv
. venv/bin/activate
pip install -e .
```
