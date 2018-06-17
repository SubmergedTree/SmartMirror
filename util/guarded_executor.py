from PyQt5.QtCore import QMutex


class GuardedExecutor:
    def __init__(self, to_exec):
        self.__to_exec = to_exec
        self.__locked = False
        self.__request_to_exec = False
        self.__mutex = QMutex()

    def lock(self):
        self.__mutex.lock()
        self.__locked = True
        self.__mutex.unlock()

    def unlock(self):
        self.__mutex.lock()
        self.__locked = False
        if self.__request_to_exec:
            self.__exec()
        self.__mutex.unlock()


    def try_to_exec(self):
        self.__mutex.lock()
        if self.__locked:
            self.__request_to_exec = True
        else:
            self.__exec()
        self.__mutex.unlock()

    def __exec(self):
        self.__to_exec()
        self.__request_to_exec = False
