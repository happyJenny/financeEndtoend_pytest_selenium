import pytest
from core.driver_factory import chrome_driver


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="以 headless 模式运行 Chrome",
    )


@pytest.fixture
def driver_conftest(request):
    driver = chrome_driver(headless=request.config.getoption("--headless"))
    try:
        yield driver
    finally:
        driver.quit()