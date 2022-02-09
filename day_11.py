import time
from random import randint
from tkinter import *
import tkinter as tk

# global counter for flashes
flash_count = 0
delay = 1
reset_flag = False


# file i/o
with open("day_11.dat", "r") as inf:
    raw_data = [line for line in inf.read().split('\n')]
# print(raw_data)
# process raw data to 2d array
grid = []
for items in range(len(raw_data)):
    grid.append([*raw_data[items]])
del raw_data, items
# print(grid)


def update_grid(my_grid):
    # print("Updating string...", end=" ")
    lb_board['text'] = get_string(my_grid)
    # print("Packing board...")
    lb_board.pack()
    lb_board.update()
    time.sleep(delay)


def check_flash(my_grid):
    for i in range(len(my_grid)):
        for j in range(len(my_grid[i])):
            # if the current cell has already flashed, skip comparisons here
            if my_grid[i][j] == '*':
                continue
            # if the current cell is needing to flash, do so
            if int(my_grid[i][j]) >= 10:
                lb_flash_count['text'] = int(lb_flash_count['text']) + 1
                fr_flash_count.update()
                my_grid[i][j] = '*'
                # increase all neighbors
                for foo in range(-1, 2):
                    for bar in range(-1, 2):
                        # if we are looking at negative indexes skip
                        if foo + i < 0 or bar + j < 0:
                            # print(i + foo, j + bar, "is oob")
                            continue
                        # if we are looking at ourselves, skip
                        if foo == 0 and bar == 0:
                            continue
                        try:
                            # print(i + foo, j + bar, my_grid[i + foo][j + bar])
                            my_grid[i + foo][j + bar] = int(my_grid[i + foo][j + bar]) + 1
                        except IndexError:
                            # if we are looking out the end of the array, skip
                            # print(i + foo, j + bar, "is oob")
                            continue
                        except ValueError:
                            # if we tried to add to a *, skip
                            # print("Can't add to flash")
                            continue

                # print("\nTrying to update visuals cf")
                # if I am doing more than 100 steps, don't animate the flashes
                if int(lb_iterations_count['text']) < 100:
                    update_grid(my_grid)

                my_grid = check_flash(my_grid)
                # recursive call to check flash

    # return all * to 0
    for i in range(len(my_grid)):
        for j in range(len(my_grid[i])):
            if my_grid[i][j] == '*':
                my_grid[i][j] = '0'

    # return finished grid
    return my_grid


def get_string(my_grid):
    # print("In Get String")
    # define empty string
    my_string = ""
    # loop through data in my_grid
    for i in range(len(my_grid)):
        for j in range(len(my_grid[i])):
            try:
                # if the item is interpreted as an int continue here
                if int(my_grid[i][j]) >= 10:
                    # if the integer is >= 10, display as a 0 for formatting of the string
                    my_string += '0'
                else:
                    # if the integer is single digit append to string
                    my_string += str(my_grid[i][j])
            except ValueError:
                # if the item is character (it's a '*') then display as 0 for formatting
                my_string += '0'
        # add end line to keep string as grid while displaying
        my_string += "\n"

    # # print(my_string)
    return my_string


