def find_all(arr,x):
    if not isinstance(arr, list):
        raise TypeError(f"Expected a list, but got {type(arr).__name__}")
    indices=[]
    for i in range(len(arr)):
        if arr[i]==x:
            indices.append(i)
    return indices

def find_nth(arr,x,n):
    if not isinstance(arr, list):
        raise TypeError(f"Expected a list, but got {type(arr).__name__}")
    found=0
    for i in range(len(arr)):
        if arr[i]==x:
            found+=1
            if found==n:
                return i
    return -1

def find_unique(arr):
    if not isinstance(arr,list):
        raise TypeError(f"Expected a list, but got {type(arr).__name__}")
    return list(set(arr))

def find_nth_highest(arr,n):
    if not isinstance(arr,list):
        raise TypeError(f"Expected a list, but got {type(arr).__name__}")
    return sorted(arr)[(-1*n)]

def find_nth_lowest(arr,n):
    if not isinstance(arr,list):
        raise TypeError(f"Expected a list, but got {type(arr).__name__}")
    return sorted(arr)[(n-1)]

def find_intersections(arr1,arr2):
    if not isinstance(arr1,list) and not isinstance(arr2,list):
        raise TypeError(f"Expected lists, but got {type(arr1).__name__}, {type(arr2).__name__}")
    return list(set(arr1) & set(arr2))