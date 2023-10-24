# creating the ui
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import time
from tkinter import messagebox
import json
import csv
import resource
import math
import heapq


def openflie():
    global donedata1
    opendfile = filedialog.askopenfilename()
    with open(opendfile, "r") as file:
        data = file.read()
    donedata1 = [int(x) for x in data.split(",")]
    return donedata1


def Bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def Selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def introsort_helper(data, start, end, maxdepth):
    if end - start <= 1:
        return

    if maxdepth == 0:
        # recursion depth limit exceeded, use heapsort instead
        heapq.heapify(data[start:end])
        return

    pivot = partition(data, start, end)
    introsort_helper(data, start, pivot, maxdepth - 1)
    introsort_helper(data, pivot+1, end, maxdepth - 1)


def Intro_Sort(data):
    maxdepth = 2 * (len(data)).bit_length()
    introsort_helper(data, 0, len(data), maxdepth)
    return data


def partition(data, start, end):
    pivot = data[start]
    i = start - 1
    j = end

    while True:
        i += 1
        while data[i] < pivot:
            i += 1

        j -= 1
        while data[j] > pivot:
            j -= 1

        if i >= j:
            return j

        data[i], data[j] = data[j], data[i]


def Merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        Merge_sort(left_half)
        Merge_sort(right_half)
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
    return arr


def Radix_Sort(arr):
    # Find the maximum number to know the number of digits
    max_num = max(arr)

    # Do counting sort for every digit
    exp = 1
    while max_num // exp > 0:
        counting_sort(arr, exp)
        exp *= 10


def counting_sort(arr, exp):
    n = len(arr)

    # The output array that will have sorted arr
    output = [0] * n

    # Initialize count array
    count = [0] * 10

    # Store count of occurrences in count[]
    for i in range(n):
        index = (arr[i] // exp)
        count[index % 10] += 1

    # Change count[i] so that count[i] now contains actual
    # position of this digit in output[]
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build the output array
    i = n - 1
    while i >= 0:
        index = (arr[i] // exp)
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    # Copy the output array to arr[], so that arr[] now
    # contains sorted numbers according to current digit
    for i in range(n):
        arr[i] = output[i]


def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[i] < arr[left]:
        largest = left
    if right < n and arr[largest] < arr[right]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def Heap_sort(arr):
    n = len(arr)
    for i in range(n//2-1, -1, -1):
        heapify(arr, n, i)
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr


def sort_and_save():
    selected_method = choice_list_box.get()
    data = donedata1
    if len(data) == 0:
        messagebox.showerror("Error", "Please select a file to sort.")
        return
    elif len(selected_method) == 0:
        messagebox.showerror("Error", "Please select a sorting method.")
        return
    # sort the data using the selected method and measure the time it takes
    elif selected_method == "Bubble_Sort":
        start_time = time.time()
        sorted_data = Bubble_sort(data)
        end_time = time.time()
    elif selected_method == "Selection_Sort":
        start_time = time.time()
        sorted_data = Selection_sort(data)
        end_time = time.time()
    elif selected_method == "Radix_Sort":
        start_time = time.time()
        sorted_data = Radix_Sort(data)
        end_time = time.time()
    elif selected_method == "Merge_Sort":
        start_time = time.time()
        sorted_data = Merge_sort(data)
        end_time = time.time()
    elif selected_method == "Intro_Sort":
        start_time = time.time()
        sorted_data = Intro_Sort(data)
        end_time = time.time()
    elif selected_method == "Heap_Sort":
        start_time = time.time()
        sorted_data = Heap_sort(data)
        end_time = time.time()
    else:
        messagebox.showerror("Error", "Please select 1 a sorting method.")
        return

    delimiter = ","
    sorted_str = delimiter.join(str(item) for item in sorted_data)

    # display the time taken to sort the data
    time_taken = end_time - start_time
    Timerun.config(text="Time taken: {} seconds".format(round(time_taken, 2)))
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # convert from bytes to megabytes
    usage_mb = usage / 1024 / 1024
    memorytab.config(text="Memory used: {} MB".format(round(usage_mb, 2)))

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    with open(file_path, "w") as file:
        file.write(sorted_str)

    messagebox.showinfo("Done", "The file is sorted and saved ")
    Timerun.config(text="")
    memorytab.config(text="")


window = tk.Tk()
window.geometry("700x500")
window.title("SORTED")

frameside = tk.LabelFrame(window, height=500, width=350, background="blue")
label = tk.Label(window, text="Welcome to Sorted ",
                 font=("arial", 35), bg="Blue")
label.place(x=10, y=20)
label2 = tk.Label(window, text="An experiment app allows you \nto choose a \n sorting algorithm and \n its sorts the data in \n the upload doucument and its shows\n the time the \n selected Algo took to sort the data ",
                  font=("arial", 18), bg="blue", )
label2.place(x=5, y=300)
frameside.pack(side="left")

buttonupload = tk.Button(window, text="Upload File", highlightbackground="red",
                         command=openflie, width=30, )
buttonupload.pack(pady=70)

Lablequest = tk.Label(window, text="Please Select a Method :")
Lablequest.pack(padx=50)


choices = ["Heap_Sort", "Intro_Sort", "Bubble_Sort",
           "Merge_Sort", "Radix_Sort", "Selection_Sort"]
choice_list_box = ttk.Combobox(window, values=choices)
choice_list_box.current(1)
choice_list_box.pack()

buttonsort = tk.Button(window, text="   SORT & SAVE   ",
                       width=25, highlightbackground="blue", command=sort_and_save)
buttonsort.pack(pady=100)

memorytab = tk.Label(window, text="fuck you")
memorytab.pack()
Timerun = tk.Label(window, text="fuck you2")
Timerun.pack()


window = tk.mainloop()
