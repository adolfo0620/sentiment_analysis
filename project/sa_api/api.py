
class Score():
    def __init__(self):
        self.positive = ['love','loved','like','liked','awesome','amazing','good','great','excellent', 'nice', 'sweet']
        self.negative = ['hate','hated','dislike','disliked','awful','terrible','bad','painful','worst', 'disgraceful', 'horrible']
        self.pos = 0
        self.neg = 0
    
    def eval( self, text ):
        for word in self.positive:
            if word in text:
                self.pos += 1
        for word in self.negative:
            if word in text:
                self.neg += 1