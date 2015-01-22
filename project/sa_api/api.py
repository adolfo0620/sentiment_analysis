import re, string
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

regex = re.compile('[%s]' % re.escape(string.punctuation))

class Score():
    def __init__(self):
        self.pos = 0
        self.neg = 0

    def eval( self, text ):
        words = text.split(' ')
        to_dict = {}
        for word in words:
            word = regex.sub('', word).lower()       
            if word in to_dict:
                to_dict[word] += 1
            else:
                to_dict[word] = 1
        for word in to_dict:
            if r.sismember('pos', word) == 1:
                self.pos += to_dict[word]
            elif r.sismember('neg', word) == 1:
                self.neg += to_dict[word]
        return True

if __name__ == "__main__":
    a = Score()

    a.eval("bad bad terrible.. #happy")

    print(a.pos)
    print(a.neg)