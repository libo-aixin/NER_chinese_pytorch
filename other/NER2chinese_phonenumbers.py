#/usr/bin/env python3
#from  snownlp  import SnowNLP


# the first three digits of the phone number can only be one of the following list
phone = ['134','135','136','137','138','139','150','151','152','158','159','157','182','187','188','147',
        '130','131','132','155','156','185','186','133','153','180','189']

def NER2ch_phonenum(input_texts):
    '''
    chinese mobile phone number is an 11-digit number,and the first three digits need to meet the requirements in the list

    '''
    phone_nums = []
    if len(input_texts)>= 11:
        for i in range(len(input_texts)-10):
            line = input_texts[i:i+11]
            if line.isdigit() and line[:3] in phone:
#                print(f'{line} is a phone number')
                phone_nums.append(line)
            else:
                pass
#                print(f"{line} is not a phone number")
    else:
        print("don't detect a phone number")
    return phone_nums

def main():
    text = input('please enter some text :')
    chinese_phonenumber_list=NER2ch_phonenum(text)
    print(f'the content you entered is as follows {text} \n -------------')
    print(f'Recognized phone number as follows \n {chinese_phonenumber_list} \n ------------------------')
#    s=SnowNLP(text)
#    print(f'detect the word is {s.words}')
if __name__=="__main__":
    main()

