# atc2txt
Automatic speech recognition and transcription of ATC (Air Traffic Control) streams.

* https://atc2txt.org
* https://spacecruft.org/aviation/atc2txt

# Installation
Thusly, suit to taste:

```
git clone https://spacecruft.org/aviation/atc2txt
cd atc2txt/
python -m venv venv
source venv/bin/activate
pip install -U setuptools pip wheel
pip install -e .
```

# Help
```
$ atc2txt --help
usage: atc2txt [-h] [-c] [-D] [-d [DOWNLOAD_MODEL]] [-m MODEL] [-s] [-u URL] [-v] [-V]

Automatic speech recognition and transcription of ATC streams

options:
  -h, --help            show this help message and exit
  -c, --client          Run client
  -D, --debug           Debugging
  -d [DOWNLOAD_MODEL], --download-model [DOWNLOAD_MODEL]
                        Download model. Default: https://huggingface.co/jacktol/whisper-medium.en-fine-tuned-for-ATC-faster-whisper
  -m MODEL, --model MODEL
                        Model. Default: models/whisper-medium.en-fine-tuned-for-ATC-faster-whisper
  -s, --server          Run server
  -u URL, --url URL     URL to stream. Default: http://d.liveatc.net/kden1_1
  -v, --verbose         Increase output verbosity
  -V, --version         Show version
```

# Usage
* Download a model.
* Run the server in one window.
* Run the client in another window.

## Download
```
atc2txt --download-model
```

## Server
```
atc2txt --server
```

## Client
```
atc2txt --client
```

# Upstream
* https://github.com/collabora/WhisperLive -- MIT License.
* https://huggingface.co/jacktol/whisper-medium.en-fine-tuned-for-ATC-faster-whisper -- MIT License.

# License
MIT or Creative Commons CC by SA 4.0 International.
You may use this code, files, and text under either license.

Unofficial project, not related to upstream projects.

Upstream sources under their respective copyrights.

*Copyright &copy; 2025 Jeff Moe.*
