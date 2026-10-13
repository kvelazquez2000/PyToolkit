class count_to_ten:
    def __init__(self):
        self.max = 10

    def __itef__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.max:
            