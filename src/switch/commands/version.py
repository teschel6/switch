from importlib import metadata


def version():
    ver = metadata.version("switch")
    print(f"v{ver}")

