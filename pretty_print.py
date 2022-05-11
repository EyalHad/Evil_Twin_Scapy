from time import sleep


def pretty(content: str):
    for c in content:
        if "=" in c:
            sleep(0.007)
        else:
            sleep(0.035)
        print(c, end="", flush=True)
    print("")
