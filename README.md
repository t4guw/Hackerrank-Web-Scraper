# Hackerrank Web Scraper

## Dependencies

* Selenium
* ChromeDriver

### First-Time Setup

`git clone` this repository.

In the project's root directory, run the following commands to setup a virtual environment.
This will ensure that we are using the versions of each module and the same Python version.
See [the Python 3 docs](https://docs.python.org/3/library/venv.html) for more information.

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt 
```

### Installing Dependencies

#### Windows

Run `python3 -m pip install selenium`.

The `ChromeDriver` executable can be downloaded from this [link](https://chromedriver.storage.googleapis.com/index.html?path=2.41/).

#### Linux

Run `pip3 install -r requirements.txt`.

Run the following commands to install `ChromeDriver`.
```bash
wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
```

## Usage

1. Install dependencies

2. Download main.py and scrape_hackerrank.py into the same directory

3. `main.py` accepts a command line argument for a hackerrank category. Provide the name of whichever hackerrank category you want to scrape. For instance, if you want to scrape the algorithms section (https://www.hackerrank.com/domains/algorithms) , run `python3 main.py algorithms`.

3. Run main.py (e.g. `python3 main.py <category>`)

