
class AltLogger:
    def __init__(self, src: str):
        self.src = src

    def fail(self, name):
        with open('logs/alt-{}.csv'.format(self.src), 'a+') as f:
            f.write('{}\n'.format(name))
            f.close()
