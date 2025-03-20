
def is_webdriver_available(handle):
    try:
        handle.session
        return True
    except NoSuchSessionException:
        # The session does not exist
        return False
    except WebDriverException:
        # Some other WebDriver exception occured
        return False




