import time
import tkinter as tk

# file i/o
def get_data(file_name='test.dat'):
    with open(file_name, 'r') as inf:
        raw_data = [line for line in inf.read().split('\n')]
    my_data = []
    for lines in raw_data:
        my_data.append([int(item) for item in lines])
    return my_data




if __name__ == "__main__":

    data = get_data()

    quickest = traverse_map(data)

    print(quickest)