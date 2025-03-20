import random
from transformations import concatenate
import matplotlib.pyplot as plt

def empty(dimensions:list[int], datatype: type):
    if not isinstance(dimensions, list):
        raise TypeError(f"Expected type 'list[int]', but got type {type(dimensions).__name__}")
    else:
        if not all(isinstance(d, int) for d in dimensions):
            raise TypeError(f"Expected type 'list[int]', but got some non-int value")
    if not isinstance(datatype,type):
        raise TypeError(f"Expected type 'type', but got {type(datatype).__name__}")
    if len(dimensions) == 1:
        return [datatype() for _ in range(dimensions[0])]
    else:
        return [empty(dimensions[1:], datatype) for _ in range(dimensions[0])]

def uniform_fill(dimensions:list[int], value):
    if not isinstance(dimensions, list):
        raise TypeError(f"Expected type 'list[int]', but got type {type(dimensions).__name__}")
    else:
        if not all(isinstance(d, int) for d in dimensions):
            raise TypeError(f"Expected type 'list[int]', but got some non-int value")
    if len(dimensions) == 1:
        return [value for _ in range(dimensions[0])]
    else:
        return [uniform_fill(dimensions[1:], value) for _ in range(dimensions[0])]

def randoms(length,datatype,minimum=-100,maximum=100):
    arr=[]
    if datatype in [int,float,complex]:
        for _ in range(length):
            arr.append(random.randint(minimum,maximum))
    if datatype==str:
        for _ in range(length):
            st=''
            for _ in range(random.randint(1,10)):
                st+=random.choice([chr(random.randint(65,90)),chr(random.randint(97,122))])
            arr.append(st)
    if datatype==bool:
        for _ in range(length):
            arr.append(random.choice([True,False]))
    if datatype==dict:
        for _ in range(length):
            arr.append({concatenate(randoms(1,str)):str(random.randint(-100,100))})
    if datatype==list:
        for _ in range(length):
            x=[]
            for _ in range(random.randint(1, 10)):
                x.append(concatenate(randoms(1,str)))
            arr.append(x)
    if datatype==tuple:
        for _ in range(length):
            x=[]
            for _ in range(random.randint(2, 5)):
                x.append(concatenate(randoms(1,int)))
            arr.append(tuple(x))
    if datatype==range:
        for _ in range(length):
            for _ in range(2):
                arr.append(range(random.randrange(0,100)))
    if datatype==set:
        for _ in range(length):
            arr.append({concatenate(randoms(1, str)): str(random.randint(-100, 100))})
    return arr

def chart(arr):
    plt.ion()
    plt.clf()
    graph = plt.plot(list(range(len(arr))), arr)
    plt.pause(0.000001)
