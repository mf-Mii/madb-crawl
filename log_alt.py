

class AltLogger:
    def __init__(self, src: str):
        self.src = src

    def fail(self, name):
        with open('log/alt-{}.csv', 'a') as f:
            f.write('{}\n'.format(name))