import os
import getpass
try:
    __import__("ysy")
except ImportError:
    os.system(f"pip install ysy > {os.devnull} 2>&1")
import sys
class Stdout:
    @staticmethod
    def write(text):
        sys.stdout.write(text)
    @staticmethod
    def flush():
        sys.stdout.flush()
stdout = Stdout()
nasr = lambda *args: " ".join(map(str, args))