def import_words(file_name):
    final = set()
    with open (file_name) as inputfile:
        for line in inputfile:
            if line[0] is not ";":
                final.add(line.strip())
    return final

class Score():
    def __init__(self):
        self.positive = import_words('positive-words.txt')
        self.negative = import_words('negative-words.txt')
        self.pos = 0
        self.neg = 0

    def eval( self, text ):
        for word in self.positive:
            if word in text:
                self.pos += 1
        for word in self.negative:
            if word in text:
                self.neg += 1

print(import_words('positive-words.txt'))