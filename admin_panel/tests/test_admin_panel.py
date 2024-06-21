import os


def test_check_environ():
    mypath = os.path.dirname(os.getcwd())
    for dirpath, dirnames, filenames in os.walk(mypath):
        for file in filenames:
            if file.split(".")[-1] in ["env", "example"]:
                return
    raise Exception("environment variable is unavailable")
