#### Introduction
This is a python based website crawling script equipped with following capabilities to trick the website robot and avoid getting blocked.
* Random time intervals
* User-Agent switching
* IP rotation through proxy server

#### Installation
Although, the script has been tested on Python3.6 but it should work with future versions of Python too.

Install the libraries provided in requirements.txt by using following command <br />
*python -m pip install -r requirements.txt*

#### Installation on M1
1. Remove line redislite==5.0.165407 from requirements.txt
2. Run the command - sudo git clone https://github.com/tvd0x2a/redislite --branch m1-support ../redislite-m1-support && cd ../redislite-m1-support && python setup.py install
3. /opt/homebrew/opt/python@3.9/bin/pip3 install -r requirements.txt

#### Running the script
run the script by using following command <br />
*python websitescrap.py https://www.wikipedia.org*

**if you wish to start the crawling afresh from the supplied address, please use following command** <br />
*python websitescrap.py https://www.wikipedia.org --start_afresh true*

#### Output
The output will be a number of json files (stored in /data/ directory), where each file contains the raw html content of webpage in the following format

{"url": "raw html content of the webpage associated with URL"}
