# -*- encoding: utf-8 -*-
"""
@File    :   format.py
@Time    :   2025/2/25 下午8:29
@Author  :   Li Jiawei
@Version :   1.0
@Contact :   Li.J.W.adrian421@hotmail.com
@License :   (C)Copyright 2023-2030
@Desc    :   None
@Brief   :
"""
import os, sys, argparse
from tqdm import tqdm
from itertools import groupby, tee
from datetime import timedelta
from collections import Counter
import codecs, json, \
    time, datetime, pickle, \
    re, random, numpy as np, \
    pandas as pd, xml.dom.minidom as xmldom, string
import inspect
import platform
import yaml
import itertools
from pdb import set_trace as stop
from typing import Any, List, Tuple, Union


class EasyDict(dict):
    """Convenience class that behaves like a dict but allows access with the attribute syntax."""

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value

    def __delattr__(self, name: str) -> None:
        del self[name]


def jsondump(x):
    """
    adjusted json.dumps according to
    https://blog.csdn.net/weixin_39561473/article/details/123227500
    param
    ------
    x: dict, input

    return
    ------
    res: string, json.dumps dict string
    """

    def default_dump(obj):
        """Convert numpy classes to JSON serializable objects."""
        if isinstance(obj, (np.integer, np.floating, np.bool_)):
            return obj.item()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj

    res = json.dumps(x, ensure_ascii=False, default=default_dump)
    return res


def dict2class(dct, clsname='default_cls'):
    """
    Fasr converting a input dict to be a python Class

    Parameter:
    ----------
    dct: dict, any dict
    clsname: string, determine the class name for the new class

    Return:
    -------
    res: class, a new class having attributes from dict keys
    attrs: list, a list containing all attribute names
    """
    res = type(f"{clsname}", (), dct)
    attrs = list(res.__dict__.keys())
    return res, attrs


def topct(x, total):
    return round(x / total, ndigits=4) * 100


def limnum(x, out_float=1):
    """
    limit number
    """
    if out_float:
        return float(f"{x:.4f}")
    else:
        return f"{x:.4f}"


class PathHandler:
    def __init__(self, path_str):
        """
        Initialize with a file or directory path string.

        Args:
            path_str (str): The path to a file or directory
        """
        self._path = os.path.normpath(path_str)

    @property
    def path(self):
        """Get the full path of the file or directory."""
        return self._path

    @property
    def back(self):
        """
        Get the parent directory of the current path.

        Returns:
            PathHandler: A new PathHandler object for the parent directory
        """
        parent_dir = os.path.dirname(self._path)
        return PathHandler(parent_dir)

    def next(self, name):
        """
        Join the current path with the given name and check if it exists.

        Args:
            name (str): Name of file or directory to join with current path

        Returns:
            PathHandler or None: A new PathHandler object for the joined path if it exists,
                                otherwise prints a message and returns None
        """
        joined_path = os.path.join(self._path, name)

        if os.path.exists(joined_path):
            return PathHandler(joined_path)
        else:
            print(f"The path '{joined_path}' does not exist.")
            return None

    def __str__(self):
        """String representation of the PathHandler object."""
        return self._path

    def __repr__(self):
        """Representation of the PathHandler object."""
        return f"PathHandler('{self._path}')"

    # Allow the object to be used anywhere a string is expected
    __radd__ = __add__ = lambda self, other: str(self) + other if isinstance(other, str) else NotImplemented

    def usage_case(self):
        test_obj = PathHandler("/Users/nerozac421/Documents/nerozac_arxiv/others/public_pypi/wixio/wixio")
        print(test_obj)
        print(test_obj.back)
        print(test_obj.back.back)
        print(test_obj.next("crawl"))
        print(test_obj.next("retry").next("retry.py"))


# Example usage:
if __name__ == "__main__":
    # Example with a file path
    test_obj = PathHandler("/Users/nerozac421/Documents/nerozac_arxiv/others/public_pypi/wixio/wixio")
    test_obj.usage_case()
