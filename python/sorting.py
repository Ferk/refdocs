#!/usr/bin/python
#
####################################
# Properties of sorting algorithms #
####################################
#
#
# Adaptative
# ----------
# Takes advantage of existing order in its input.
# It benefits from the presortedness in the input sequence – or a limited amount
# of disorder for various definitions of measures of disorder – and sorts faster.
#
#
# Stable
# ------
# Does not change the relative order of elements with equal keys
#
# In-place
# --------
# Only needs a constant amount O(1) of additional memory space.
# The input is usually overwritten by the output as the algorythm executes.
#
# Online
# ------
# Can sort a list as it receives it
#
######


########################
### Quicksort
########################
#
# time complexity: O( n log(n) )
#


#
# Quicksort for lists
#

def qsort(list):
    """
    Quicksort using list comprehensions
    >>> qsort1<<docstring test numeric input>>
    <<docstring test numeric output>>
    >>> qsort1<<docstring test string input>>
    <<docstring test string output>>
    """
    if list == []: 
        return []
    else:
        pivot = list[0]
        lesser = qsort1([x for x in list[1:] if x < pivot])
        greater = qsort1([x for x in list[1:] if x >= pivot])
        return lesser + [pivot] + greater


#
# Quicksort for arrays
#

def partition(a, start, end, pivotIndex):
    """In-place partition function.

    It will shuffle the elements of the array in such a way that the
    selecte pivot will end up in the right ordered final position,
    this means all the elements at its left will be lower than the
    pivot, and all the elements to the right will be higher.

    The most common approach is to take two positions: one moving up
    from the start and other moving down from the end, searching for
    the first higher value from the lower partition and the first
    lower value from the high partition. Then they are exchanged.
    """
    low = start
    high = end - 1  # After we remove pivot it will be one smaller
    pivotValue = a[pivotIndex]
    # remove pivot (it will be added back to the center when we finish)
    a[pivotIndex] = a[end]
    while True:
        while low <= high and a[low] < pivotValue:
            low = low + 1
        while low <= high and a[high] >= pivotValue:
            high = high - 1
        if low > high:
            break
        a[low], a[high] = a[high], a[low]
    # insert pivot into final position and return final position
    a[end] = a[low]
    a[low] = pivotValue
    return low


def qsort(a, start, end):
    """Will select a random pivot and do partition operations recursivelly on
    each of the 2 resulting ranges. 

    The subpartitions will be smaller every call, if we keep going until the size
    is 1 or 0, that whole branch of array ranges will have been sorted.

    average time complexity: O( n log(n) )

    However, in this implementation we fallback to using the 'insertionsort'
    algorithm when the size is less than 32."""
    if end - start + 1 < 32:
        insertionSort(a, start, end)
    else:
        pivotIndex = partition(a, start, end, randint(start, end))
        qsortRange(a, start, pivotIndex - 1)
        qsortRange(a, pivotIndex + 1, end)
    return a

########################
### Insertionsort
########################
#
# time complexity: O(n + d) where d is number of inversions (adaptive)
#
# http://upload.wikimedia.org/wikipedia/commons/0/0f/Insertion-sort-example-300px.gif
#

def insertionSort(a, start, end):
    """Simple sorting algorithm. Sorts one item at a time.

    time complexity: O(n + d) where d is number of inversions (adaptive)

    Much less efficient on large sets than quicksort, heapsort, or merge sort.
    But it's better than O(n^2) like bubble sort or selection sort.

    On a repetition, insertion sort removes one element from the input
    data, finds the location it belongs within the sorted list, and
    inserts it there. It repeats until no input elements remain.

    Sorting is typically done in-place, by iterating up the array,
    growing the sorted list behind it. At each array-position, it
    checks the value there against the largest value in the sorted
    list (which happens to be next to it, in the previous
    array-position checked). If larger, it leaves the element in place
    and moves to the next. If smaller, it finds the correct position
    within the sorted list, shifts all the larger values up to make a
    space, and inserts into that correct position.

    The resulting array after k iterations has the property where the
    first k + 1 entries are sorted ("+1" because the first entry is
    skipped). In each iteration the first remaining entry of the input is
    removed, and inserted into the result at the correct position, thus
    extending the result.
    """
    for i in xrange(start, end + 1):
        # Insert a[i] into the sorted sublist
        v = a[i]
        for j in xrange(i-1, -1, -1):
            if a[j] <= v:
                a[j + 1] = v
                break
            a[j + 1] = a[j]
        else:
            a[0] = v
    return a

    
