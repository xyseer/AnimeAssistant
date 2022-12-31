from SubscribeCore import SubscribeCore
from web.frontend import flask_main
from logging_module import Logger


def main():
    try:
        S_C=SubscribeCore()
        flask_main(S_C)
    except Exception as e:
        Logger().error(f"launcher.main occurred an error:{str(e)}")
        return