#Added by Jan Odenthal, University of Heidelberg,  odenthal@stud.uni-heidelberg.de
#Commissioned by Universitätsklinikum Heidelberg, Klinik für Allgemein-, Viszeral- und Transplantationschirurgie

from HyperGuiModules.utility import *
from HyperGuiModules.constants import *
from tkinter import filedialog, simpledialog, messagebox, Scrollbar, Frame, Canvas, StringVar, OptionMenu, Text
from PIL import Image
import numpy as np
import os
import glob
import pandas as pd
from copy import deepcopy
import json


class MDA2:
    def __init__(self, mda_frame, listener):
        self.root = mda_frame
        self.live = False

        # Listener
        self.listener = listener
        self.unfocus = False
        self.sub_dirs = []

        # GUI
        self.select_data_cube_button = None
        self.select_output_dir_button = None
        self.render_data_cube_button = None
        self.selection_listbox = None
        self.data_cube_path_label = None
        self.output_dir_label = None
        self.delete_button = None
        
        self.overexposure = False
        self.underexposure = False
        self.blur = False
        self.non = False


        self.data_cube_paths = []
        self.data_cube_path_label = None
        self.path_label = None

        self.rgb_button = None
        self.sto2_button = None
        self.nir_button = None
        self.thi_button = None
        self.twi_button = None
        self.tli_button = None
        self.ohi_button = None
        self.active_image = "RGB"

        self.save_label = None
        self.automatic_names = True
        self.live_folder = None
        
        self.labels = [None]*20
        self.remove = [None]*20
        self.eudis_text = None
        self.df_dict = dict()
        self.row = 0
        self.var_overexposure = IntVar()
        self.var_non = IntVar()
        self.var_blur = IntVar()
        self.var_underxposure = IntVar()

        self.all_points_remove = None

        self.instant_save_button = None
        self.input_coords_button = None

        self.coords_window = None
        self.input_points_title = None
        self.go_button = None

        self.original_image_graph = None
        self.original_image_data = None
        self.original_image = None
        self.image_array = None

        self.current_dc_path = None
        
        if not self.__read_lists():
            self.OptionList_organs = [
                "Bladder",
                "Bone",
                "Colon",
                "Fat",
                "Gallbladder",
                "Liver",
                "Heart",
                "Jejunum",
                "Kidney",
                "Liver",
                "Lung",
                "Muscle",
                "Omentum",
                "Pancreas",
                "Peritoneum",
                "Skin",
                "Spleen",
                "Stomach",
                "Vena Cava"
                ] 
            self.OptionList_cert = [
                "yes",
                "no"
                ]
            self.OptionList_diff = [
                "yes",
                "no"
                ]
            self.OptionList_modif = [
                "None",
                "Stitches"
                ]
            self.OptionList_perf_stat = [
                "good",
                "bad"
                ]
        
        self.coords_text = []
        self.coords = []
        
        self.variable_organs = []
        self.organs = []
        
        self.variable_cert = []
        self.cert = []
        
        self.variable_diff = []
        self.diff = []
        
        self.variable_perf_stat = []
        self.perf_stat = []
        self.reset_labels = []
        
        self.variable_modif = []
        self.modif = []

        # coords in dimensions of image, i.e. xrange=[1, 640], yrange=[1, 480]
        self.coords_list = [(None, None) for _ in range(100)]
        self.mask_raw = None

        self._init_widget()

        self.rgb_button.config(foreground="red")

    # ---------------------------------------------- UPDATER AND GETTERS ----------------------------------------------
        

    def get_selected_data_cube_path(self):
        if len(self.selection_listbox.curselection())>0:
            index = self.selection_listbox.curselection()[0]
        else: 
            if self.current_dc_path is not None:
                index = self.current_dc_path
            else:
                return None
        return self.data_cube_paths[index]

    def get_selected_data_paths(self):
        selection = self.selection_listbox.curselection()
        selected_data_paths = [self.data_cube_paths[i] for i in selection]
        return selected_data_paths

    def update_original_image(self, original_image_data):
        self.original_image_data = original_image_data
        self._build_original_image(self.original_image_data)
    
    def update_saved(self, key, value):
        assert type(value) == bool
        self.saves[key] = value

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widget(self):
        self._build_rgb()
        self._build_sto2()
        self._build_nir()
        self._build_thi()
        self._build_twi()
        self._build_tli()
        self._build_ohi()
        self._build_original_image(self.original_image_data)
        self._build_select_superdir_button()
        self._build_select_all_subfolders_button()
        self._build_selection_box()
        self._build_trash_button()
        self._build_save_all_and_next()
        self._build_next_button()
        self._build_label_frame()
        self._build_comments_and_artifacts_frame()
        self._build_info_label()

    # ---------------------------------------------- BUILDERS (DISPLAY) -----------------------------------------------

    def _build_rgb(self):
        self.rgb_button = make_button(self.root, text='RGB', width=3, command=self.__update_to_rgb, row=0, column=1,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))

    def _build_sto2(self):
        self.sto2_button = make_button(self.root, text='StO2', width=4, command=self.__update_to_sto2, row=0, column=2,
                                       columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))


    def _build_nir(self):
        self.nir_button = make_button(self.root, text='NIR', width=3, command=self.__update_to_nir, row=0, column=3,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))


    def _build_thi(self):
        self.thi_button = make_button(self.root, text='THI', width=3, command=self.__update_to_thi, row=0, column=4,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))


    def _build_twi(self):
        self.twi_button = make_button(self.root, text='TWI', width=3, command=self.__update_to_twi, row=0, column=5,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))
        
    def _build_tli(self):
        self.tli_button = make_button(self.root, text='TLI', width=3, command=self.__update_to_tli, row=0, column=6,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))
        
    def _build_ohi(self):
        self.ohi_button = make_button(self.root, text='OHI', width=3, command=self.__update_to_ohi, row=0, column=7,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))


        
    # ----------------------------------------------- BUILDERS (MISC) -----------------------------------------------
        
    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Meta-data Annotation', command=self.__info, width=8)

    def _build_next_button(self):
        self.next_button = make_button(self.root, text='Next', width=12, command=self.__next,
                                               row=26, column=10, columnspan=1, inner_pady=5, outer_padx=5,
                                               outer_pady=(10, 15), height= 2)
      
    def __new_label(self, coords = None):
        self.coords_text.append(Text(self.frame_buttons))
        if coords is None:
            not_none = [i for i in self.coords_list if i != (None, None) ]
            self.coords_text[-1].delete("1.0", END)
            self.coords_text[-1].insert(END, str(not_none[-1]))
        else: 
            self.coords_text[-1].delete("1.0", END)
            self.coords_text[-1].insert(END, str(coords))
        self.coords_text[-1].config(width=6, height = 1,  font=('Helvetica', 12))
        self.coords_text[-1].grid(row=self.row, column=0, sticky='news')
        
        self.variable_organs.append(StringVar(self.root))
        self.variable_organs[-1].set(self.OptionList_organs[0])
        self.variable_organs[-1].trace("w", lambda a,b,c, d = len(self.variable_organs): self.__rearange_organs(d-1))
        self.organs.append(OptionMenu(self.frame_buttons, self.variable_organs[-1], *self.OptionList_organs))
        self.organs[-1].config(width=12, font=('Helvetica', 12))
        self.organs[-1].grid(row=self.row, column=1, sticky='news')
            
        self.variable_cert.append(StringVar(self.root))
        self.variable_cert[-1].set(self.OptionList_cert[0])
        self.cert.append(OptionMenu(self.frame_buttons, self.variable_cert[-1], *self.OptionList_cert))
        self.cert[-1].config(width=6, font=('Helvetica', 12))
        self.cert[-1].grid(row=self.row, column=2, sticky='news')
        
        self.variable_diff.append(StringVar(self.root))
        self.variable_diff[-1].set(self.OptionList_diff[0])
        self.diff.append(OptionMenu(self.frame_buttons, self.variable_diff[-1], *self.OptionList_diff))
        self.diff[-1].config(width=6, font=('Helvetica', 12))
        self.diff[-1].grid(row=self.row, column=3, sticky='news')
        
        self.variable_modif.append(StringVar(self.root))
        self.variable_modif[-1].set(self.OptionList_modif[0])
        self.modif.append(OptionMenu(self.frame_buttons, self.variable_modif[-1], *self.OptionList_modif))
        self.modif[-1].config(width=8, font=('Helvetica', 12))
        self.modif[-1].grid(row=self.row, column=5, sticky='news')
            
        self.variable_perf_stat.append(StringVar(self.root))
        self.variable_perf_stat[-1].set(self.OptionList_perf_stat[0])
        self.perf_stat.append(OptionMenu(self.frame_buttons, self.variable_perf_stat[-1], *self.OptionList_perf_stat))
        self.perf_stat[-1].config(width=8, font=('Helvetica', 12))
        self.perf_stat[-1].grid(row=self.row, column=4, sticky='news')
        
        index = deepcopy(self.row)-1
        self.reset_labels.append(make_button(self.frame_buttons, text='x', width=1, command= lambda: self._pop_row(index),
                                               row=self.row, column=6, columnspan=1, inner_pady=5, outer_padx=5,
                                               outer_pady=(5, 5), height= 1))
        
        vsb = Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        vsb.grid(row=0, column=7, rowspan=7, sticky='news')
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def _pop_row(self, row):
        table_list = self._get_table()
        table_list.pop(row)
        self.coords_list.pop(row)
        self.coords_list.append((None, None))
        self._reset_table()
        ii=0
        for table in table_list:
            self.__add_label(coords = table[2])
            self.__fill_row(ii, table)
            ii = ii+1
        self._draw_points()
        
    def _build_label_frame(self):
        self.frame_canvas = Frame(self.root)
        self.frame_canvas.grid(row=2, column=11, columnspan = 2, pady=(5, 0), sticky='news', rowspan = 10)
        self.frame_canvas.grid_propagate(False)
        
        # Add a canvas in that frame
        self.canvas = Canvas(self.frame_canvas, bg="yellow")
        self.canvas.grid(row=0, column=0, columnspan = 6, sticky="news")
        clear_button = make_button(self.root, text='Clear Table', width=5, command=self._clear_table, row=12, column=12,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))
        
        # Link a scrollbar to the canvas
        vsb = Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        vsb.grid(row=0, column=5, rowspan=7, sticky='news')
        self.canvas.configure(yscrollcommand=vsb.set)
        
        self.frame_buttons = Frame(self.canvas, bg="blue")
        self.canvas.create_window((0, 0), window=self.frame_buttons, anchor='nw')
        
        # Add 9-by-5 buttons to the frame
        
        text_coord = Text(self.frame_buttons, height = 1, width = 6)
        text_coord.insert(END, "Coord")
        text_coord.grid(row=0, column=0, columnspan = 1, sticky='news')
        
        text_label_canvas = Frame(self.frame_buttons)
        text_label_canvas.grid(row=0, column=1, columnspan = 1, sticky='news')
        text_label = Text(text_label_canvas, height = 1, width = 10)
        text_label.insert(END, "Label")
        text_label.grid(row=0, column=0, columnspan = 1, sticky='news')
        text_label_add = make_button(text_label_canvas, text='+', width=1, command=self._add_organ, row=0, column=1,
                                      columnspan=1)
        
        text_certain_canvas = Frame(self.frame_buttons)
        text_certain_canvas.grid(row=0, column=2, columnspan = 1, sticky='news')
        text_certain = Text(text_certain_canvas, height = 1, width = 8)
        text_certain.insert(END, "Certain?")
        text_certain.grid(row=0, column=0, columnspan = 1, sticky='news')
        text_certain_add = make_button(text_certain_canvas, text='+', width=1, command=self._add_certain, row=0, column=1,
                                      columnspan=1)
        
        text_diff_canvas = Frame(self.frame_buttons)
        text_diff_canvas.grid(row=0, column=3, columnspan = 1, sticky='news')
        text_diff = Text(text_diff_canvas, height = 1, width = 8)
        text_diff.insert(END, "Difficult\nto segment?")
        text_diff.grid(row=0, column=0, columnspan = 1, sticky='news')
        text_diff_add = make_button(text_diff_canvas, text='+', width=1, command=self._add_diff, row=0, column=1,
                                      columnspan=1)
        
        text_perf_canvas = Frame(self.frame_buttons)
        text_perf_canvas.grid(row=0, column=4, columnspan = 1, sticky='news')
        text_perf = Text(text_perf_canvas, height = 1, width = 15)
        text_perf.insert(END, "Perfusion\nStatus?")
        text_perf.grid(row=0, column=0, columnspan = 1, sticky='news')
        text_perf_add = make_button(text_perf_canvas, text='+', width=1, command=self._add_perf, row=0, column=1,
                                      columnspan=1)
        
        text_prop_canvas = Frame(self.frame_buttons)
        text_prop_canvas.grid(row=0, column=5, columnspan = 1, sticky='news')
        text_prop = Text(text_prop_canvas, height = 1, width = 12)
        text_prop.insert(END, "Properties")
        text_prop.grid(row=0, column=0, columnspan = 1, sticky='news')
        text_prop_add = make_button(text_prop_canvas, text='+', width=1, command=self._add_prop, row=0, column=1,
                                      columnspan=1)
        
        text_reset = Text(self.frame_buttons, height = 1, width = 10)
        text_reset.insert(END, "Reset")
        text_reset.grid(row=0, column=6, columnspan = 1, sticky='news')
        
        for c in range(5):
            self.frame_canvas.columnconfigure(c, weight=1)
        for c in range(5):
            self.frame_buttons.columnconfigure(c, weight=1)
        
        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.frame_buttons.update_idletasks()
        self.frame_canvas.config(width=800,
                            height=300)
        
        # Set the canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
        
        if len(self.selection_listbox.curselection())>0:
            sel = self.selection_listbox.curselection()[0]
        else:
            sel = None
        if sel is not None:
            if self.selection_listbox.get(sel) in self.df_dict.keys():
                table_list = self.df_dict[self.selection_listbox.get(sel)]
                ii=0
                for table in table_list:
                    self.__add_label(coords = table[2])
                    self.__fill_row(ii, table)
                    ii = ii+1
                    
    def _build_comments_and_artifacts_frame(self):
        self.frame_comments_and_artifacts = Frame(self.root)
        self.frame_comments_and_artifacts.grid(row=13, column=11, columnspan = 2, pady=(5, 0), sticky='nw', rowspan = 5)
        self.frame_comments_and_artifacts.grid_propagate(False)
        
        self.cb_overexposure = Checkbutton(self.frame_comments_and_artifacts, text='overexposure', variable=self.var_overexposure)
        self.cb_overexposure.grid(row=0, column=0, columnspan = 1, sticky='nw')
        self.cb_overexposure.bind('<Button-1>', self.__update_overexposure_checkbox)
        
        self.cb_underexposure = Checkbutton(self.frame_comments_and_artifacts, text='underexposure', variable=self.var_underxposure)
        self.cb_underexposure.grid(row=1, column=0, columnspan = 1, sticky='nw')
        self.cb_underexposure.bind('<Button-1>', self.__update_underexposure_checkbox)
        
        self.cb_blur = Checkbutton(self.frame_comments_and_artifacts, text='blur', variable=self.var_blur)
        self.cb_blur.grid(row=2, column=0, columnspan = 1, sticky='nw')
        self.cb_blur.bind('<Button-1>', self.__update_blur_checkbox)
        
        self.cb_non = Checkbutton(self.frame_comments_and_artifacts, text='none', variable=self.var_non)
        self.cb_non.grid(row=3, column=0, columnspan = 1, sticky='nw')
        self.cb_non.bind('<Button-1>', self.__update_non_checkbox)
        self.cb_non.select()
        self.non = True
        
        self.comment_insert = Text(self.frame_comments_and_artifacts, width=70, height = 4)
        self.comment_insert.grid(column = 1, row = 0, rowspan = 4)
        
        self.frame_comments_and_artifacts.config(width=650,
                            height=200)
        
    def _reset_checkboxes(self):
        self.cb_overexposure.deselect()
        self.cb_underexposure.deselect()
        self.cb_blur.deselect()
        self.cb_non.deselect()
        self.overexposure = False
        self.underexposure = False
        self.blur = False
        self.non = False
        if len(self.selection_listbox.curselection())>0:
            sel = self.selection_listbox.curselection()[0]
        else:
            sel = None
        if sel is not None:
            if self.selection_listbox.get(sel) in self.df_dict.keys():
                table_list = self.df_dict[self.selection_listbox.get(sel)]
                if len(table_list)>0:
                    table = table_list[0]
                    if table[7] == 0:
                        self.overexposure = True
                        self.cb_overexposure.select()
                    elif table[7] == 1:
                        self.underexposure = True
                        self.cb_underexposure.select()
                    elif table[7] == 2:
                        self.blur = True
                        self.cb_blur.select()
                    elif table[7] == 3:
                        self.non = True
                        self.cb_non.select()
                    else:
                        self.non = True
                        self.cb_non.select()
                else:
                    self.non = True
                    self.cb_non.select()
            else:
                self.non = True
                self.cb_non.select()
        else:
            self.non = True
            self.cb_non.select()
    
    def __update_overexposure_checkbox(self, event = None):
        self.cb_underexposure.deselect()
        self.cb_blur.deselect()
        self.cb_non.deselect()
        self.overexposure = True
        self.underexposure = False
        self.blur = False
        self.non = False
    
    def __update_underexposure_checkbox(self, event = None):
        self.cb_overexposure.deselect()
        self.cb_blur.deselect()
        self.cb_non.deselect()
        self.overexposure = False
        self.underexposure = True
        self.blur = False
        self.non = False
        
    def __update_blur_checkbox(self, event = None):
        self.cb_overexposure.deselect()
        self.cb_underexposure.deselect()
        self.cb_non.deselect()
        self.overexposure = False
        self.underexposure = False
        self.blur = True
        self.non = False
        
    def __update_non_checkbox(self, event = None):
        self.cb_overexposure.deselect()
        self.cb_underexposure.deselect()
        self.cb_blur.deselect()
        self.overexposure = False
        self.underexposure = False
        self.blur = False
        self.non = True
    
    def __fill_row(self, row, table):
        self.variable_organs[row].set(table[3])
        self.variable_cert[row].set(table[4])
        self.variable_diff[row].set(table[5])
        self.variable_modif[row].set(table[6])
        self.variable_perf_stat[row].set(table[7])
        
        
    def _build_trash_button(self):
        self.trash_button = make_button(self.root, text='Clear List', width=9, command=self.__trash_list,
                                               row=26, column=1, columnspan=3, inner_pady=5, outer_padx=0,
                                               outer_pady=(10, 15))


    def _build_select_superdir_button(self):
        self.select_data_cube_button = make_button(self.root, text="Open OP\nFolder",
                                                   command=self.__add_data_cube_dirs, inner_padx=10, inner_pady=10,
                                                   outer_padx=15, row=25, rowspan = 1, column=0, width=11, outer_pady=(5, 5))
        
    def _build_select_all_subfolders_button(self):
        self.select_data_cube_button = make_button(self.root, text="Open Project\nFolder",
                                                   command=self.__add_data_cube_subdirs, inner_padx=10, inner_pady=10,
                                                   outer_padx=15, row=26, rowspan=1, column=0, width=11, outer_pady=(5, 5))


    def _build_selection_box(self):
        self.selection_listbox = make_listbox(self.root, row=1, column=0, rowspan=24, padx=(0, 15), pady=(0, 15), height = 30, selectmode = "SINGLE", width = 18)
        self.selection_listbox.bind('<<ListboxSelect>>', self.__update_selected_data_cube)
        

    def _build_save_all_and_next(self):
        self.save_as_tif_label = make_button(self.root, "Export as CSV\nand next", row=26, column=7, outer_padx=(12, 0), height= 2,
                                     outer_pady=(10, 15), inner_padx=10, inner_pady=5, rowspan = 1, columnspan=2, width = 15, command = self.__save_single)

    


    # ---------------------------------------------- BUILDERS (IMAGE) -----------------------------------------------
        
    def _build_original_image(self, data):
        if data is None:
            # Placeholder
            self.original_image = make_label(self.root, "Navigation:\n Mouse-Left or 'q' to place point\n '+' or 'w' to zoom in\n '-' or 's' to zoom out\n arrows to change image", row=1, column=1, rowspan=25,
                                             columnspan=10, inner_pady=30, inner_padx=40, outer_padx=(5, 5),
                                             outer_pady=(5, 5))
        else:
            #data = np.asarray(rgb_image_to_hsi_array(self.original_image_data)).reshape((480, 640))
            (self.original_image_graph, self.original_image, self.image_array) = \
                make_image(self.root, data, row=1, column=1, columnspan=10, rowspan=25, lower_scale_value=None,
                           upper_scale_value=None, color_rgb=BACKGROUND, original=True, figheight=6, figwidth=8, img = self.original_image, axs = self.original_image_graph, figu = self.original_image_graph)
            self.original_image.get_tk_widget().bind('<Left>', self.__prev)
            self.original_image.get_tk_widget().bind('<Right>', self.__next)
            self.original_image.get_tk_widget().bind('<Up>', self.__first)
            self.original_image.get_tk_widget().bind('<Down>', self.__last)
            self.original_image.get_tk_widget().bind('<Button-1>', self.__add_label)
            self.original_image.get_tk_widget().focus_force()
    
    def __add_label(self, event=None, coords = None):
        self.row = self.row+1
        if event is not None:
            pos = self.original_image_graph.axes[0].get_position()
            axesX0 = pos.x0
            axesY0 = pos.y0
            axesX1 = pos.x1
            axesY1 = pos.y1
            canvas = event.widget
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            canvas.canvasx
            minX=width*axesX0
            maxX=width*axesX1
            minY=height*axesY0
            maxY=height*axesY1
            axWidth=maxX-minX
            conversionFactor = 640/axWidth
            Xc=int((event.x-minX)*conversionFactor)
            Yc=int((event.y-minY)*conversionFactor)
            if Xc>=0 and Yc>=0 and Xc<=640 and Yc<=480:
                self.__add_pt((Xc, Yc))
                coords = (Xc, Yc)
        self.__new_label(coords = coords)
        
        
            
        
    def __add_pt(self, pt):
        index = self.coords_list.index((None, None))
        if pt[0] <640 and pt[1] < 480:
            data_dict = dict()
            self.coords_list[index] = pt
            #self._build_points()
            self._draw_points()
    
    def _draw_points(self):
        if self.original_image_data is not (None, None):
            copy_data = self.original_image_data.copy()
            not_none = [i for i in self.coords_list if i != (None, None) ]
            for point in not_none:
                y = int(point[0])
                x = int(point[1])
                for xi in range(-4, 5):
                    copy_data[(x + xi) % 480, y, :3] = (100, 100, 100)
                for yi in range(-4, 5):
                    copy_data[x, (y + yi) % 640, :3] = (100, 100, 100)

            self._build_original_image(np.array(copy_data))
            self.original_image.get_tk_widget().focus_force()
        
        
    def __next(self, event = None):      
        if len(self.selection_listbox.curselection())>0:
            sel = self.selection_listbox.curselection()[0]
        else:
            sel = self.current_dc_path
        self.df_dict[self.selection_listbox.get(sel)] = self._get_table()
        if self.selection_listbox.get(sel+1) not in self.df_dict.keys():
            self.df_dict[self.selection_listbox.get(sel+1)] = self._get_table()
        self.selection_listbox.selection_clear(0, END)
        self.selection_listbox.select_set(sel+1) #This only sets focus on the first item.
        self.selection_listbox.event_generate("<<ListboxSelect>>")
        #self.__remove_pt('all')
            
    def __prev(self, event = None):
        if len(self.selection_listbox.curselection())>0:
            sel = self.selection_listbox.curselection()[0]
        else:
            sel = self.current_dc_path
        if sel is not 0:
            self.selection_listbox.selection_clear(0, END)
            self.selection_listbox.select_set(sel-1) #This only sets focus on the first item.
            self.selection_listbox.event_generate("<<ListboxSelect>>")
            #self.__remove_pt('all')
    
    def __first(self, event = None):
        self.selection_listbox.selection_clear(0, END)
        self.selection_listbox.select_set(0) #This only sets focus on the first item.
        self.selection_listbox.event_generate("<<ListboxSelect>>")
        #self.__remove_pt('all')
        
    def __last(self, event = None):
        self.selection_listbox.selection_clear(0, END)
        self.selection_listbox.select_set("end") #This only sets focus on the first item.
        self.selection_listbox.event_generate("<<ListboxSelect>>")
        #self.__remove_pt('all')
    
    def _clear_table(self, event = None):
        if len(self.selection_listbox.curselection())>0:
            sel = self.selection_listbox.curselection()[0]
        else:
            sel = None
        if sel is not None:
            if self.selection_listbox.get(sel) in self.df_dict.keys():
                del self.df_dict[self.selection_listbox.get(sel)]
        self._reset_table()
        
    def _reset_table(self):
        self.coords_text = []
        self.variable_organs = []
        self.organs = []
        self.variable_cert = []
        self.cert = []
        self.variable_diff = []
        self.diff = []
        self.variable_perf_stat = []
        self.perf_stat = []
        self.variable_modif = []
        self.modif = []
        self._build_label_frame()
        self.row = 0

    # ----------------------------------------------- UPDATERS (IMAGE) ------------------------------------------------
    def _get_table(self):
            df = []
            if self.get_selected_data_cube_path() is not None:
                path = os.path.abspath(self.get_selected_data_cube_path())
            else:
                path = ""
            patient_id = os.path.basename(os.path.dirname(os.path.dirname(path)))
            timestamp = os.path.basename(os.path.dirname(path))
            if self.overexposure:
                artifact = 0
            elif self.underexposure:
                artifact = 1
            elif self.blur:
                artifact = 2
            elif self.non:
                artifact = 3
            comment = self.comment_insert.get("1.0",END)
            self.coords_list = [(None, None) for _ in range(100)]
            for idx in range(len(self.organs)):
                coord = self.coords_text[idx].get("1.0",END)
                coord = coord.replace(")", "")
                coord = coord.replace("(", "")
                coord = tuple([int(x) for x in coord.split(", ")])
                self.coords_list[idx] = coord
                organ = self.variable_organs[idx].get()
                cert = self.variable_cert[idx].get()
                diff = self.variable_diff[idx].get()
                modif = self.variable_modif[idx].get()
                perf_stat = self.variable_perf_stat[idx].get()
                df.append([patient_id,timestamp,coord, organ, cert, diff, modif, perf_stat, artifact, comment])
            return df

    def __update_to_rgb(self):
        self.active_image = "RGB"
        self.rgb_button.config(foreground="red")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.RGB)

    def __update_to_sto2(self):
        self.active_image = "STO2"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="red")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.STO2)

    def __update_to_nir(self):
        self.active_image = "NIR"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="red")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.NIR)

    def __update_to_thi(self):
        self.active_image = "THI"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="red")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.THI)

    def __update_to_twi(self):
        self.active_image = "TWI"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="red")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.TWI)
        
    def __update_to_tli(self):
        self.active_image = "TLI"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="red")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.TLI)
        
    def __update_to_ohi(self):
        self.active_image = "OHI"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="red")
        self.update_original_image(self.OHI)



    # ------------------------------------------------- INPUT POP-UP --------------------------------------------------

    def _insert_comment(self):
        self.comment_insert.delete("1.0", 'end')
        if len(self.selection_listbox.curselection())>0:
            sel = self.selection_listbox.curselection()[0]
        else:
            sel = None
        if sel is not None:
            if self.selection_listbox.get(sel) in self.df_dict.keys():
                table_list = self.df_dict[self.selection_listbox.get(sel)]
                if len(table_list)>0:
                    table = table_list[0]
                    self.comment_insert.insert("1.0", table[9])

    def __update_selected_data_cube(self, event):
        self._reset_checkboxes()
        self._reset_table()
        self._insert_comment()
        dc_path = self.get_selected_data_cube_path()[0:-12]
        if self.current_dc_path is not self.selection_listbox.curselection()[0]:
            if len(self.selection_listbox.curselection())>0:
                self.current_dc_path = self.selection_listbox.curselection()[0]
        
        a = Image.open(dc_path +"RGB-Image.png")
        a = np.asarray(a)
        if a.shape[0] == 550:
            a = a[50:530, 20:660, :3]
        else:
            a = a[30:510, 3:643, :3]
        self.RGB = a
        
        if os.path.exists(dc_path +"NIR-Perfusion.png"):
            b = Image.open(dc_path +"NIR-Perfusion.png")
            b = np.asarray(b)
            if b.shape[0] == 550:
                b = b[50:530, 50:690, :3]
            else:
                b = b[26:506, 4:644, :3]
            self.NIR = b
        else:
            self.NIR = np.zeros((480, 680,3)).astype("uint8")
        
        if os.path.exists(dc_path +"TWI.png"):
            c = Image.open(dc_path +"TWI.png")
            c = np.asarray(c)
            if c.shape[0] == 550:
                c = c[50:530, 50:690, :3]
            else:
                c = c[26:506, 4:644, :3]
            self.TWI = c
        else:
            self.TWI = np.zeros((480, 680,3)).astype("uint8")
        
        if os.path.exists(dc_path +"THI.png"):
            d = Image.open(dc_path +"THI.png")
            d = np.asarray(d)
            if d.shape[0] == 550:
                d = d[50:530, 50:690, :3]
            else:
                d = d[26:506, 4:644, :3]
            self.THI = d
        else:
            self.THI  = np.zeros((480, 680,3)).astype("uint8")
        
        if os.path.exists(dc_path +"Oxygenation.png"):
            e = Image.open(dc_path +"Oxygenation.png")
            e = np.asarray(e)
            if e.shape[0] == 550:
                e = e[50:530, 50:690, :3]
            else:
                e = e[26:506, 4:644, :3]
            self.STO2 = e
        else:
            self.STO2 = np.zeros((480, 680,3)).astype("uint8")
        
        if os.path.exists(dc_path +"TLI.png"):
            f = Image.open(dc_path +"TLI.png")
            f = np.asarray(f)
            if f.shape[0] == 550:
                f = f[50:530, 50:690, :3]
            else:
                f = f[26:506, 4:644, :3]
            self.TLI = f
        else:
            self.TLI = np.zeros((480, 680, 3)).astype("uint8")
        
        if os.path.exists(dc_path +"OHI.png"):
            g = Image.open(dc_path +"OHI.png")
            g = np.asarray(g)
            if g.shape[0] == 550:
                g = g[50:530, 50:690, :3]
            else:
                g = g[26:506, 4:644, :3]
            self.OHI = g
        else:
            self.OHI = np.zeros((480, 680,3)).astype("uint8")
        
        if self.active_image is "RGB":
            self.__update_to_rgb()
        elif self.active_image is "STO2":
            self.__update_to_sto2()
        elif self.active_image is "NIR":
            self.__update_to_nir()
        elif self.active_image is "TWI":
            self.__update_to_twi()
        elif self.active_image is "THI":
            self.__update_to_thi()
        elif self.active_image is "OHI":
            self.__update_to_ohi()
        elif self.active_image is "TLI":
            self.__update_to_tli()
        
        

    def __add_data_cube_dirs(self):
        super_dir = self.__get_path_to_dir("Please select folder containing all the data folders.")
        sub_dirs = self.__get_sub_folder_paths(super_dir)
        for sub_dir in sub_dirs:
            if len(glob.glob(sub_dir + "/*RGB-Image.png"))>=1:
                self.__add_data_cube(sub_dir)
    
    def __add_data_cube_subdirs(self):
        super_dir = self.__get_path_to_dir("Please select folder containing all the OP folders.")
        sub_dirs = self.__get_sub_folder_paths(super_dir, True)
        for sub_dir in sub_dirs:
            if len(glob.glob(sub_dir + "/*RGB-Image.png"))>=1:
                self.__add_data_cube(sub_dir)              

    def __add_data_cube(self, sub_dir):
        contents = os.listdir(sub_dir)
        dc_path = [sub_dir + "/" + i for i in contents if "SpecCube.dat" in i]  # takes first data cube it finds
        if len(dc_path) > 0:
            dc_path = dc_path[0]
            if dc_path in self.data_cube_paths:
                messagebox.showerror("Error", "That data has already been added.")
            else:
                self.data_cube_paths.append(dc_path)
                concat_path = os.path.basename(os.path.normpath(dc_path))
                self.selection_listbox.insert(END, concat_path)
                self.selection_listbox.config(width=18)

    def __get_path_to_dir(self, title):
        if self.listener.dc_path is not None:
            p = os.path.dirname(os.path.dirname(self.listener.dc_path))
            path = filedialog.askdirectory(parent=self.root, title=title, initialdir=p)
        else:
            path = filedialog.askdirectory(parent=self.root, title=title)
        return path


    @staticmethod
    def __get_sub_folder_paths(path_to_main_folder, recursive = False): 
        sub_folders = sorted(glob.glob(path_to_main_folder+"/**/", recursive = recursive))
        return sub_folders
        
    def __trash_list(self):
        self.df_dict = dict()
        self.data_cube_paths = []
        self.selection_listbox.delete(0,'end')
        self._reset_table()
  
    def __switch_autoname(self):
        self.automatic_names=True
        self._update_tif_save_path()
        
    def __save_single(self):
        csv_dict = {"patient_id": [], "timestamp": [], "coord" : [], "label": [], "presence_certain": [], "segmentation_difficult": [], "perfusion_status": [], "modifications": [], "image_artifacts": [], "comments": []}
        lis = self._get_table()
        for organ in lis:
                    print(organ)
                    if organ[8] == 0:
                        artifact = "overexposure"
                    elif organ[8] == 1:
                        artifact = "underexposure"
                    elif organ[8] == 2:
                        artifact = "blur"
                    elif organ[8] == 3:
                        artifact = "None"
                    csv_dict["patient_id"].append(organ[0])
                    csv_dict["timestamp"].append(organ[1])
                    csv_dict["coord"].append(organ[2])
                    csv_dict["label"].append(organ[3])
                    csv_dict["presence_certain"].append(organ[4])
                    csv_dict["segmentation_difficult"].append(organ[5])
                    csv_dict["perfusion_status"].append(organ[6])
                    csv_dict["modifications"].append(organ[7])
                    csv_dict["image_artifacts"].append(artifact)
                    csv_dict["comments"].append(organ[9])
        print(csv_dict)
        df = pd.DataFrame(csv_dict) 
        folder = os.path.dirname(os.path.abspath(self.get_selected_data_cube_path())) + "/_weak_label"
        if not os.path.exists(folder):
            os.mkdir(folder)
        SAVING_PATH = folder + "/_weak_label_1.csv"
        df.to_csv(SAVING_PATH, index = False)
        self.__next()
        
    def __save_all(self): 
        csv_dict = {"patient_id": [], "timestamp": [], "coord": [], "label": [], "presence_certain": [], "segmentation_difficult": [], "perfusion_status": [], "modifications": [], "image_artifacts": [], "comments": []}
        keys = list(self.df_dict.keys())
        keys.sort()
        for key in keys:
            print(key)
            lis = self.df_dict[key]
            for organ in lis:
                if "Choose label" != organ[2]:
                    if organ[8] == 0:
                        artifact = "overexposure"
                    elif organ[8] == 1:
                        artifact = "underexposure"
                    elif organ[8] == 2:
                        artifact = "blur"
                    elif organ[8] == 3:
                        artifact = "None"
                    csv_dict["patient_id"].append(organ[0])
                    csv_dict["timestamp"].append(organ[1])
                    csv_dict["coord"].append(organ[2])
                    csv_dict["label"].append(organ[3])
                    csv_dict["presence_certain"].append(organ[4])
                    csv_dict["segmentation_difficult"].append(organ[5])
                    csv_dict["perfusion_status"].append(organ[6])
                    csv_dict["modifications"].append(organ[7])
                    csv_dict["image_artifacts"].append(artifact)
                    csv_dict["comments"].append(organ[9])
        df = pd.DataFrame(csv_dict) 
        SAVING_PATH = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
        df.to_csv(SAVING_PATH, index = False)
        
    # ------------------------------------------------------- MISC -----------------------------------------
        
    def __info(self): 
        info = self.listener.modules[INFO].mda_info
        title = "Meta-data Annotation"
        make_info(title=title, info=info)
        
    def __read_lists(self):
        if os.path.exists("./options.json"):
            with open("./options.json") as jsonFile:
                dictus = json.load(jsonFile)
                jsonFile.close()
            self.OptionList_organs = dictus["organ"]
            self.OptionList_cert = dictus["certain"]
            self.OptionList_diff = dictus["diff"]
            self.OptionList_modif = dictus["modif"]
            self.OptionList_perf_stat = dictus["perf"]
            return True
        else:
            return False
            
        
    def __save_lists(self):
        dictus = {"organ": self.OptionList_organs,
                  "certain": self.OptionList_cert,
                  "diff": self.OptionList_diff,
                  "modif": self.OptionList_modif,
                  "perf": self.OptionList_perf_stat}
        if os.path.exists("./options.json"):
            os.remove("./options.json")
        with open("./options.json", "w") as f:
            json.dump(dictus, f)
            f.close()
        
    def _add_organ(self, event = None):
        answer = simpledialog.askstring("Input", "Type '-LABEL' to delete LABEL.",
                                parent=self.root)
        if answer == "":
            pass
        elif answer[0] == "-":
            a = self.OptionList_organs.index(answer[1::])
            self.OptionList_organs.pop(a)
            for ii, organ in enumerate(self.organs):
                menu = organ["menu"]
                menu.delete(a) 
        else:
            self.OptionList_organs.append(answer)
            for ii, organ in enumerate(self.organs):
                menu = organ["menu"]
                menu.add_command(label=answer, 
                                    command=lambda value=answer: self.variable_organs[ii].set(value))
        self.__save_lists()

    
    def _add_certain(self, event = None):
        answer = simpledialog.askstring("Input", "Type '-LABEL' to delete LABEL.",
                                parent=self.root)
        if answer == "":
            pass
        elif answer[0] == "-":
            a = self.OptionList_cert.index(answer[1::])
            self.OptionList_cert.pop(a)
            for ii, organ in enumerate(self.cert):
                menu = organ["menu"]
                menu.delete(a) 
        else:
            self.OptionList_cert.append(answer)
            for ii, organ in enumerate(self.cert):
                menu = organ["menu"]
                menu.add_command(label=answer, 
                                    command=lambda value=answer: self.variable_cert[ii].set(value))
        self.__save_lists()
    
    def _add_diff(self, event = None):
        answer = simpledialog.askstring("Input", "Type '-LABEL' to delete LABEL.",
                                parent=self.root)
        if answer == "":
            pass
        elif answer[0] == "-":
            a = self.OptionList_diff.index(answer[1::])
            self.OptionList_diff.pop(a)
            for ii, organ in enumerate(self.diff):
                menu = organ["menu"]
                menu.delete(a) 
        else:
            self.OptionList_diff.append(answer)
            for ii, organ in enumerate(self.diff):
                menu = organ["menu"]
                menu.add_command(label=answer, 
                                    command=lambda value=answer: self.variable_diff[ii].set(value))
        self.__save_lists()
    
    def _add_perf(self, event = None):
        answer = simpledialog.askstring("Input", "Type '-LABEL' to delete LABEL.",
                                parent=self.root)
        if answer == "":
            pass
        elif answer[0] == "-":
            a = self.OptionList_perf_stat.index(answer[1::])
            self.OptionList_perf_stat.pop(a)
            for ii, organ in enumerate(self.perf_stat):
                menu = organ["menu"]
                menu.delete(a) 
        else:
            self.OptionList_perf_stat.append(answer)
            for ii, organ in enumerate(self.perf_stat):
                menu = organ["menu"]
                menu.add_command(label=answer, 
                                    command=lambda value=answer: self.variable_perf_stat[ii].set(value))
        self.__save_lists()
    
    def _add_prop(self, event = None):
        answer = simpledialog.askstring("Input", "Type '-LABEL' to delete LABEL.",
                                parent=self.root)
        if answer == "":
            pass
        elif answer[0] == "-":
            a = self.OptionList_modif.index(answer[1::])
            self.OptionList_modif.pop(a)
            for ii, organ in enumerate(self.modif):
                menu = organ["menu"]
                menu.delete(a) 
        else:
            self.OptionList_modif.append(answer)
            for ii, organ in enumerate(self.modif):
                menu = organ["menu"]
                menu.add_command(label=answer, 
                                    command=lambda value=answer: self.variable_modif[ii].set(value))
        self.__save_lists()
        
    def __rearange_organs(self, index):
        s = self.variable_organs[index].get()
        a = self.OptionList_organs.index(s)
        order_list = list(range(len(self.OptionList_organs)))
        order_list.pop(a)
        order_list = [a] + order_list
        self.OptionList_organs = [self.OptionList_organs[i] for i in order_list]
        #for ii, organ in enumerate(self.organs):
        #    menu = organ["menu"]
        #    menu.delete(0, "end") 
        #    for opt in self.OptionList_organs:
        #        menu.add_command(label=opt, command=lambda value=opt: self.variable_organs[ii].set(value))
                
        
        
        
        