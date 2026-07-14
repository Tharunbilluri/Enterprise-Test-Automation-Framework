"""Checkout flow locators for Sauce Demo."""

from __future__ import annotations

from selenium.webdriver.common.by import By

# Step One — Your Information
FIRST_NAME = (By.CSS_SELECTOR, "[data-test='firstName']")
LAST_NAME = (By.CSS_SELECTOR, "[data-test='lastName']")
POSTAL_CODE = (By.CSS_SELECTOR, "[data-test='postalCode']")
CONTINUE_BUTTON = (By.CSS_SELECTOR, "[data-test='continue']")
CANCEL_BUTTON = (By.CSS_SELECTOR, "[data-test='cancel']")
ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
STEP_ONE_TITLE = (By.CSS_SELECTOR, "[data-test='title']")

# Step Two — Overview
FINISH_BUTTON = (By.CSS_SELECTOR, "[data-test='finish']")
SUMMARY_SUBTOTAL = (By.CSS_SELECTOR, "[data-test='subtotal-label']")
SUMMARY_TAX = (By.CSS_SELECTOR, "[data-test='tax-label']")
SUMMARY_TOTAL = (By.CSS_SELECTOR, "[data-test='total-label']")
OVERVIEW_ITEM_NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
OVERVIEW_ITEM_PRICE = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")

# Complete
COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")
COMPLETE_TEXT = (By.CSS_SELECTOR, "[data-test='complete-text']")
BACK_HOME = (By.CSS_SELECTOR, "[data-test='back-to-products']")
