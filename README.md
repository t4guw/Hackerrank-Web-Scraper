# Hackerrank Web Scraper

## Dependencies

* Selenium
* ChromeDriver

### Installing Dependencies

#### Windows

Run `python -m pip install selenium`.

The `ChromeDriver` executable can be downloaded from this [link](https://chromedriver.storage.googleapis.com/index.html?path=2.41/).

#### Linux

Run `pip3 install -r requirements.txt`.


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

3. In main.py, there is a variable called "category". Change it to whichever hackerrank category you want to scrape. For instance, if you want to scrape the algorithms section (https://www.hackerrank.com/domains/algorithms) set category to "algorithms".

3. Run main.py (e.g. `python3 main.py`)