def show_loop(my_list):
    # print(my_list)
    # print(my_list[0])

    # variables for frame count rectangle
    current_frame = 0
    end_frame = len(my_list)

    loop_popup = Toplevel(root)
    fr_loop_popup = tk.Frame(loop_popup,
                             bg="white",
                             width=500,
                             height=300,
                             border="5"
                             )

    # game board assignments
    fr_loop_board = tk.Frame(fr_loop_popup,
                             relief=tk.RAISED,
                             height=400,
                             border=6)
    lb_loop_board = tk.Label(fr_loop_board,
                             width=25,
                             text="{}".format(my_list[0])
                             )

    lb_loop_board.pack()
    fr_loop_board.grid(row=0, column=0, sticky="nsew")

    # frame count space
    fr_frame_count = tk.Frame(fr_loop_popup, height="50", border=3)
    canvas = Canvas(fr_frame_count, height=45, width=480)
    canvas.create_rectangle(5, 5, 475, 40, fill="orange")
    canvas.pack()
    lb_frame_current = tk.Label(fr_frame_count, text='0 of {}'.format(end_frame))
    lb_frame_current.pack()
    fr_frame_count.grid(row=1, column=0, sticky="ew")

    # close button
    fr_buttons = tk.Frame(fr_loop_popup, height="100")
    bt_close = tk.Button(fr_buttons, text="close", command=loop_popup.destroy)
    bt_close.pack()
    fr_buttons.grid(row=2, column=0, sticky="nsew")
    fr_loop_popup.pack()

    # determine frame rate
    if len(my_list) < 15:
        frame_rate = .5
    else:
        frame_rate = .25

    while True:
        for strings in my_list:
            # update board
            lb_loop_board['text'] = strings
            lb_loop_board.update()

            # update progress bar
            current_frame += 1
            # avoid "frame 0" bug
            if int(current_frame % end_frame) == 0:
                current_bar_length = 475
            else:
                current_bar_length = int(((current_frame % end_frame) / end_frame) * 475)
            # print('{}/{}, {}'.format(current_frame, end_frame, int(((current_frame % end_frame) / end_frame) * 475)))
            canvas.delete('all')
            canvas.create_rectangle(5, 5, current_bar_length, 40, fill="green")
            canvas.update()
            # avoid "frame 0" bug
            if int(current_frame % end_frame) == 0:
                lb_frame_current['text'] = "{} of {}".format(end_frame, end_frame)
            else:
                lb_frame_current['text'] = "{} of {}".format((current_frame % end_frame), end_frame)
            lb_frame_current.update()

            # timer for frame rate
            time.sleep(frame_rate)


def loop_warning(my_looping_list):
    popup = Toplevel(root)

    # define contents of window
    fr_popup = tk.Frame(popup,
                        bg="white",
                        border=5
                        )
    lb_warning = tk.Label(fr_popup,
                          bg="white",
                          height=3,
                          text="I think I'm in an infinite loop. I've exited"
                          )
    lb_warning_details = tk.Label(fr_popup,
                                  bg="white",
                                  height=3,
                                  text="I think it starts {} frames ago.".format(len(my_looping_list))
                                  )
    bt_showme = tk.Button(fr_popup, height=3,
                          width=5,
                          text="Show me",
                          command=lambda arg1=my_looping_list: show_loop(arg1)
                          )
    bt_warning = tk.Button(fr_popup,
                           height=3,
                           width=5,
                           text="OK",
                           command=popup.destroy
                           )

    # grid and pack contents
    lb_warning.grid(row=0, columnspan=3)
    lb_warning_details.grid(row=2, columnspan=3)
    bt_showme.grid(row=3, column=2)
    bt_warning.grid(row=3, column=3)
    fr_popup.pack()


