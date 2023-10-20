"""Jupyter Wolframizer magic"""
__version__ = '0.0.1'

from .Wolframizer import Wolframizer


def load_ipython_extension(ipython):
    ipython.register_magics(Wolframizer)
