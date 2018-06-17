from PyQt5.QtCore import QMutex


class CompoundMutex:
    def __init__(self):
        self.__mutex = QMutex()

    def __enter__(self):
        self.__mutex.lock()
        return self

    def __exit__(self, type, value, traceback):
        self.__mutex.unlock()


class GuardedExecutor:
    def __init__(self, to_exec):
        self.__to_exec = to_exec
        self.__locked = False
        self.__request_to_exec = False

    def lock(self):
        with CompoundMutex as cm:
            self.__locked = True

    def unlock(self):
        with CompoundMutex as cm:
            self.__locked = False
            if self.__request_to_exec:
                self.__exec()

    def try_to_exec(self):
        with CompoundMutex as cm:
            if self.__locked:
                self.__request_to_exec = True
            else:
                self.__exec()

    def __exec(self):
        self.__to_exec()
        self.__request_to_exec = False
