class Loader:
    def __init__(self, fileName):
        self.fileName = fileName

    def loadReads(self):
        f = open(self.fileName, 'r')
        reads = []

        for line in f:
            reads.append(line.rstrip("\n"))

        return reads