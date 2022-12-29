from SubscribeCore import SubscribeCore


def main():
    S_C=SubscribeCore()
    print(S_C.scheduler.state,S_C.scheduler.get_jobs())