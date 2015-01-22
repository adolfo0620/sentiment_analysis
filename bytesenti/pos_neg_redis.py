import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

def import_words(file_name):
    final = set()
    with open (file_name) as inputfile:
        for line in inputfile:
            final.add(line.strip())
    return final

pos = import_words('positive-words.txt')
neg = import_words('negative-words.txt')

for word in pos:
    r.sadd('pos', word)

for word in neg:
    r.sadd('neg', word)