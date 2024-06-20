from typing import List


def gen_build(generators):
    # converting generators to list
    generators_list = []
    for i in range(len(generators)):
        generators_list.append(generators[i])
    # converting numbers in generators to binary and slicing
    for i in range(len(generators_list)):
        generators_list[i] = bin(generators_list[i])
        generators_list[i] = generators_list[i][2:]
        # completing the binary so they would be the same length
    for i in range(len(generators_list)):
        generators_list[i] = generators_list[i].zfill(len(max(generators_list, key=len)))
    return generators_list


class ConvolutionalCode:
    """The code assumes zero state termination, and k=1"""

    def __init__(self, generators: tuple):
        self.generators = gen_build(generators)
        self.K = int(len(max(self.generators, key=len)) - 1)
        self.reg = ["0"] * self.K
        self.new_data_list = []
        self.status = self.dict_build()
        self.imp_list=[0*i for i in range(2**self.K)]

    def dict_build(self):
        graph_dict = {}
        bin_state_list = [bin(i)[2:].zfill(self.K) for i in range(2 ** self.K)]
        for i in bin_state_list:
            graph_dict[i] = [""]*2
            for b in range(2):
                for j in range(len(self.generators)):
                    num = 0
                    for k in range(self.K):
                        num += int(self.generators[j][k]) * int(i[k])
                    num += int(b) * int(self.generators[j][-1])
                    graph_dict[i][b] += str(num % 2)
        print(graph_dict)
        return graph_dict

    def str_dist(self, str1, str2):
        counter=0
        for i in range(len(str1)):
            if str1[i]!=str2[i]:
                counter+=1
        return counter


    def encode(self, data: bytes) -> List[int]:
        # converting bytes to binary
        data_bin = ''
        for i in range(len(data)):
            y = bin(data[i])[2:].zfill(8)
            data_bin += y
        # adding zeros to the end of data
        data_bin += self.K * "0"
        list = []
        # XORing
        for i in data_bin:
            for j in range(len(self.generators)):
                num = 0
                for k in range(self.K):
                    num += int(self.generators[j][-k-2]) * int(self.reg[k])
                num += int(i) * int(self.generators[j][-1])
                list.append(num % 2)
            self.reg.pop(-1)
            self.reg.insert(0, i)
        return list


    def decode(self, data: List[int]) -> (bytes, int):
        # splitting thr data to groups according the number of generators
        new_data = []
        temp_list=[-1 for h in range(2**self.K)]
        for i in range(0, len(data), len(self.generators)):
            group = data[i:i+len(self.generators)]
            new_data.append(''.join(str(n) for n in group))
        self.imp_list[0]=['', 0]
        for i in new_data:
            temp_list=[-1 for h in range(2**self.K)]
            for j in range(len(self.imp_list)):
                if self.imp_list[j]==0 or self.imp_list[j] == -1:
                    continue
                for k in range(2):
                    ind = int(bin(j)[2:].zfill(self.K)[1:]+str(k), 2)
                    val = self.imp_list[j][0]+str(k)
                    misti= self.imp_list[j][1]+self.str_dist(i, self.status[bin(j)[2:].zfill(self.K)][k])
                    if temp_list[ind]==-1:
                        temp_list[ind]= [val, misti]
                    else:
                        if misti<temp_list[ind][1]:
                            temp_list[ind]= [val, misti]
            self.imp_list=temp_list
        str1 = self.imp_list[0][0][0:-self.K:]
        lst1=[]
        for i in range(0, len(str1) // 8):
            lst1.append(int(str1[8*i:8*(i+1)], 2))
        print(bytes(lst1))
        return bytes(lst1), self.imp_list[0][1]
