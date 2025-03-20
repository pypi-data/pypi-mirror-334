=====
Usage
=====
Thusly.

Help
----

.. code-block:: bash

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


Overview
--------
* Download a model.
* Run the server in one window.
* Run the client in another window.

Download
--------
.. code-block:: bash

  atc2txt --download-model

Server
------
.. code-block:: bash

  atc2txt --server

Client
------
.. code-block:: bash

  atc2txt --client

