import os.path

from davidkhala.build import Installer
from davidkhala.syntax.path import dirname

_current = dirname(__file__)
source = os.path.join(_current, "davidkhala/microsoft/purview/databricks/cli.py")
i = Installer(os.path.join(_current, 'dist'), source)


def build():
    r = i.build()
    print(" ".join(r.args)) # raw command


def clean():
    i.clean(True)
