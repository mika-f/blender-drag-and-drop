
def check_module_installed(mod: str) -> bool:
    try:
        __import__(mod)
        return True
    except ModuleNotFoundError:
        return False