def adv_one(my_grid=None, iterations=1):
    if my_grid is None:
        print("Error in data, empty array!")
        return
    # set the global frame rate from the lb_iterations_count
    lb_iterations_count['text'] = iterations
    # set the delay for the animation, the more iterations, the faster it goes
    global delay
    delay = (1 / (iterations * 10))
    # create empty list for infinite loop check
    loop_check = []
    # repeat the adv one for iterations times
    for runs in range(iterations):
        # print("Advancing one")
        lb_iterations['text'] = int(lb_iterations['text']) + 1
        for i_ao in range(len(my_grid)):
            for j in range(len(my_grid[i_ao])):
                my_grid[i_ao][j] = int(my_grid[i_ao][j]) + 1
                # print(my_grid[i][j], end="")
            # print()
        my_grid = check_flash(my_grid)
        # print("\nTrying to update visuals adv1")

        # loop check here
        new_string = get_string(my_grid)
        if new_string in loop_check:
            update_grid(my_grid)
            # print("Found matching loop!")
            # I think I found a loop. create a new list of the looped items
            looped_list = []
            beg_index = loop_check.index(new_string)
            end_index = len(loop_check)
            for i_ao in range(beg_index, end_index):
                looped_list.append(loop_check[i_ao])
            loop_warning(looped_list)
            break
        else:
            loop_check.append(new_string)
            # print("Archiving string at", len(loop_check))

        # if we are looking at more than 100 steps, only update every 20 frames
        if iterations <= 100:
            update_grid(my_grid)
        else:
            if runs % 20 == 0:
                update_grid(my_grid)

        # if all flashes are lined up, exit loop
        # print("Flashes this turn:", end="")
        turn_total = 0
        for i_ao in range(len(my_grid)):
            turn_total += my_grid[i_ao].count('0')
        # print(turn_total)
        if turn_total == len(my_grid) * len(my_grid):
            update_grid(my_grid)
            break

    # delete history list for memory management
    del loop_check


def reset():
    # randomize grid
    for i_r in range(len(grid)):
        for j in range(len(grid[i_r])):
            grid[i_r][j] = randint(1, 9)

    # update visuals
    update_grid(grid)
    lb_iterations['text'] = '0'
    lb_iterations.update()
    lb_flash_count['text'] = '0'
    lb_flash_count.update()


#
#
# windows management
root = tk.Tk()
root.resizable(False, False)
fr_background = tk.Frame(root, bg="grey", relief=tk.SUNKEN, border=6)

# game board assignments
fr_board = tk.Frame(fr_background, relief=tk.RAISED, height=400, border=6)
lb_board = tk.Label(fr_board, text="{}".format(get_string(grid)))
lb_board.pack()
fr_board.grid(row=0, column=0, sticky="nsew")

# flash count assignments
fr_flash_count = tk.Frame(fr_background, height=50, bg="white")
lb_flash_title = tk.Label(fr_flash_count, text="Flash Count: ", bg="white")
lb_flash_count = tk.Label(fr_flash_count, text='0', bg="white")
lb_flash_title.pack(side="left")
lb_flash_count.pack(side="left")
fr_flash_count.grid(row=1, column=0, sticky="ew")

# controls and buttons assignments
fr_controls = tk.Frame(fr_background, relief=tk.RAISED, bg="blue", height=100, border=6)
bt_one = tk.Button(fr_controls, text="Adv\nOne", command=lambda arg1=grid: adv_one(arg1))
bt_ten = tk.Button(fr_controls, text="Adv\nTen", command=lambda arg1=grid, arg2=10: adv_one(arg1, arg2))
lb_iterations = tk.Label(fr_controls, text='0', height=3, width=7, bg="yellow", fg="black", border=6)
bt_one.grid(row=0, column=0, sticky="nsew", pady=3, padx=3)
bt_ten.grid(row=0, column=1, sticky="nsew", pady=3, padx=3)
lb_iterations.grid(row=0, column=2, sticky="nsew")
bt_hun = tk.Button(fr_controls, text="Adv 100", command=lambda arg1=grid, arg2=100: adv_one(arg1, arg2))
bt_don = tk.Button(fr_controls, text="finish", command=lambda arg1=grid, arg2=10000: adv_one(arg1, arg2))
bt_hun.grid(row=1, columnspan=2, sticky="nsew")
bt_don.grid(row=1, column=2, sticky="nsew")
bt_reset = tk.Button(fr_controls, text="Reset Board", command=reset)
bt_reset.grid(row=2, columnspan=3, sticky="nsew")
fr_controls.grid(row=2, column=0, sticky="ew")


fr_background.grid(column=1, row=1)

# using this as a global variable to control frame rate
lb_iterations_count = tk.Label(fr_background, text="1")

root.mainloop()
