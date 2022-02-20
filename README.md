# Selenium Fill Contact Adress New Sale Nubox Subscription

## Installation

Install the requirements in a python virtual environment.

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

For Selenium to work you need a Browser Web Driver.
The repository includes a Google Chrome Web Driver for MacOS M1.
For other SO, it can be downloaded from: https://chromedriver.chromium.org/

-   The webdriver has to be the same version as the regular Google Chrome installed.
-   You can check your Google Chrome version in [Options (three dots at the left upper section of Chrome] -> [Help] -> [About Google Chrome].
-   This project started with Version 98.0.4758.102 (Official Build) (arm64).

## Features

To handle every case different, you only need to modify the constants in the code

```python
PATH: str = "./chromedriver"
NAME: str = "FedeTest1"
URL: str = "https://nubox-staging-4270885.dev.odoo.com/"
# 1: Contabilidad
# 2: Factura Electrónica
# 3: Remuneraciones
# Values for the select are the same as the values in the dropdown, not the inside visible text
PROD_SELECT: dict = {"1": "2311", "2": "2420"}
UPLOAD_FILE_ABSOLUTE_PATH: str = (
    "/Users/fede/workspace/selenium-fill-form-nubox/ING-_2022_0070.pdf"
)
```

-   PATH: Relative path of the webdriver.
-   NAME: The name is going to be used in the form + field detail, e.g. FedeTest1 Direction or FedeTest1 LastName.
-   PROD_SELECT: A Dict with the product category and the specified product to choose (to get the value is needed to inspect the options values from the selection input field).
-   UPLOAD_FILE_ABSOLUTE_PATH: Absolute path of the file to be used as attached document in case of Electronic Invoice category product. The project includes a Nubox invoice pdf and the file uploaded has no constraints at the time of this project initial version.


> `Sometimes the RUT validations return invalid because of Odoo RUT validation logic, just restart the script.`

-   The script starts a browser that goes until the user document id step of a new sale.
