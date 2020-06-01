
class MyExcepetion(Exception):

    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


if __name__ == '__main__':
    e = MyExcepetion('Something wrong with the brand file', Exception)
    raise e

