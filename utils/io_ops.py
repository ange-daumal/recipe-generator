import glob
import ntpath
import os
import pickle
from typing import Optional, List

import chardet
from dotenv import load_dotenv


def get_env_var(varname: str, env_path: str = ".env", ignore_not_found=False) -> str:
    """
    Try to get variable value from environment. If not found, check at env_path.
    If ignore_not_found is False and the value is not found, raise an error.
    :param varname:
    :param env_path:
    :param ignore_not_found:
    :return:
    """
    var = os.getenv(varname)
    if var:
        return var

    if not os.path.isfile(env_path):
        if ignore_not_found:
            return ''

        msg = f"Environment file not found at {os.getcwd()}/{env_path} and {varname} not found in environment " \
            "variables."
        raise Exception(msg)

    else:
        load_dotenv(dotenv_path=env_path)
        var = os.getenv(varname)
        if var:
            return var

        if ignore_not_found:
            return ''

        msg = f"Variable {varname} not found in environment variable even after loading" \
            f"{os.getcwd()}/{env_path} file."
        raise Exception(msg)


# Functions for save and load derived data objects

def save_obj(obj, fpath):
    with open(fpath, 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(fpath):
    if os.path.exists(fpath):
        with open(fpath, 'rb') as f:
            return pickle.load(f)
