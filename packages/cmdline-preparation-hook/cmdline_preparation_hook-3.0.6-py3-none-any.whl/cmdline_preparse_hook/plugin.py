import os
from time import sleep

import pytest

from App.admin.sauce_lab import SauceLabDevice, get_simulator_list
from App.config.driver_config import SAUCE_LAB
from App.config.env import SAUCE_LAB_DEVICES
from pytest_cmdline.cmdline_preparse_hook.config.env import (
    ALLURE_REPORT_PATH,
    ANDROID_PHONE_DEVICE_NAME,
    ANDROID_TABLET_DEVICE_NAME,
    APPIUM_PORT,
    CREATE_ALLURE_REPORT,
    IPAD_DEVICE_NAME,
    IPHONE_DEVICE_NAME,
    PLATFORM,
    PLATFORM_AND_APP,
)
from Testrail_utils.pytest_testrail_api.test_rail import TestRail


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(args):
    print("pytest_load_initial_conftests is called")

    create_allure_report = str(os.getenv("CREATE_ALLURE_REPORT", CREATE_ALLURE_REPORT)).lower() == "true"
    # browser = get("BROWSER", "chrome").lower()
    # allure_report_path = get_browser_name(browser=browser, current_directory=CURRENT_DIRECTORY)
    # ALLURE_REPORT_PATH = get_browser_name(browser=browser, current_directory=CURRENT_DIRECTORY)

    pytest.tr = TestRail()
    if create_allure_report:
        """Remove old allure results"""
        # if PLATFORM_AND_APP == "TABLET_DEVELOP":
        #     os.system(f'rm -rf {os.path.join(ALLURE_REPORT_PATH, "allure-results/tablet", "*-result.json")}')
        # else:
        #     os.system(f'rm -rf {os.path.join(ALLURE_REPORT_PATH, "allure-results/phone", "*-result.json")}')
        # os.system(f'rm -rf {os.path.join(ALLURE_REPORT_PATH, "allure-results/", "*.tar")}')
        new_args = ""
        if PLATFORM_AND_APP == "TABLET_DEVELOP":
            if "IPAD" in PLATFORM:
                new_args = [
                    "-v",
                    f"--alluredir={ALLURE_REPORT_PATH}/allure-results/ipad",
                ]
            else:
                new_args = [
                    "-v",
                    f"--alluredir={ALLURE_REPORT_PATH}/allure-results/android_tablet",
                ]

        elif PLATFORM_AND_APP == "PHONE_DEVELOP":
            if "IPHONE" in PLATFORM:
                new_args = [
                    "-v",
                    f"--alluredir={ALLURE_REPORT_PATH}/allure-results/iphone",
                ]
            else:
                new_args = [
                    "-v",
                    f"--alluredir={ALLURE_REPORT_PATH}/allure-results/android_phone",
                ]

        for arg in new_args:
            if arg not in args:
                if args[-1].split(".")[-1] == "py":
                    args.insert(-1, arg)
                else:
                    args.append(arg)
    if APPIUM_PORT == 443:
        device_name = {
            "IPAD": IPAD_DEVICE_NAME,
            "IPHONE": IPHONE_DEVICE_NAME,
            "ANDROID_PHONE": ANDROID_PHONE_DEVICE_NAME,
            "ANDROID_TABLET": ANDROID_TABLET_DEVICE_NAME,
        }.get(PLATFORM)
        if device_name is not None:
            SAUCE_LAB_DEVICES.append(SauceLabDevice(device_name))
            device_count_correction = 1
        else:
            device_count_correction = 0
        if "-n" in args:
            devices_filter = {
                "IPAD": {
                    "is_tablet": True,
                    "min_ram_size": 6000,
                    "os_type": "ios",
                    "min_os_version": "16",
                    "name_not_contains": "mini",
                },
                "IPHONE": {
                    "is_tablet": False,
                    "min_ram_size": 6000,
                    "os_type": "ios",
                    "name_not_contains": "Beta",
                    "min_os_version": "16",
                },
                "ANDROID_PHONE": {
                    "is_tablet": False,
                    "min_ram_size": 8000,
                    "os_type": "Android",
                    "min_os_version": "12",
                    "name_contains": "Google",
                },
                "ANDROID_TABLET": {
                    "is_tablet": True,
                    "min_ram_size": 6000,
                    "os_type": "Android",
                    "min_os_version": "12",
                    "name_not_contains": "S7",
                },
            }[PLATFORM]
            device_count = int(args[args.index("-n") + 1]) - device_count_correction
            devices_filter.update(
                {
                    "is_available": True,
                    "get_random_devices": device_count,
                    "is_private": False,
                }
            )
            devices = SAUCE_LAB.devices.filter_devices(**devices_filter)
            while len(devices) < device_count:
                sleep(15)
                devices = SAUCE_LAB.devices.filter_devices(**devices_filter)
            for test_device in devices:
                SAUCE_LAB_DEVICES.append(SauceLabDevice(test_device))
    else:
        if "-n" in args:
            for test_device in get_simulator_list(int(args[args.index("-n") + 1])):
                SAUCE_LAB_DEVICES.append(test_device)
