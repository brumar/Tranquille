import calc
import sys
import re
import eel
import os

# IMPORTANT
# IN PROD(i.e in Jenkins), Transcrypt is not imported and there is no transpiling step
# Transpiling takes place when you develop
# When developping, change DEV to True (next line) or set an environnement variable "ENV" at "DEV"
# so that each time you run this file, your python file gets transpile with transcrypt

DEV = os.getenv("ENV", "PROD") == "DEV"
if DEV:
    from transcrypt.__main__ import main as transpile
if False:
    import web.frontendscrypt as eel


# KEEP THIS STRUCTURE EACH TIME YOU IMPORT FRONT END FUNCTIONS
with eel.import_frontend_functions():
    # warning. this wont work : from web.frontendscrypt import show_previous_results, logdone
    # My patching of __import__ fails when doing so
    # Any idea how to fix it
    from web.frontendscrypt import show_previous_results
    from web.frontendscrypt import logdone

web_app_options = {
    "mode": "chromium",  # or "chrome"
    "port": 8000,
    "chromeFlags": [
        "--start-fullscreen",
        "--browser-startup-dialog",
        "-disable-application-cache",
        "–media-cache-size=1",
        "--disk-cache-dir=/dev/null",
        "–disk-cache-size=1",
    ],
}


def log_result_in_file(v1, v2, result):
    with open("./log.txt", "a") as lg:
        lg.write(f"{v1} + {v2} = {result}\r\n")
        #logdone()

@eel.expose
def showpreviousvalues():
    if os.path.exists("./log.txt"):
        with open("./log.txt", "r") as lg:
            lines = [line.strip() for line in lg]
            show_previous_results(lines)


@eel.expose  # Expose this function to Javascript
def compute(a, b):
    value = calc.add2(a, b)
    log_result_in_file(a, b, value)
    return value


def restart(page, websockets):
    start(block=False, webpath="web", alive=True)


def start(block=True, webpath="web", alive=False):
    eel.init(webpath, search_exposed_js=False, search_into_imports=True)  # Give folder containing web files
    eel.register_backend_names(["backend"])
    eel.register_frontend_js_files(["web/__target__/frontendscrypt.js"])
    eel.start(
        "additions_diary.html",
        size=(300, 200),
        block=block,
        options=web_app_options,
        callback=restart,
        alive=alive,
    )  # Start


# eel.start('additions_diary.html', size=(300, 200), block=False)    # Start
if __name__ == "__main__":
    
    # stolen from /bin/transcrypt
    if DEV:
        sys.argv = ["transcrypt.py", "-e", "6", "-b", "./web/frontendscrypt.py", "-n"]
        sys.argv[0] = re.sub(r"(-script\.pyw?|\.exe)?$", "", sys.argv[0])
        transpile()
    start(block=False, webpath="web")
    while True:
        eel.sleep(10)
