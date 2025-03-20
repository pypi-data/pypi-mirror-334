import inits
import math

def flatten(arr):
    if not isinstance(arr,list):
        raise TypeError(f"Expected a list, but got {type(arr).__name__}")
    a=[]
    for element in arr:
        if isinstance(element,list):
            a.extend(flatten(element))
        else:
            a.append(element)
    return a

def sliding_window(arr,win_size):
    if not isinstance(arr,list):
        raise TypeError(f"Expected a list, but got {type(arr).__name__}")
    return list(arr[i:i+win_size] for i in range(len(arr)-win_size+1))

def reverse(arr):
    if not isinstance(arr,list):
        raise TypeError(f"Expected a list, but got {type(arr).__name__}")
    return arr[::-1]

def concatenate(arr) -> str:
    if not isinstance(arr,list):
        raise TypeError(f"Expected a list, but got {type(arr).__name__}")
    a = ''
    for element in arr:
        if isinstance(element, list):
            a+=str(concatenate(element))
        else:
            a+=str(element)
    return a

def chunk(arr,chunk_size=-1,chunk_quantity=-1): #Could be optimized to work with non-factors
    if not isinstance(arr,list):
        raise TypeError(f"Expected a list, but got {type(arr).__name__}")
    if (chunk_size!=-1 and not chunk_quantity==-1) or (chunk_size==-1 and not chunk_quantity!=-1):
        raise ValueError("Must define only either chunk size or chunk quantity")
    chunks=[]
    if chunk_size!=-1:
        for i in range(math.ceil(len(arr)/chunk_size)):
            chunks.append(arr[i*chunk_size:(i+1)*chunk_size])
        return chunks
    if chunk_quantity!=-1:
        for i in range(chunk_quantity):
            chunks.append(arr[math.ceil(len(arr)/chunk_quantity)*i:(i + 1) * math.ceil(len(arr)/chunk_quantity)])
        return chunks

def remove_duplicates(arr):
    if not isinstance(arr,list):
        raise TypeError(f"Expected a list, but got {type(arr).__name__}")
    return list(dict().fromkeys(arr))

def zip_arrays(arr1,arr2):
    if not isinstance(arr1,list) and not isinstance(arr2,list):
        raise TypeError(f"Expected lists, but got {type(arr1).__name__}, {type(arr2).__name__}")
    return list(zip(arr1,arr2))