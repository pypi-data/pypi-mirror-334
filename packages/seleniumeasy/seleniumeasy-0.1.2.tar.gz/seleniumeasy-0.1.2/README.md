# EasySelenium
# Table of Contents
1. [Overview](#overview)
2. [Configuration](#configuration)  
4. [Usage](#usage)
    1. [Web Driver Class](#webdriver-class-usage)
    2. [Automatically Updating Chromedriver](#updating-chromedriver)
5. [Contributing](#contributing)

## Overview
The EasySelenium project is designed to make the `Selenium` module a little bit easier to use. It supports automatic chromedriver updates, and shorter syntax for finding_elements. 

### Modules
The two main funtions of the module can be imported using 
```python
from seleniumeasy import WebDrvier
from seleniumeasy import update_driver
```

# Configuration
To easily download all repo code onto your local machine download the selenium-easy module from pip
```bash
pip install seleniumeasy
```
# Usage

## WebDriver Class Usage

The `WebDriver` class is designed to simplify Selenium programming by reducing tedious syntax. Below are the usage instructions and examples.

### Initialization

```python
from seleniumeasy import WebDriver

# Initialize WebDriver with default settings
driver = WebDriver()

# Initialize WebDriver in headless mode
driver = WebDriver(headless=True)

# Initialize WebDriver with a custom memory structure
driver = WebDriver(memory_structure={})

#Initialize WebDriver, using the specified chromedriver service
driver = WebDriver(headless = True, CHROMEDRIVER_PATH=/c/some/path/to/chromedriver.exe)
```

#### Parameters

- `headless`: A boolean to determine whether the opened page will be visible. If `True`, the browser will run in headless mode (no GUI). Defaults to `False`.
- `memory_structure`: A data structure to hold values for later use. Defaults to an empty list.
- `CHROMEDRIVER_PATH`: The path to your `chromedriver.exe`, by default will assume the current working directory.

### Methods

#### `find_element_by_id`

```python
element = driver.find_element_by_id('element_id', wait=10, errors='raise')
```

- `id`: The ID of the element to find.
- `wait`: Time in seconds to wait for the element to be present. Defaults to `None`.
- `errors`: Error handling strategy. If `'raise'`, an exception will be raised on error. If `'coerce'`, the error will be printed and the program will continue.

#### `find_elements_by_id`

```python
elements = driver.find_elements_by_id('element_id', wait=10, errors='raise')
```

- `id`: The ID of the elements to find.
- `wait`: Time in seconds to wait for the elements to be present. Defaults to `None`.
- `errors`: Error handling strategy. If `'raise'`, an exception will be raised on error. If `'coerce'`, the error will be printed and the program will continue.


EasySelenium can also be used to search by *class, css selector, and by xpath* with similar syntax, using:
- `find_element_by_class` and `find_elements_by_class` to search by class
- `find_element_by_css` and `find_elements_by_css`to search by css selector
- `find_element_by_xpath` and `find_elements_by_xpath` to search by xpath

### `get_soup`
```
#Returns a BeautifulSoup html parser of the JS-rendered page. 
soup = driver.get_soup()
```
### Example Usage

```python
from seleniumeasy import WebDriver

with WebDriver(headless=True) as driver:
    driver.get('https://example.com')

    #This may not exist on the website, so in that case we'll just log that it wasn't found instead of halting the program
    element = driver.find_element_by_id('example_id', wait=10, errors='coerce')
    print(element.text if element else "Element not found")

    #This is essential for the program to run, raise an error if not found
    elements = driver.find_elements_by_class('example_class', wait=10, errors='raise')
    for elem in elements:
        print(elem.text)
    #Create a BeautifulSoup parser of the driver (post JS-rendering)
    soup = driver.get_soup()
```
## Updating Chromedriver

The `update_driver` function allows you to automatically download the most recent version of the chromedriver for an input Operating System.

### Platforms
The available platforms are:
- `linux64`
- `mac-arm64`
- `mac-x64`
- `win32`
- `win64`

### Example Usage

```python
from seleniumeasy import update_driver

# Update chromedriver for Windows 64-bit
update_driver('win64')

# Update chromedriver for macOS ARM64
update_driver('mac-arm64')
```

This will download the most recent chromedriver for the specified platform to the current working directory. It is an intended future update to customize the driver download/launch locations for each project.


## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
