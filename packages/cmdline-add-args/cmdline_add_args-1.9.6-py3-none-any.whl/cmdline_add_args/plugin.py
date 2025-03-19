import os
import importlib.util

import pytest
from dotenv import load_dotenv

from cmdline_add_args.allure_report_path import CURRENT_DIRECTORY, CREATE_ALLURE_REPORT, get_browser_name, get

"""A custom function like load_dotenv()"""
def load_env_from_py(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")

    spec = importlib.util.spec_from_file_location("env", file_path)
    env = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(env)

    for attr in dir(env):
        if not attr.startswith("__"):
            value = getattr(env, attr)
            if isinstance(value, (bool, int, float)):
                value = str(value)
            elif not isinstance(value, str):
                continue
            os.environ[attr] = value


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(args):
    print("pytest_load_initial_conftests is called")

    env_path = os.path.join(CURRENT_DIRECTORY, 'config', 'env.py')

    if os.path.exists(env_path):
        load_env_from_py(env_path)
        print(f"Loaded environment variables from {env_path}")
    else:
        print(f"Environment file {env_path} not found.")

    create_allure_report = str(os.getenv('CREATE_ALLURE_REPORT', CREATE_ALLURE_REPORT)).lower() == 'true'
    browser = get('BROWSER', "chrome").lower()
    allure_report_path = get_browser_name(browser=browser, current_directory=CURRENT_DIRECTORY)

    if create_allure_report:
        new_args = ["-v", f"--alluredir={allure_report_path}", "--clean-alluredir"]
        for arg in new_args:
            if arg not in args:
                if args[-1].split(".")[-1] == "py":
                    args.insert(-1, arg)
                else:
                    args.append(arg)
        print(f"Modified pytest args: {args}")
    else:
        args[:] = [arg for arg in args if '--alluredir' not in arg and '--clean-alluredir' not in arg]
        print("Allure report is disabled.")

    print(f"Final pytest args: {args}")
