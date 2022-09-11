
class AltLogger:
    def __init__(self, src: str):
        self.src = src

    def fail(self, name, skin):
        with open('logs/alt-{}.csv'.format(self.src), 'a+') as f:
            f.write('{},{}\n'.format(name, skin))
            f.close()
