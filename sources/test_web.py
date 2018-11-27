import backend
import pytest
import eel
import time


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=1024,768")  # hacky fix
    return chrome_options


def wait_for_value1(selenium):
    try:
        selenium.find_element_by_name("value_1")
        return True
    except:
        return False
    


def wait_for(condition_function, selenium, delay=3):
    start_time = time.time()
    while time.time() < start_time + delay:
        if condition_function(selenium):
            return True
        else:
            time.sleep(0.1)
    raise Exception('Timeout waiting for {}'.format(condition_function.__name__))


def test_interface(selenium):
    backend.start(block=False, webpath="web")
    eel.sleep(10)
    selenium.get("http://localhost:8000/additions_diary.html")
    eel.sleep(10)
    print(selenium.find_element_by_tag_name("body").get_attribute('innerHTML'))
    wait_for(wait_for_value1, selenium, delay=10)
    selenium.execute_script("document.getElementsByName('value_1')[0].value='6'")
    selenium.execute_script("document.getElementsByName('value_2')[0].value='10'")
    selenium.find_element_by_id("compute").click()
    # time.sleep(4)
    assert "16" in selenium.find_element_by_id("result").get_attribute('innerHTML')
