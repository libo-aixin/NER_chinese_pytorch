# chinsesNER-pytorch

### train

setp 1: edit **models/config.yml**

    embedding_size: 100
    hidden_size: 128
    model_path: models/
    batch_size: 20
    dropout: 0.5
    tags:
      - organization
      - name
      - address
      - company
      - government
      - book
      - game
      - movie 
      - position
      - scene
      - chinese_political_party 

step 2: train

    python3 main.py train
    

### predict

    python3 main.py predict
    
    请输入文本: 中国农业发展银行近日联合下发通知，中国电竞运动中心自成立以来，在国家体育总局、北京市和石景山区相关部门的大力支持下
    [{'start': 39, 'stop': 42, 'word': '北京市', 'type': 'address'}, {'start': 43, 'stop': 51, 'word': '石景山区相关部门', 'type': 'address'}, {'start': 52, 'stop': 57, 'word': '大力支持下', 'type': 'address'}, {'start': 0, 'stop': 8, 'word': '中国农业发展银行', 'type': 'company'}, {'start': 32, 'stop': 38, 'word': '国家体育总局', 'type': 'government'}]
### test
    python3 main.py test
    
    show the predict label
    model restore success!
        eval
        organization    recall 0.33     precision 0.17  f1 0.22
        name    recall 0.50     precision 0.75  f1 0.60
        address recall 0.38     precision 0.40  f1 0.39
        company recall 0.67     precision 0.57  f1 0.62
        government      recall 0.33     precision 0.50  f1 0.40
        book    recall 0.50     precision 1.00  f1 0.67
        game    recall 0.80     precision 1.00  f1 0.89
        movie   recall 0.50     precision 0.40  f1 0.44
        position        recall 0.75     precision 0.67  f1 0.71
        scene   recall 0.60     precision 0.60  f1 0.60
        chinese_political_party recall 0.00     precision 0.00  f1 0.00
    

### REFERENCES
- [Log-Linear Models, MEMMs, and CRFs](http://www.cs.columbia.edu/~mcollins/crf.pdf)
- [Neural Architectures for Named Entity Recognition](https://arxiv.org/pdf/1603.01360.pdf)
