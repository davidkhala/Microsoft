from pathlib import Path

from davidkhala.utils.build import Installer

source = Path(__file__).parent / "davidkhala/microsoft/purview/databricks/cli.py"
i = Installer(str(Path(__file__).parent / 'dist'),   str(source))


def build():
    i.name = 'purview'
    r = i.build()
    print(" ".join(r.args)) # raw command


def clean():
    i.clean(True)
