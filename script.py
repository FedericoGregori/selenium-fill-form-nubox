"""
Nubox New Sale QA Automation Script
"""

import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

from utils import chile_rut
from utils.timer import Timer

_logger = logging.getLogger(__name__)

PATH: str = "./utils/chromedriver"
NAME: str = "Test"
URL: str = "https://nubox-staging-4270885.dev.odoo.com/"
# 1: Contabilidad
# 2: Factura Electrónica
# 3: Remuneraciones
# Values for the select are the same as the values in the dropdown, not the inside visible text
PROD_SELECT: dict = {"1": "2311", "2": "2420"}
UPLOAD_FILE_ABSOLUTE_PATH: str = (
    "/Users/fede/workspace/selenium-fill-form-nubox/utils/ING-_2022_0070.pdf"
)

LONG_WAIT: int = 10
MEDIUM_WAIT: int = 5
SHORT_WAIT: int = 2

os.system("clear")

try:
    with Timer("Nubox New Sale Automation") as t:
        # Browser
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument("--incognito")
        service = Service(PATH)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(URL)

        # Pages navigation
        # Home page
        time.sleep(MEDIUM_WAIT)
        services_button = driver.find_element("id", "services")
        services_button.click()

        # Select products page
        time.sleep(SHORT_WAIT)
        for categ_id, product in PROD_SELECT.items():
            category = driver.find_element(
                "xpath",
                f"//*[@id='wrapwrap']/main/div[1]/div/div/div[1]/div[{categ_id}]/input",
            )
            category.click()
            if not category.is_selected():
                category.click()

            time.sleep(SHORT_WAIT)
            select = Select(
                driver.find_element(
                    "xpath",
                    f"//*[@id='wrapwrap']/main/div[1]/div/div/"
                    f"div[1]/div[{categ_id}]/div/div/select",
                )
            )
            select.select_by_value(product)

        next_element = driver.find_element("xpath", "//*[@id='buttonSig']")
        next_element.click()

        # Check order page
        time.sleep(SHORT_WAIT)
        pay_now_element = driver.find_element(
            "xpath", "//*[@id='wrap']/div[1]/div/div[2]/div/div/a[2]"
        )
        pay_now_element.click()

        # Addresses page
        # User Data
        time.sleep(SHORT_WAIT)
        ruts = chile_rut.random_ruts(2)
        driver.find_element("name", "vat").send_keys(ruts[0])
        driver.find_element("name", "name").send_keys(NAME)
        driver.find_element("name", "last_name").send_keys(NAME + " LastName")
        driver.find_element("name", "last_name_mother").send_keys(NAME + " MotherName")
        time.sleep(SHORT_WAIT)
        Select(
            driver.find_element(
                "xpath",
                "//*[@id='commune']",
            )
        ).select_by_value("Alhue")
        driver.find_element("name", "street").send_keys(NAME + " Street")
        driver.find_element("name", "phone").send_keys("56224674996")
        driver.find_element("name", "mobile").send_keys("56224674996")
        driver.find_element("name", "email").send_keys(NAME + "@gmail.com")
        driver.find_element("name", "email_confirmation").send_keys(NAME + "@gmail.com")
        driver.find_element("name", "identification_card").send_keys("123456789")
        # Upload id file
        field = driver.find_element("id", "attach_photocopy")
        driver.execute_script("arguments[0].style.display = 'block';", field)
        field.send_keys(UPLOAD_FILE_ABSOLUTE_PATH)

        # Company Data
        driver.find_element("name", "company_name").send_keys(NAME + " Company")
        driver.find_element("name", "company_vat").send_keys(ruts[1])
        driver.find_element("name", "company_phone").send_keys("56224674996")
        driver.find_element("name", "company_l10n_cl_activity_description").send_keys(
            NAME + " Company Activity"
        )
        Select(
            driver.find_element(
                "xpath",
                "//*[@id='company_commune']",
            )
        ).select_by_value("Alhue")
        driver.find_element("name", "company_street").send_keys(NAME + " Street")
        driver.find_element("name", "company_l10n_cl_dte_email").send_keys(
            NAME + "@gmail.com"
        )
        driver.find_element("name", "company_email_confirmation").send_keys(
            NAME + "@gmail.com"
        )

        driver.find_element("id", "buttonNext").click()

        # Retry RUTs
        time.sleep(SHORT_WAIT)
        try:
            modal_error = driver.find_element("id", "modal-error")
            if modal_error.is_displayed():
                modal_error_button = driver.find_element(
                    "xpath", "//*[@id='modal-error']/div/div/div[3]/button"
                )
                modal_error_button.click()
                ruts = chile_rut.random_ruts(2)
                time.sleep(SHORT_WAIT)
                driver.find_element("name", "vat").clear()
                time.sleep(SHORT_WAIT)
                modal_error_button.click()
                time.sleep(SHORT_WAIT)
                driver.find_element("name", "vat").send_keys(ruts[0])
                driver.find_element("name", "company_vat").clear()
                time.sleep(SHORT_WAIT)
                modal_error_button.click()
                time.sleep(SHORT_WAIT)
                driver.find_element("name", "company_vat").send_keys(ruts[1])
                driver.find_element("id", "buttonNext").click()
        except (TypeError, NoSuchElementException):
            pass

        # Payment methods page
        time.sleep(SHORT_WAIT)
        driver.find_element(
            "xpath", "//*[@id='payment_method']/form/div[1]/div[3]/label/input"
        ).click()
        driver.find_element("xpath", "//*[@id='checkbox_tyc']").click()
        driver.find_element("id", "o_payment_form_pay").click()

        # Mercado Pago
        time.sleep(LONG_WAIT)
        driver.find_element("xpath", "//*[@id='group_form_scroller']").click()
        time.sleep(MEDIUM_WAIT)
        driver.find_element("id", "card_number").send_keys("5031755734530604")
        driver.find_element("id", "input_expiration_date").send_keys("1125")
        driver.find_element("id", "fullname").send_keys("APRO")
        driver.find_element("id", "cvv").send_keys("123")
        driver.find_element("id", "submit").click()

        # Document page
        time.sleep(MEDIUM_WAIT)
        driver.find_element("id", "number").send_keys("123456789")
        driver.find_element("xpath", "//*[@id='type']/button").click()
        driver.find_element("xpath", "//*[@id='type']/div[2]/ul/li[3]").click()
        driver.find_element("xpath", "//*[@id='submit']").click()

        # Installments page
        time.sleep(SHORT_WAIT + 1)
        driver.find_element("xpath", "//*[@id='select_installments']/ul/li[1]").click()

    # Finish message
    _logger.warning(
        "\n\tTest finished successfully. %s\n", t.elapsed()
    )  # Using warning because it's the default log level

except (TypeError, NoSuchElementException) as e:
    _logger.error(e.msg)