########################
### Mergesort
########################
#
# time complexity: O( n log(n) )
#
# This is a very illustrative animation:
# http://upload.wikimedia.org/wikipedia/commons/c/cc/Merge-sort-example-300px.gif
#
# 1. Divide the unsorted list into two sublists of about half the size
# 2. Sort each of the two sublists
# 3. Merge the two sorted sublists back into one sorted list.
#

def merge(left, right):
    """Merges two sublists into an ordered list.

    On each iteration we copy the smaller value between the two
    indexes we keep for each list and then advance the index for that
    list.

    When we reach the end of one of the lists, we just copy the
    remainder portion.

    """
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    # Add remainders. One of them will be empty, but it's ok
    result += left[i:]
    result += right[j:]
    return result
            
def mergesort(lst):
    """Divides into into two sublists and recurse on them separately.
    Then it merges the returned resulting lists using  merge().

    The recursive call just further splits until there's only 1
    element in the list, which is returned.

    Since merging two lists of 1 element each will order them, and
    merging two already ordered list will produce an ordered result,
    then we will always end up with an ordered list.

    """    
    if len(lst) <= 1:
        return lst
    middle = int(len(lst) / 2)
    left = mergesort(lst[:middle])
    right = mergesort(lst[middle:])
    return merge(left, right)
            

########################
### Heapsort
########################
#
# In the first step, a heap is built out of the data.
#
# A heap is a tree where the child nodes always satisfy the same condition
# with respect to the parent (eg. all childs of a node will be smaller than
# the parent node, so the root will always hold the highest value)
#
# In the second step, a sorted array is created by repeatedly removing
# the largest element from the heap, and inserting it into the
# array. The heap is reconstructed after each removal. Once all
# objects have been removed from the heap, we have a sorted array. The
# direction of the sorted elements can be varied by choosing a
# min-heap or max-heap in step one.
#
# Heapsort can be performed in place. The array can be split into two
# parts, the sorted array and the heap. The storage of heaps as arrays
# is diagrammed here. The heap's invariant is preserved after each
# extraction, so the only cost is that of extraction.
#

def Heapify( A, i, n ):
    """Maintains the heap property in the binary tree.
    Runs in O( logn ).
    """
    l = Left( i )
    r = Right( i )
    if l  A[ i ]: largest = l
    else: largest = i
    if r  A[ largest ]:
        largest = r
    if largest != i:
        A[ i ], A[ largest ] = A[ largest ], A[ i ]
        Heapify( A, largest, n )


def HeapLength( A ): return len( A ) - 1
def BuildHeap( A ): 
    """BuildHeapSort procedure, which runs in O( n ), produces a heap from an
    unordered input array.It uses the Heapify procedure in a bottom-up manner
    from the element to the index n/2 to 1(the root), where n is the length
    of the array.
    """
    n = HeapLength( A )
    for i in range( n/2 ,0 ,-1 ):
        Heapify( A, i, n )
# 
def HeapSort( A ):
    """
    Runs in O( n logn ). 
    The first step in this procedure use the BuildHeapSort subroutine to build
    a heap given an input array and then use the Heapify procedure to mantain
    the heap property.
    """
    BuildHeap( A )
    HeapSize = HeapLength( A )
    for i in range( HeapSize, 1 , -1 ):
        A[ 1 ],A[ i ] = A[ i ],A[ 1 ]
        HeapSize = HeapSize-1 
        Heapify( A,1,HeapSize )

