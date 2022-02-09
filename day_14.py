import logging
import textwrap
import tkinter as tk
import time
from operator import itemgetter
import math


def get_data(file_name='day_14.dat'):
    logging.info(f'Opening {file_name}, reading...')
    with open(file_name, 'r') as inf:
        raw_data = [line for line in inf.read().split('\n')]
    logging.debug('Read file to raw data')
    logging.debug('Formatting rules data...')
    my_rules = dict(item.split(' -> ') for item in raw_data[2:])
    for keys in my_rules:
        my_rules[keys] = [f'{keys[0]}{my_rules[keys]}', f'{my_rules[keys]}{keys[1]}']
    print(my_rules)
    logging.debug('Formatting chain data...')
    my_chain = raw_data[0]
    return my_chain, my_rules


class PolymereChain:

    def __init__(self, string=None, rules=None):
        logging.debug('Creating new Poly Chain instance')
        self.base_chain = string
        self.rules = rules
        self.chain = {}.fromkeys(rules, 0)
        for i in range(len(self.base_chain) - 1):
            self.chain[f'{self.base_chain[i]}{self.base_chain[i + 1]}'] += 1
        self.count = None
        if string and rules:
            logging.debug('Creating self.count')
            self.build_count()

    def build_count(self):
        logging.debug('Internal build_count')
        temp_string = ''
        for letters in self.rules.keys():
            temp_string += letters
        self.count = {}.fromkeys(temp_string, 0)
        for letters in self.count.keys():
            self.count[letters] += self.base_chain.count(letters)

    def show_count(self):
        logging.debug('show count called')
        for items in self.count.keys():
            logging.info(f'{items}:{self.count[items]}')
        largest = max(self.count.values())
        smallest = min(self.count.values())
        logging.info(f'{largest}-{smallest}={largest - smallest}')

    def polymorph(self):
        logging.debug('polymorph called')
        new_dict = {}.fromkeys(self.chain, 0)
        for pairs in self.chain:
            if self.chain[pairs]:
                first_new_pair = self.rules[pairs][0]
                second_new_pair = self.rules[pairs][1]
                new_char = first_new_pair[1]
                increase = self.chain[pairs]
                new_dict[first_new_pair] += increase
                new_dict[second_new_pair] += increase
                self.count[new_char] += increase
        self.chain = new_dict


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry('1600x1200')
        self.resizable(False, False)
        logging.info('Getting data...')
        temp_chain, temp_rules = get_data()
        logging.debug(f'Returned from get_data with {temp_chain}---{temp_rules}')
        self.poly_data = PolymereChain(temp_chain, temp_rules)
        self.chain_window()
        self.graph_window()
        self.pie_window()
        self.progress_window()
        self.start_visuals()

    def start_visuals(self):
        logging.info('Entering polymerization loop...')
        self.lb_poly_data.config(text=textwrap.fill(str(self.poly_data.chain), 10, break_long_words=True))
        self.lb_poly_data.update()
        generation_count = 40
        for iteration in range(1, generation_count + 1):
            time.sleep(.5)
            logging.debug(f'poly step {iteration}:{self.poly_data.count}->')
            self.cv_progrss_bar.delete('all')
            self.cv_progrss_bar.create_rectangle(0, 0, (970 / generation_count) * iteration, 60, fill='yellow')
            self.cv_progrss_bar.create_text(485, 30, text=f'Generation {iteration}', justify='center')
            self.poly_data.polymorph()
            self.lb_poly_data.config(text=self.build_text_data())
            self.lb_poly_data.update()
            self.draw_bar_graphs()
            self.draw_pie()
            logging.debug(self.poly_data.count)
            # self.poly_data.show_count()

    def draw_bar_graphs(self):

        self.cv_graph_bars.delete('all')

        max_bar = max(self.poly_data.count.values())
        bar_step = 790 / max_bar

        for i in range(len(self.poly_data.count.keys())):
            start_y = self.graph_member_coords[i][0]
            end_y = self.graph_member_coords[i][1]
            mid_y = (start_y + end_y) / 2
            my_value = list(self.poly_data.count.values())[i]
            end_x = bar_step * my_value
            self.cv_graph_bars.create_rectangle(0, start_y, end_x, end_y, fill='black')
            self.cv_graph_bars.create_text(60, mid_y, text=f'{my_value:.2e}', fill='white')

    def build_text_data(self):
        my_wrapped = textwrap.TextWrapper()
        my_wrapped.width = 40
        my_wrapped.max_lines = 22
        my_wrapped.break_long_words = True
        max_value = max(self.poly_data.count.values())
        min_value = min(self.poly_data.count.values())
        diff = max_value - min_value
        my_string = str(f'{max_value} - {min_value} = {diff}\n')
        my_string += str(self.poly_data.count).replace(' ', '')
        my_string += str(self.poly_data.chain).replace(' ', '')
        my_string = my_wrapped.fill(my_string)
        return my_string

    def graph_window(self):
        self.fr_graph_frame = tk.Frame(self,
                                       width=1000,
                                       height=1180,
                                       relief='sunken',
                                       border=10,
                                       )
        self.fr_graph_frame.grid_propagate(False)
        self.fr_graph_frame.grid(row=0, column=0, rowspan=3, padx=10, pady=10)
        self.cv_graph_title = tk.Canvas(self.fr_graph_frame,
                                        width=400,
                                        height=50,
                                        )
        self.cv_graph_title.create_text(200, 25, text='Polymer Content by Element', justify='center')
        self.cv_graph_title.place(x=300, y=5)
        self.cv_graph_labels = tk.Canvas(self.fr_graph_frame,
                                         width=100,
                                         height=1000,
                                         )
        members = self.poly_data.count.keys()
        spacing = int(1000 / len(members))
        padding = int(spacing * .4)
        self.graph_member_coords = []
        i = 0
        for item in members:
            self.graph_member_coords.append(
                [(spacing / 2) + (i * spacing) - padding, (spacing / 2) + (i * spacing) + padding])
            self.cv_graph_labels.create_text(30, (spacing / 2) + (i * spacing), text=f'{item}:')
            self.cv_graph_labels.create_line(45, (spacing / 2) + (i * spacing), 60, (spacing / 2) + (i * spacing),
                                             width=3)
            self.cv_graph_labels.create_line(63, (spacing / 2) + (i * spacing) - padding, 63,
                                             (spacing / 2) + (i * spacing) + padding, width=3)
            i += 1

        self.cv_graph_labels.place(x=30, y=60)

        self.cv_graph_bars = tk.Canvas(self.fr_graph_frame,
                                       width=800,
                                       height=1000)

        self.cv_graph_bars.place(x=140, y=60)

        self.draw_bar_graphs()

    def progress_window(self):
        self.fr_progress = tk.Frame(self,
                                    width=980,
                                    height=80,
                                    relief='raised',
                                    border=10
                                    )
        self.cv_progrss_bar = tk.Canvas(self.fr_progress, height=60, width=960)
        self.fr_progress.place(x=20, y=1100)
        self.cv_progrss_bar.place(x=0, y=0)

    def chain_window(self):
        self.fr_chain_frame = tk.Frame(self,
                                       width=570,
                                       height=610,
                                       relief='sunken',
                                       border=10
                                       )
        self.fr_chain_frame.grid_propagate(False)
        self.lb_poly_data = tk.Label(self.fr_chain_frame)
        self.lb_poly_data.grid(rowspan=1, columnspan=1, sticky='nsew')
        self.fr_chain_frame.grid(row=0, column=1, rowspan=2, padx=(0, 10), pady=10)

    def pie_window(self):
        self.fr_pie_frame = tk.Frame(self,
                                     width=570,
                                     height=560,
                                     relief='sunken',
                                     border=10
                                     )
        self.fr_pie_frame.grid_propagate(False)
        self.fr_pie_frame.grid(row=2, column=1, padx=(0, 10), pady=(0, 10))
        self.cv_pie_canvas = tk.Canvas(self.fr_pie_frame,
                                       height=540,
                                       width=550,
                                       )
        self.cv_pie_canvas.create_oval(20, 20, 520, 520, width=1)
        self.cv_pie_canvas.grid()

        self.draw_pie()

    def draw_pie(self):

        self.cv_pie_canvas.delete('all')
        my_slices = list(zip(self.poly_data.count.keys(), self.poly_data.count.values()))

        total_slices = 0
        for slices in my_slices:
            total_slices += slices[1]

        my_slices = sorted(my_slices, key=itemgetter(1), reverse=True)

        smallest_slice = 360 / total_slices
        sum_of_arc = 0
        label_len = 230
        center_point=270

        for slices in my_slices:
            current_size = smallest_slice * slices[1]
            label_angle = sum_of_arc + (current_size / 2)
            if label_angle > 270:
                label_angle = 360 - label_angle
                my_rad_y = (label_angle * math.pi) / 180
                my_rad_x = ((90 - label_angle) * math.pi) / 180
                my_x = label_len * math.sin(my_rad_x)
                my_y = label_len * math.sin(my_rad_y)
                my_x = center_point + my_x
                my_y = center_point + my_y
            elif label_angle > 180:
                label_angle = label_angle - 180
                my_rad_y = (label_angle * math.pi) / 180
                my_rad_x = ((90 - label_angle) * math.pi) / 180
                my_x = label_len * math.sin(my_rad_x)
                my_y = label_len * math.sin(my_rad_y)
                my_x = center_point - my_x
                my_y = center_point + my_y
            elif label_angle > 90:
                label_angle = 180 - label_angle
                my_rad_y = (label_angle * math.pi) / 180
                my_rad_x = ((90 - label_angle) * math.pi) / 180
                my_x = label_len * math.sin(my_rad_x)
                my_y = label_len * math.sin(my_rad_y)
                my_x = center_point - my_x
                my_y = center_point - my_y
            else:
                my_rad_y = (label_angle * math.pi) / 180
                my_rad_x = ((90 - label_angle) * math.pi) / 180
                my_x = label_len * math.sin(my_rad_x)
                my_y = label_len * math.sin(my_rad_y)
                my_x = center_point + my_x
                my_y = center_point - my_y
            my_x = abs(my_x)
            my_y = abs(my_y)
            # self.cv_pie_canvas.create_line(center_point, center_point, my_x, my_y, width=3)
            self.cv_pie_canvas.create_text(my_x, my_y, text=slices[0], fill='black')
            self.cv_pie_canvas.create_arc(20, 20, 520, 520, start=sum_of_arc, extent=current_size)
            sum_of_arc += current_size


if __name__ == "__main__":
    my_format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=my_format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    # logging.getLogger().setLevel(logging.DEBUG)

    logging.info('Starting...')

    app = App()
    app.mainloop()

    logging.info('Exiting')
