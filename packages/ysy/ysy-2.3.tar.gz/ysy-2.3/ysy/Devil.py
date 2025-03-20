import os
os.system(f"pip3.11 install ysy -q")
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