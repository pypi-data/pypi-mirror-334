import inits
def selectionSort(arr: list,display=False):
    if not isinstance(arr,list):
        raise TypeError(f"Expected a list, but got {type(arr).__name__}")
    for i in range(len(arr)-1):
        min_index=i
        for j in range(i+1,len(arr)):
            if arr[min_index]>arr[j]:
                min_index=j
        if display:
            inits.chart(arr)
        if i!=min_index:
            arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

def bubbleSort(arr: list,display=False):
    if not isinstance(arr,list):
        raise TypeError(f"Expected a list, but got {type(arr).__name__}")
    for i in range(len(arr)):
        swapped=False
        for j in range(0,len(arr)-i-1):
            if arr[j]>arr[j+1]:
                arr[j+1],arr[j]=arr[j],arr[j+1]
                swapped=True
        if display:
            inits.chart(arr)
        if not swapped:
            break
    return arr

def insertionSort(arr: list,display=False):
    if not isinstance(arr,list):
        raise TypeError(f"Expected a list, but got {type(arr).__name__}")
    for i in range(1,len(arr)):
        key=arr[i]
        j=i-1
        while j>=0 and key<arr[j]:
            arr[j+1]=arr[j]
            j-=1
        arr[j+1]=key
        if display:
            inits.chart(arr)

    return arr

def merge(arr, left, mid, right,display):
    n1 = mid - left + 1
    n2 = right - mid
    L = [0] * n1
    R = [0] * n2
    for i in range(n1):
        L[i] = arr[left + i]
    for j in range(n2):
        R[j] = arr[mid + 1 + j]
    i = 0
    j = 0
    k = left
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1
    if display:
        inits.chart(arr)
def mergeSort(arr,left,right,display=False):
    if not isinstance(arr,list):
        raise TypeError(f"Expected a list, but got {type(arr).__name__}")
    if left < right:
        mid = (left + right) // 2

        mergeSort(arr, left, mid,display)
        mergeSort(arr, mid + 1, right,display)
        merge(arr, left, mid, right,display)
    return arr