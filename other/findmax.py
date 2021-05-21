#/usr/bin/env python3


def find_max(list):
    mid_index = len(list)//2
    if list[mid_index-1] < list[mid_index]  and  list[mid_index] > list[mid_index+1]:
        print(f'find the max is {list[mid_index]} and index is {mid_index}')
        return mid_index
    elif list[mid_index] < list[mid_index+1]:
        if len(list)<=3:
            print(f'find the max is {list[mid_index+1]} and index is mid_index+1')
            return mid_index+1
        else:
            find_max(list[mid_index+1:])
    elif list[mid_index] < list[mid_index-1]:
        if len(list)<=3:
            print(f'find the max is {list[mid_index-1]} and index is {mid_index-1}')
            return mid_index-1
        else:
            find_max(list[:mid_index])
    else:
        print('input error')

if __name__=='__main__':
    input = input('please inter some list:')
    l= list(eval(input))
    find_max(l)





