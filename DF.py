class DF:
    def __init__(self,l,r):
        self.l=l
        self.r=r

    def getV(self):
        return self.r

    def getK(self):
        return self.l

    def __str__(self):
        return str(self.l)+"->"+str(self.r)

    def __repr__(self):
            return str(self.l)+"->"+str(self.r)