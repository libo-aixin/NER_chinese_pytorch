# -*- coding:utf-8 -*-
'''
@Author: libo
@Date: 2021/5/15
'''
import copy
import pickle as cPickle
import torch

class DataManager():
    def __init__(self, max_length=1000, batch_size=20, data_type='train', tags=[]):
        self.index = 0
        self.input_size = 0
        self.batch_size = batch_size
        self.max_length = max_length
        self.data_type = data_type
        self.data = []
        self.batch_data = []
        self.vocab = {"unk": 0}
        self.tag_map = {"O":0,  "START":1, "STOP":2}
  
        # self.tag_map = {"O":0, 
        #                 "B-ADDR":1, "I-ADDR":2,'E-ADDR':3,
        #                 "B-BOOK":4, "I-BOOK":5,'E-BOOK':6,
        #                 "B-COMP":7, "I-COMP":8,'E-COMP':9,
        #                 "B-GAME":10,"I-GAME":11,'E-GAME':12,
        #                 "B-GOVE":13,"I-GOVE":14,'E-GOVE':15,
        #                 "B-MOVE":16,"I-MOVE":17,'E-MOVE':18,
        #                 "B-NAME":19,'I-NAME':20,'E-NAME':21,
        #                 'B-ORGN':22,'I-ORGN':23,'E-ORGN':24,
        #                 'B-POSI':25,'I-POSI':26,'E-POSI':27,
        #                 'B-SCEN':28,'I-SCEN':29,'E-SCEN':30,
        #                 "S":31}


        if data_type == "train":
            assert tags, Exception("请指定需要训练的tag类型，如[\"ORG\", \"PER\"]")
            self.generate_tags(tags)
            self.data_path = "data/NER_train"
        elif data_type == "dev":
            self.data_path = "data/NER_dev"
            self.load_data_map()
        elif data_type == "test":
            self.data_path = "data/test"
            self.load_data_map()

        self.load_data()
        self.prepare_batch()

    def generate_tags(self, tags):
        self.tags = []
        for tag in tags:
            for prefix in ["B-", "I-", "E-"]:
                self.tags.append(prefix + tag)
        self.tags.append("O")

    def load_data_map(self):
        with open("models/data.pkl", "rb") as f:
            self.data_map = cPickle.load(f)
            print(f'show datapkl{self.data_map}')
            self.vocab = self.data_map.get("vocab", {})
            print(f'vocab is show {self.vocab}')
            self.tag_map = self.data_map.get("tag_map", {})
            self.tags = self.data_map.keys()

    def load_data(self):
        # load data
        # add vocab
        # covert to one-hot
        sentence = []
        target = []
        with open(self.data_path,errors='ignore') as f:
            for line in f:
                line = line[:-1]
                if line == "end":
                    self.data.append([sentence, target])
                    sentence = []
                    target = []
                    continue
                try:
                    word, tag = line.split(" ")
                except Exception:
                    continue
                if word not in self.vocab and self.data_type == "train":
                    self.vocab[word] = max(self.vocab.values()) + 1 
                if tag not in self.tag_map and self.data_type == "train" and tag in self.tags:
                    self.tag_map[tag] = len(self.tag_map.keys())
                sentence.append(self.vocab.get(word, 0))
                print(f'sentence is {self.vocab.get(word,0)}') 
                target.append(self.tag_map.get(tag, 0))
        self.input_size = len(self.vocab.values())
        print("{} data: {}".format(self.data_type ,len(self.data)))
        print("vocab size: {}".format(self.input_size))
        print("unique tag: {}".format(len(self.tag_map.values())))
        print("-"*50)
    
    def convert_tag(self, data):
        # add E-XXX for tags
        # add O-XXX for tags
        _, tags = data
        converted_tags = []
        for _, tag in enumerate(tags[:-1]):
            if tag not in self.tag_map and self.data_type == "train":
                self.tag_map[tag] = len(self.tag_map.keys())
            converted_tags.append(self.tag_map.get(tag, 0))
        converted_tags.append(0)
        data[1] = converted_tags
        assert len(converted_tags) == len(tags), "convert error, the list dosen't match!"
        return data

    def prepare_batch(self):
        '''
            prepare data for batch
        '''
        index = 0
        while True:
            if index+self.batch_size >= len(self.data):
                pad_data = self.pad_data(self.data[-self.batch_size:])
                self.batch_data.append(pad_data)
                break
            else:
                pad_data = self.pad_data(self.data[index:index+self.batch_size])
                index += self.batch_size
                self.batch_data.append(pad_data)
    
    def pad_data(self, data):
        c_data = copy.deepcopy(data)
        print(f'show me the {c_data}')
        max_length = max([len(i[0]) for i in c_data])
        for i in c_data:
            i.append(len(i[0]))
            i[0] = i[0] + (max_length-len(i[0])) * [0]
            i[1] = i[1] + (max_length-len(i[1])) * [0]
            # i[0] = torch.tensor(i[0])
            # i[1] = torch.tensor(i[1])
        return c_data

    def iteration(self):
        idx = 0
        while True:
            yield self.batch_data[idx]
            idx += 1
            if idx > len(self.batch_data)-1:
                idx = 0

    def get_batch(self):
        for data in self.batch_data:
            yield data
