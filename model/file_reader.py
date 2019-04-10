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
    
    def read_v2(self, path):
        with open(path, "r", encoding='utf-8') as fp:
            data = []
            label = []
            for line in fp.readlines():
                if re.search("\,\s[\-]?[0-2]$", line):
                    sentence_elements = line.split(",")
                    if int(sentence_elements[-2].replace("\n", "").strip()) != 0:
                        data.append(",".join(sentence_elements[0: -2]))
                        label.append(int(sentence_elements[-1].replace("\n", "").strip()))
        
        return data, label


if __name__ == "__main__":
    data, label = file_reader().read_v2("test.txt")
    print(data)
    print(label)
    print(len(data))
    print(len(label))

