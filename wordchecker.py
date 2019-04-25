
class WordBank:
    dictionary = {}
    f = open("C:\\Users\\hp\\Desktop\\ScrabbleTester\\wordsEn.txt", "r")
    word = ""
    v = f.read(1)
    while v:
        if not v == " ":
            if v == ",":
                if len(word) <= 15:
                    dictionary[word] = 1
                word = ""
            else:
                word += v
        v = f.read(1)

    def check(self, string):
        return string in self.dictionary


w = WordBank()
print(len(w.dictionary))
