class count_to_ten:
    def __init__(self):
        self.max = 10

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.max:
            self.n +=1
            return self.n
        else:
            raise StopIteration

count_obj = count_to_ten()
count_iter = iter(count_obj)

for i in count_iter:
        print(i)

def reverse_str(str):
     for i in range(len(str)-1,-1,-1):
          yield str[i]

for char in reverse_str("hello"):
     print(char)