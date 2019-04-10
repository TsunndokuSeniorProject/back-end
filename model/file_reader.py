import re

class file_reader:
    def read(self, path):
        with open(path, "r", encoding='utf-8') as fp:
            data = []
            label = []
            for line in fp.readlines():
                if re.search("\,\s[\-]?\d$", line) and re.search(r'[^\x00-\x7F]+', line) == None:
                    sentence_elements = line.split(",")
                    if int(sentence_elements[-2].replace("\n", "").strip()) in [1, 2, 3]:
                        data.append(",".join(sentence_elements[0: -2]))
                        label.append(int(sentence_elements[-2].replace("\n", "").strip()))

        return data, label
    
    def read_v2(self, path, position, num_of_lab):
        with open(path, "r", encoding='utf-8') as fp:
            data = []
            label = []
            
            for line in fp.readlines():
                if re.search("\,\s[\-]?[\d]$", line):
                    sentence_elements = line.split(",")
                    checker = sentence_elements[:]
                    checker.reverse()
                    count = 0
                    for i in range(0, len(checker)):
                        if type(checker[i]) is int:
                            count += 1
                    if count == num_of_lab:
                        if int(sentence_elements[(-1*position)].replace("\n", "").strip()) != 0:
                            data.append(",".join(sentence_elements[0: (-1*position)]))
                            label.append(int(sentence_elements[-1].replace("\n", "").strip()))
        
        return data, label


if __name__ == "__main__":
    data, label = file_reader().read_v2("test.txt")
    print(data)
    print(label)
    print(len(data))
    print(len(label))

