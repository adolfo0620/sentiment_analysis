def import_words(file_name):
    final = set()
    with open (file_name) as inputfile:
        for line in inputfile:
            final.add(line.strip())
    return final

class Score():
    def __init__(self):
        self.positive = import_words('../sa_api/positive-words.txt')
        self.negative = import_words('../sa_api/negative-words.txt')
        self.pos = 0
        self.neg = 0

    def eval( self, text ):
        words = text.split(' ')
        to_dict = {}
        for word in words:
            if word in to_dict:
                to_dict[word] += 1
            else:
                to_dict[word] = 1
        for word in to_dict:
            if word in self.positive:
                self.pos += to_dict[word]
        for word in to_dict:
            if word in self.negative:
                self.neg += to_dict[word]
        return True


### Test ###
# a = Score()

# a.eval("bad bad terrible happy")

# print(a.pos)
# print(a.neg)