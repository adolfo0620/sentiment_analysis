class Score():
    def __init__(self, string):
        self.positive = ['love','loved','like','liked','awesome','amazing','good','great','excellent', 'nice', 'sweet']
        self.negative = ['hate','hated','dislike','disliked','awful','terrible','bad','painful','worst', 'disgraceful', 'horrible']
        self.pos = 0
        self.neg = 0
        self.text = string

    def eval(self):
        for result in self.text['statuses']:
            for word in self.positive:
                if word in result['text']:
                    self.pos += 1
            for word in self.negative:
                if word in result['text']:
                    self.neg += 1