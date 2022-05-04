#Added by Jan Odenthal, University of Heidelberg,  odenthal@stud.uni-heidelberg.de
#Commissioned by Universitätsklinikum Heidelberg, Klinik für Allgemein-, Viszeral- und Transplantationschirurgie

from HyperGuiModules.utility import *
from HyperGuiModules.constants import *
from skimage.draw import line_aa
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import os
import glob
import xlsxwriter
import pandas as pd
import shutil

class Measure:
    def __init__(self, measure_frame, listener):
        self.root = measure_frame

        # Listener
        self.listener = listener
        
        # BOOLS & CHECKBOXES
        self.save_tif_bool = False
        self.first = True
        self.delete_content = True
        self.save_as_tif_checkbox_value = IntVar()
        self.var_keep = IntVar()
        self.var_load_recent = IntVar()
        self.keep = False
        self.load_recent = False
        
        # COORDS & MOUSE POSITION
        self.mouse_x = 320
        self.mouse_y = 240
        self.view_mid = [240, 320]
        self.measure_point = (None, None)
        self.coords_list = [(None, None) for _ in range(2)]
        
        # NUMERICAL
        self.counter = 0
        self.conversion_factor = 0.448801743
        self.line_index = 0
        self.zoom_factor = 1
        self.name_unique = False
        
        # LISTS  
        self.lines = [[(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)]
                      ]
        self.centers = [(None, None)]*100           
        self.dists = [None]*100
        self.lengths = [None]*100
        self.cum_dists = [None]*100
        self.data_cube_paths = []
        
        # GUI
        self.select_data_cube_button = None
        self.select_output_dir_button = None
        self.render_data_cube_button = None
        self.selection_listbox = None
        self.data_cube_path_label = None
        self.output_dir_label = None
        self.delete_button = None
        self.measure_mode = "simple"
        self.eudis_text = None
        self.title1 = None
        self.title2 = None
        self.title3 = None
        self.title4 = None
        self.title5 = None
        self.data_cube_path_label = None
        self.path_label = None
        self.rgb_button = None
        self.sto2_button = None
        self.nir_button = None
        self.thi_button = None
        self.twi_button = None
        self.tli_button = None
        self.ohi_button = None
        self.all_points_remove = None
        self.instant_save_button = None
        self.input_coords_button = None
        self.coords_window = None
        self.input_points_title = None
        self.go_button = None
        self.original_image_graph = None

        # SAVING & LOADING
        self.filename = "_measuring_results_SIMPLE_1"
        self.image_to_save = None
        self.current_dc_path = None
        
        # IMAGE
        self.image_array = None
        self.active_image = "RGB"
        self.original_image_data = None
        self.original_image = None

        self._init_widget()

    # ---------------------------------------------- UPDATER AND GETTERS ----------------------------------------------
        

    def get_selected_data_cube_path(self):
        if len(self.selection_listbox.curselection())>0:
            index = self.selection_listbox.curselection()[0]
        else: 
            index = self.current_dc_path
        return self.data_cube_paths[index]

    def get_selected_data_paths(self):
        selection = self.selection_listbox.curselection()
        selected_data_paths = [self.data_cube_paths[i] for i in selection]
        return selected_data_paths
    
    def update_filename(self, event = None):
        self.counter = 0
        self.filename_unique = self.filename_entry.get()
        self.name_unique = True
        self._new_filename()
    
    def _insert_filename(self):
        self.filename_entry.delete(0,"end")
        self.filename_entry.insert(0, self.filename)

    def update_original_image(self, original_image_data):
        self.original_image_data = original_image_data
        self._build_original_image(self.original_image_data)
        self._draw_points()
    
    def update_saved(self, key, value):
        assert type(value) == bool
        self.saves[key] = value
        
    def update_conversion_factor(self, event = None):
        self.conversion_factor = float(self.input_conversion_factor.get())
        self.input_conversion_factor.delete(0,"end")
        self.input_conversion_factor.insert(0, str(self.conversion_factor))
        self.__update_all_listboxes()

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widget(self):
        self._build_info_label()
        self._build_rgb()
        self._build_sto2()
        self._build_nir()
        self._build_thi()
        self._build_twi()
        self._build_tli()
        self._build_ohi()
        self._build_instant_save_button()
        self._build_original_image(self.original_image_data)
        self._build_select_superdir_button()
        self._build_select_all_subfolders_button()
        self._build_selection_box()
        self._build_line_box()
        self._build_centers_box()
        self._build_dists_box()
        self._build_dists_converted_box()
        self._build_lengths_box()
        self._build_lengths_converted_box()
        self._build_save_tif()
        self._build_next_button()
        self._build_eudis_text()
        self._build_trash_button()
        self._build_reset_lines_button()
        self._build_save_xlsx_button()
        self._build_conversion_factor_input()
        self._build_filename_entry()
        self._build_keep_Checkbox()
        self._build_load_recent_Checkbox()
        self._build_delete_folder_button()
        self.__update_all_listboxes()
        self._build_titles()
        self.rgb_button.config(foreground="red")

    # ---------------------------------------------- BUILDERS (DISPLAY) -----------------------------------------------

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Measure Tool', command=self.__info, width=8)

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

    def _build_next_button(self):
        self.next_button = make_button(self.root, text='Next (wo. saving)', width=12, command=self.__next,
                                               row=28, column=10, columnspan=1, inner_pady=5, outer_padx=5,
                                               outer_pady=(10, 15), height= 2)

    def _build_instant_save_button(self):
        self.instant_save_button = make_button(self.root, text='Save measurements\nand Next', width=12, command=self.__save_measure_and_next,
                                               row=28, column=4, columnspan=3, inner_pady=5, outer_padx=5,
                                               outer_pady=(10, 15), height= 2)
        
    def _build_delete_folder_button(self):
        self.delete_folder_button = make_button(self.root, text='Delete folder', width=12, command=self.__delete_folder,
                                               row=28, column=3, columnspan=1, inner_pady=5, outer_padx=5,
                                               outer_pady=(10, 15), height= 2)
        
    def __delete_folder(self):
        path = os.path.dirname(self.get_selected_data_cube_path())
        if not os.path.exists(path + "/_measuring"):
            os.mkdir(path + "/_measuring")
        path = path + "/_measuring"
        if os.path.exists(path):
            shutil.rmtree(path)
        self.__reset_lines()
        
    def _build_trash_button(self):
        self.trash_button = make_button(self.root, text='Clean List', width=9, command=self.__trash_list,
                                               row=28, column=1, columnspan=2, inner_pady=5, outer_padx=0,
                                               outer_pady=(10, 15))
        
    def _build_reset_lines_button(self):
        self.trash_button = make_button(self.root, text='Reset (r)', width=9, command=self.__reset_lines,
                                               row=28, column=11, columnspan=2, inner_pady=5, outer_padx=0,
                                               outer_pady=(10, 15))
    
    def _build_save_xlsx_button(self):
        self.trash_button = make_button(self.root, text='Save xlsx (x)', width=9, command=self.__save_xlsx,
                                               row=28, column=13, columnspan=2, inner_pady=5, outer_padx=0,
                                               outer_pady=(10, 15))


    def _build_select_superdir_button(self):
        self.select_data_cube_button = make_button(self.root, text="Open OP\nFolder",
                                                   command=self.__add_data_cube_dirs, inner_padx=10, inner_pady=10,
                                                   outer_padx=15, row=25, rowspan = 2, column=0, width=11, outer_pady=(5, 5))
        
    def _build_select_all_subfolders_button(self):
        self.select_data_cube_button = make_button(self.root, text="Open Project\nFolder",
                                                   command=self.__add_data_cube_subdirs, inner_padx=10, inner_pady=10,
                                                   outer_padx=15, row=28, rowspan=1, column=0, width=11, outer_pady=(5, 5))

    def _build_selection_box(self):
        self.selection_listbox = make_listbox(self.root, row=1, column=0, rowspan=24, padx=(0, 15), pady=(0, 15), height = 35, width = 18)
        self.selection_listbox.bind('<<ListboxSelect>>', self.__update_selected_data_cube)
        
    def _build_line_box(self):
        self.line_listbox = make_listbox(self.root, row=1, column=11, rowspan=21, padx=(0, 15), pady=(0, 15), height = 35, width = 8)
        self.line_listbox.bind('<<ListboxSelect>>', self.__update_selected_line)
        
    def _build_keep_Checkbox(self):
        self.cb_keep = Checkbutton(self.root, text='Keep', variable=self.var_keep)
        self.cb_keep.grid(row=28, column=15, columnspan = 1, sticky='nw')
        self.cb_keep.bind('<Button-1>', self.__update_keep_checkbox)
        
    def _build_load_recent_Checkbox(self):
        self.cb_load_recent = Checkbutton(self.root, text='Most recent', variable=self.var_load_recent)
        self.cb_load_recent.grid(row=25, column=16, columnspan = 2, sticky='nw')
        self.cb_load_recent.bind('<Button-1>', self.__update_load_recent_checkbox)
        
        
    def __update_load_recent_checkbox(self, event = None):
        self.load_recent = not self.load_recent
        print(self.load_recent)
        self.__read_file()
        
    def __update_keep_checkbox(self, event = None):
        self.keep = not self.keep
        
    def _build_titles(self):
        if self.measure_mode is "simple":
            self.title1 = make_text(self.root, content="Coord", bg=tkcolour_from_rgb(BACKGROUND),
                              column=12, columnspan=1, row=0, width=8, text = self.title1)
            self.title2 = make_text(self.root, content="dist(px)", bg=tkcolour_from_rgb(BACKGROUND),
                              column=13, columnspan=1, row=0, width=8, text = self.title2)
            self.title3 = make_text(self.root, content="dist(mm)", bg=tkcolour_from_rgb(BACKGROUND),
                              column=14, columnspan=1, row=0, width=8, text = self.title3)
            self.title4 = make_text(self.root, content="cum(px)", bg=tkcolour_from_rgb(BACKGROUND),
                              column=15, columnspan=1, row=0, width=8, text = self.title4)
            self.title5 = make_text(self.root, content="cum(mm)", bg=tkcolour_from_rgb(BACKGROUND),
                              column=16, columnspan=1, row=0, width=8, text = self.title5)
        else:
            self.title1 = make_text(self.root, content="Center", bg=tkcolour_from_rgb(BACKGROUND),
                              column=12, columnspan=1, row=0, width=8, text = self.title1)
            self.title2 = make_text(self.root, content="len(px)", bg=tkcolour_from_rgb(BACKGROUND),
                              column=13, columnspan=1, row=0, width=8, text = self.title2)
            self.title3 = make_text(self.root, content="len(mm)", bg=tkcolour_from_rgb(BACKGROUND),
                              column=14, columnspan=1, row=0, width=8, text = self.title3)
            self.title4 = make_text(self.root, content="dist(px)", bg=tkcolour_from_rgb(BACKGROUND),
                              column=15, columnspan=1, row=0, width=8, text = self.title4)
            self.title5 = make_text(self.root, content="dist(mm)", bg=tkcolour_from_rgb(BACKGROUND),
                              column=16, columnspan=1, row=0, width=8, text = self.title5)
    
    def _build_centers_box(self):
        self.centers_listbox = make_listbox(self.root, row=1, column=12, rowspan=21, padx=(0, 15), pady=(0, 15), height = 35, width = 12)
        
    def _build_dists_box(self):
        self.dists_listbox = make_listbox(self.root, row=1, column=15, rowspan=21, padx=(0, 15), pady=(0, 15), height = 35, width = 8)
        
    def _build_lengths_box(self):
        self.lengths_listbox = make_listbox(self.root, row=1, column=13, rowspan=21, padx=(0, 15), pady=(0, 15), height = 35, width = 8)
        
    def _build_lengths_converted_box(self):
        self.lengths_listbox_converted = make_listbox(self.root, row=1, column=14, rowspan=21, padx=(0, 15), pady=(0, 15), height = 35, width = 8)
    
    def _build_conversion_factor_input(self):
        title = make_text(self.root, content="Push 'a' to switch measuring mode", bg=tkcolour_from_rgb(BACKGROUND),
                          column=11, columnspan=5, row=24, width=35, pady=(5, 5), padx=(5, 5))
        title = make_text(self.root, content="One pixel represents x mm:", bg=tkcolour_from_rgb(BACKGROUND),
                          column=11, columnspan=3, row=25, width=25, pady=(5, 5), padx=(5, 5))
        self.input_conversion_factor = make_entry(self.root, row=25, column=14, width=15, pady=(10, 10), columnspan=2)
        self.input_conversion_factor.bind('<Return>', self.update_conversion_factor)
        self.input_conversion_factor.delete(0,"end")
        self.input_conversion_factor.insert(0, str(self.conversion_factor))
        
    def _build_filename_entry(self):
        title = make_text(self.root, content="Filename:", bg=tkcolour_from_rgb(BACKGROUND),
                          column=11, columnspan=2, row=26, width=15, pady=(5, 5), padx=(5, 5))
        self.filename_entry = make_entry(self.root, row=26, column=13, width=35, pady=(10, 10), columnspan=4)
        self.filename_entry.bind('<Return>', self.update_filename)
        self.filename_entry.delete(0,"end")
        self.filename_entry.insert(0, self.filename)
        
    def _build_dists_converted_box(self):
        self.dists_listbox_converted = make_listbox(self.root, row=1, column=16, rowspan=21, padx=(0, 15), pady=(0, 15), height = 35, width = 8)
    
    def _build_save_tif(self):
        self.save_as_tif_label = make_button(self.root, "Save Image", row=28, column=9, outer_padx=(12, 0),
                                     outer_pady=(10, 15), inner_padx=10, inner_pady=5, rowspan = 1, columnspan=1, command = self.__save_image)
        

    def _build_eudis_text(self):
        if self.measure_mode is "complex":
            self.eudis_text = label = make_text(self.root, content="Line " + str(self.line_index+1) + ": " + str(self.lines[self.line_index]),
                                  bg=tkcolour_from_rgb(BACKGROUND), column=11, row=23, width=45, columnspan=7,
                                  padx=0, state=NORMAL, pady=0, text = self.eudis_text)
        else:
            self.eudis_text = make_text(self.root, content="Point " + str(self.line_index+1) + ": " + str(self.centers[self.line_index]) + " - 'c' to cut line.",
                                  bg=tkcolour_from_rgb(BACKGROUND), column=11, row=23, width=45, columnspan=7,
                                  padx=0, state=NORMAL, pady=0, text =self.eudis_text)
    


    # ---------------------------------------------- BUILDERS (IMAGE) -----------------------------------------------
        
    def _build_original_image(self, data):
        if data is None:
            # Placeholder
            self.original_image = make_label(self.root, "original image placeholder", row=1, column=1, rowspan=26,
                                             columnspan=10, inner_pady=300, inner_padx=400, outer_padx=(15, 10),
                                             outer_pady=(15, 10))
        else:
            #data = np.asarray(rgb_image_to_hsi_array(self.original_image_data)).reshape((480, 640))
            (self.original_image_graph, self.original_image, self.image_array) = \
                make_image(self.root, data, row=1, column=1, columnspan=10, rowspan=25, lower_scale_value=None,
                           upper_scale_value=None, color_rgb=BACKGROUND, original=True, figheight=7, figwidth=9, img = self.original_image, axs = self.original_image_graph, figu = self.original_image_graph)
            self.original_image.get_tk_widget().bind('<Button-1>', self.__get_coords)
            self.original_image.get_tk_widget().bind('<+>', self.__zoom)
            self.original_image.get_tk_widget().bind('<Key-minus>', self.__dezoom)
            self.original_image.get_tk_widget().bind('<Key-w>', self.__zoom)
            self.original_image.get_tk_widget().bind('<Key-s>', self.__dezoom)
            self.original_image.get_tk_widget().bind('<Key-x>', self.__save_xlsx)
            self.original_image.get_tk_widget().bind('<Leave>', self.__reset_mouse_position)
            self.original_image.get_tk_widget().bind('<Motion>', self.__update_mouse_position)
            self.original_image.get_tk_widget().bind('<Key-a>', self.__switch_measure_mode)
            self.original_image.get_tk_widget().bind('<Key-r>', self.__reset_lines)
            self.original_image.get_tk_widget().bind('<BackSpace>', self.__del_last)
            self.original_image.get_tk_widget().bind('<Key-c>', self.__cut_line)
            self.original_image.get_tk_widget().focus_force()
   
    # --------------------------------------------- IMAGE (NAVIGATING) -----------------------------------------------
            
    def __zoom(self, event):
        if self.zoom_factor < 16:
            self.zoom_factor = 2*self.zoom_factor
            self.view_mid[0] = round(self.view_mid[0] + self.mouse_y-240)*2
            self.view_mid[1] = round(self.view_mid[1] + self.mouse_x-320)*2
            max_x = self.zoom_factor*640-320
            max_y = self.zoom_factor*480 - 240
            if self.view_mid[0] < 240:
                self.view_mid[0] = 240
            if self.view_mid[1] < 320:
                self.view_mid[1] = 320
            if self.view_mid[0] > max_y:
                self.view_mid[0] = max_y
            if self.view_mid[1] > max_x:
                self.view_mid[1] = max_x
            self._draw_points()
        
        
    def __dezoom(self, event):
        if self.zoom_factor > 1:
            self.zoom_factor = round(0.5*self.zoom_factor)
            self.view_mid[0] = round((self.view_mid[0] + self.mouse_y-240)*0.5)
            self.view_mid[1] = round((self.view_mid[1] + self.mouse_x-320)*0.5)
            max_x = self.zoom_factor*640-320
            max_y = self.zoom_factor*480-240
            if self.view_mid[0] < 240:
                self.view_mid[0] = 240
            if self.view_mid[1] < 320:
                self.view_mid[1] = 320
            if self.view_mid[0] > max_y:
                self.view_mid[0] = max_y
            if self.view_mid[1] > max_x:
                self.view_mid[1] = max_x
            self._draw_points()
 
    # ---------------------------------------------  MOUSE POSITION ----------------------------------------      
               
    def __update_mouse_position(self, event):
        pos = self.original_image_graph.axes[0].get_position()
        axesX0 = pos.x0
        axesY0 = pos.y0
        axesX1 = pos.x1
        axesY1 = pos.y1
        canvas = event.widget
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        canvas.canvasx
        cx = canvas.winfo_rootx()
        cy = canvas.winfo_rooty()
        minX=width*axesX0
        maxX=width*axesX1
        minY=height*axesY0
        maxY=height*axesY1
        axWidth=maxX-minX
        conversionFactor = 640/axWidth
        Xc=int((event.x-minX)*conversionFactor)
        Yc=int((event.y-minY)*conversionFactor)
        if Xc>=0 and Yc>=0 and Xc<=640 and Yc<=480:
            self.mouse_x = Xc
            self.mouse_y = Yc
            Xc = round((self.view_mid[1]+Xc-320)/self.zoom_factor)
            Yc = round((self.view_mid[0]+Yc-240)/self.zoom_factor)
        not_none = [i for i in self.coords_list if i != (None, None)]
        if len(not_none)>=1:             
            pt1 = not_none[-1]
            pt2 = (Xc, Yc)
            a = pt1[0]-pt2[0]
            b = pt1[1]-pt2[1]
            c = np.sqrt(a*a + b*b)
            self._build_eudis_text()
        else :
            self._build_eudis_text() 
        self.original_image.get_tk_widget().focus_force()
            
    def __reset_mouse_position(self, event):
        self.mouse_x = 320
        self.mouse_y = 240

    # --------------------------------------------------- DRAWING -----------------------------------------------------

    def __del_last(self, event = None):
        self.line_index = self.line_index - 1
        if self.line_index == 0:
            self.line_index = 0
        if self.measure_mode is "complex":
            self.lines[self.line_index] = [(None, None), (None, None)]
            self.first = True
        self.centers[self.line_index] = (None, None)
        self._draw_points()
        self.__update_all_listboxes()
        self._build_eudis_text()

                        
        
        
    def _draw_points(self):
        copy_data = self.original_image_data.copy()
        for ii in range(100):
            if self.centers[ii][0] is not None:#
                y = int(self.centers[ii][0])
                x = int(self.centers[ii][1])
                for xi in range(-4, 5):
                    copy_data[(x + xi) % 480, y, :3] = BRIGHT_BLUE_RGB
                for yi in range(-4, 5):
                    copy_data[x, (y + yi) % 640, :3] = BRIGHT_BLUE_RGB
             
            
            jj = ii +1
            if jj == 100:
                jj=0
            
            if self.centers[ii][0] is not None and self.centers[jj][0] is not None:
                not_none = [self.centers[ii], self.centers[jj]]
                for point in not_none:
                    y = int(point[0])
                    x = int(point[1])
                    for xi in range(-4, 5):
                        copy_data[(x + xi) % 480, y, :3] = BRIGHT_GREEN_RGB
                        for yi in range(-4, 5):
                            copy_data[x, (y + yi) % 640, :3] = BRIGHT_GREEN_RGB
                    idx = not_none.index(point)
                    self._draw_a_line_green(not_none[idx - 1], not_none[idx], copy_data)
             
            if self.lines[ii][0][1] is not None and self.lines[ii][1][1] is not None:
                not_none = [self.lines[ii][0], self.lines[ii][1]]
                for point in not_none:
                    y = int(point[0])
                    x = int(point[1])
                    for xi in range(-4, 5):
                        copy_data[(x + xi) % 480, y, :3] = BRIGHT_GREEN_RGB
                        for yi in range(-4, 5):
                            copy_data[x, (y + yi) % 640, :3] = BRIGHT_GREEN_RGB
                    idx = not_none.index(point)
                    self._draw_a_line_blue(not_none[idx - 1], not_none[idx], copy_data)
        
        self.image_to_save = copy_data
        left = self.view_mid[1] - 320
        bottom = self.view_mid[0] - 240
        right = left + 640
        top = bottom + 480
        im = Image.fromarray(copy_data)
        im = im.resize((640*self.zoom_factor, 480*self.zoom_factor)) 
        im = im.crop((left, bottom, right, top))
        self._build_original_image(np.array(im))
        self.original_image.get_tk_widget().focus_force()
          
    @staticmethod
    def _draw_a_line_green(point1, point2, image):
        r0, c0 = point1
        r1, c1 = point2
        rr, cc, val = line_aa(c0, r0, c1, r1)
        for i in range(len(rr)):
            image[rr[i] % 480, cc[i] % 640] = (int(113 * val[i]), int(255 * val[i]), int(66 * val[i]))
        return image
    
    @staticmethod
    def _draw_a_line_blue(point1, point2, image):
        r0, c0 = point1
        r1, c1 = point2
        rr, cc, val = line_aa(c0, r0, c1, r1)
        for i in range(len(rr)):
            image[rr[i] % 480, cc[i] % 640] = (int(66 * val[i]), int(113 * val[i]), int(255 * val[i]))
        return image

    # --------------------------------------------- ADDING/REMOVING COORDS --------------------------------------------

    def __get_coords(self, event):
        pos = self.original_image_graph.axes[0].get_position()
        axesX0 = pos.x0
        axesY0 = pos.y0
        axesX1 = pos.x1
        axesY1 = pos.y1
        canvas = event.widget
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        canvas.canvasx
        cx = canvas.winfo_rootx()
        cy = canvas.winfo_rooty()
        minX=width*axesX0
        maxX=width*axesX1
        minY=height*axesY0
        maxY=height*axesY1
        axWidth=maxX-minX
        conversionFactor = 640/axWidth
        Xc=int((event.x-minX)*conversionFactor)
        Yc=int((event.y-minY)*conversionFactor)         
        Xc = round((self.view_mid[1]+Xc-320)/self.zoom_factor)
        Yc = round((self.view_mid[0]+Yc-240)/self.zoom_factor)
        if Xc>=0 and Yc>=0 and Xc<=640 and Yc<=480:
            if self.measure_mode is "complex":
                if self.first or self.lines[self.line_index][0] is None:
                    self.lines[self.line_index][0] = (Xc, Yc)
                    self.first = False
                else:
                    self.lines[self.line_index][1] = (Xc, Yc)
                    self.line_index = self.line_index + 1
                    if self.line_index == 100:
                        self.line_index = 0
                    self.first = True
            else:
                self.centers[self.line_index] = (Xc, Yc)
                self.line_index = self.line_index + 1
                if self.line_index == 100:
                    self.line_index = 0
            self.__update_all_listboxes()
            self._build_eudis_text()
        
        self._draw_points()
            
    # ----------------------------------------------- UPDATERS (IMAGE) ------------------------------------------------

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


    # ------------------------------------------------- UPDATE MEASURMENTS & LINES --------------------------------------------------
        
    def __insert_lines(self):
        self.line_listbox.delete(0,'end')
        for ii in range(100):
            self.__add_line(ii)
        self.line_listbox.select_set(self.line_index)
        
    def __insert_centers(self):
        self.centers_listbox.delete(0,'end')
        for ii in range(100):
            self.__add_center(ii)
        
    def __insert_dists(self):
        if self.measure_mode is "simple":
            self.lengths_listbox.delete(0,'end')
        self.dists_listbox.delete(0,'end')
        for ii in range(100):
            self.__add_dist(ii)
     
    def __insert_dists_converted(self):
        if self.measure_mode is "simple":
            self.lengths_listbox_converted.delete(0,'end')
        self.dists_listbox_converted.delete(0,'end')
        for ii in range(100):
            self.__add_dist_converted(ii)
            
    def __insert_lengths(self):
        if self.measure_mode is "complex":
            self.lengths_listbox.delete(0,'end')
            for ii in range(100):
                self.__add_length(ii)
     
    def __insert_lengths_converted(self):
        if self.measure_mode is "complex":
            self.lengths_listbox_converted.delete(0,'end')
            for ii in range(100):
                self.__add_length_converted(ii)
    
    def __update_selected_line(self, event):
        self.first = True
        self.line_index = self.line_listbox.curselection()[0]
        self._build_eudis_text()
    
    def __update_all_listboxes(self):
        self.__calc_centers()
        self.__calc_dists()
        self.__calc_lengths()
        self.__insert_lines()
        self.__insert_centers()
        self.__insert_dists()
        self.__insert_dists_converted()
        self.__insert_lengths()
        self.__insert_lengths_converted()
    
    def __reset_lines(self, event = None):
        self.lines = [[(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)]
                      ]
        self.centers = [(None, None)]*100           
        self.dists = [None]*100
        self.lengths = [None]*100
        self.cum_dists = [None]*100        
        self.line_index = 0
        self.first = True
        self.__update_all_listboxes()
        self._draw_points()
        
    def __calc_centers(self):
        for ii in range(100):
            if self.lines[ii][0][1] is not None and self.lines[ii][1][1] is not None:
                pt1 = self.lines[ii][0]
                pt2 = self.lines[ii][1]
                center1 = int(round((pt1[0] + pt2[0])/2))
                center2 = int(round((pt1[1] + pt2[1])/2))
                self.centers[ii] = (center1, center2)
    
    def __calc_dists(self):
        cc = 0
        for ii in range(100):
            if ii == 100:
                ii = 0
            jj = ii + 1
            if jj == 100:
                jj = 0
            if self.centers[ii][1] is not None and self.centers[jj][1] is not None:
                pt1 = self.centers[ii]
                pt2 = self.centers[jj]
                dist_x = pt1[0] - pt2[0] 
                dist_y = pt1[1] - pt2[1] 
                self.dists[ii] = np.sqrt(dist_x * dist_x + dist_y * dist_y)
                self.cum_dists[ii] = sum(self.dists[cc:ii+1])
            else:
                cc = jj

    def __calc_lengths(self):
        for ii in range(100):
            if ii == 100:
                ii = 0
            jj = ii + 1
            if jj == 100:
                jj = 0
            if self.lines[ii][0][0] is not None and self.lines[ii][1][0] is not None:
                pt1 = self.lines[ii][0]
                pt2 = self.lines[ii][1]
                dist_x = pt1[0] - pt2[0] 
                dist_y = pt1[1] - pt2[1] 
                self.lengths[ii] = np.sqrt(dist_x * dist_x + dist_y * dist_y)
            
    
    def __add_line(self, index):
        if self.measure_mode is "simple":
            not_none_idx = [x for x in range(100) if self.centers[x][0]]
            if index in not_none_idx:
                index_2 = not_none_idx.index(index)
                concat_path = "Point " + str(index_2+1)
                self.line_listbox.insert(END, concat_path)
        else:
            concat_path = "Line " + str(index+1)
            self.line_listbox.insert(END, concat_path)
    
    def __add_center(self, index):
        if self.measure_mode is "simple":
            not_none_idx = [x for x in range(100) if self.centers[x][0]]
            if index in not_none_idx:
                concat_path = str(self.centers[index])
                self.centers_listbox.insert(END, concat_path)
        else:
            concat_path = str(self.centers[index])
            self.centers_listbox.insert(END, concat_path)
        
    def __add_dist(self, index):
        if self.measure_mode is "complex":
            concat_path = str(self.dists[index])
            self.dists_listbox.insert(END, concat_path)
        else:
            if self.measure_mode is "simple":
                not_none_idx = [x for x in range(100) if self.centers[x][0]]
                if index in not_none_idx:
                    concat_path = str(self.dists[index])
                    concat_path_2 = str(self.cum_dists[index])
                    self.lengths_listbox.insert(END, concat_path)
                    self.dists_listbox.insert(END, concat_path_2)
            
        
    def __add_dist_converted(self, index):
        if self.measure_mode is "complex":
            if self.dists[index] is not None:
                concat_path = str(self.dists[index]*self.conversion_factor)
            else:
                concat_path = str(self.dists[index])
            self.dists_listbox_converted.insert(END, concat_path)
        else:
            if self.measure_mode is "simple":
                not_none_idx = [x for x in range(100) if self.centers[x][0]]
                if index in not_none_idx:
                    if self.dists[index] is not None:
                        concat_path = str(self.dists[index]*self.conversion_factor)
                        concat_path_2 = str(self.cum_dists[index]*self.conversion_factor)
                    else:
                        concat_path = str(self.dists[index])
                        concat_path_2 = str(self.cum_dists[index])
                    self.lengths_listbox_converted.insert(END, concat_path)
                    self.dists_listbox_converted.insert(END, concat_path_2)
    
    def __add_length(self, index):
        if self.measure_mode is "simple":
            not_none_idx = [x for x in range(100) if self.centers[x][0]]
            if index in not_none_idx:
                concat_path = str(self.lengths[index])
                self.lengths_listbox.insert(END, concat_path)
        else:
            concat_path = str(self.lengths[index])
            self.lengths_listbox.insert(END, concat_path)
        
    def __add_length_converted(self, index):
        if self.measure_mode is "simple":
            not_none_idx = [x for x in range(100) if self.centers[x][0]]
            if index in not_none_idx:
                if self.lengths[index] is not None:
                    concat_path = str(self.lengths[index]*self.conversion_factor)
                else:
                    concat_path = str(self.lengths[index])
                self.lengths_listbox_converted.insert(END, concat_path)
        else:
            if self.lengths[index] is not None:
                concat_path = str(self.lengths[index]*self.conversion_factor)
            else:
                concat_path = str(self.lengths[index])
            self.lengths_listbox_converted.insert(END, concat_path)

    # -------------------------------------------------- SELECTION LISTBOX / LOADING DATACUBES -----------------------------------

    def __update_selected_data_cube(self, event):
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
        self.original_image.get_tk_widget().focus_force()
        self.counter = 0
        self._new_filename()
        if not self.keep:
            self.__reset_lines()
            self.__read_file()
        

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
                # Add the new data to current class
                self.data_cube_paths.append(dc_path)

                # Display the data cube
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
    
    def __next(self):
        if len(self.selection_listbox.curselection())>0:
            sel = self.selection_listbox.curselection()[0]
        else:
            sel = self.current_dc_path
        self.selection_listbox.selection_clear(0, END)
        self.selection_listbox.select_set(sel+1) #This only sets focus on the first item.
        self.selection_listbox.event_generate("<<ListboxSelect>>")
        #self.__remove_pt('all')

    @staticmethod
    def __get_sub_folder_paths(path_to_main_folder, recursive = False): 
        #contents = os.listdir(path_to_main_folder)
        # Adds the path to the main folder in front for traversal
        #sub_folders = [path_to_main_folder + "/" + i for i in contents if bool(re.match('[\d/-_]+$', i))]
        sub_folders = sorted(glob.glob(path_to_main_folder+"/**/", recursive = recursive))
        return sub_folders
    
    def __trash_list(self):
        self.data_cube_paths = []
        self.selection_listbox.delete(0,'end')
        self.__remove_pt('all')
     
    # ------------------------------------------------ SAVING ---------------------------------------------------        
        
    def __save_image(self):
        path = os.path.dirname(self.get_selected_data_cube_path())
        if not os.path.exists(path + "/_measuring"):
            os.mkdir(path + "/_measuring")
        path = path + "/_measuring"+"/"+ self.filename + '.png'
        img = Image.fromarray(self.image_to_save)
        img.save(path)
        
    def __save_xlsx(self, event = None):
        self.filename = self.filename_entry.get()
        path = os.path.dirname(self.get_selected_data_cube_path())
        if not os.path.exists(path + "/_measuring"):
               os.mkdir(path + "/_measuring")
        path = path + "/_measuring"+"/" + self.filename + '.xlsx'
        workbook = xlsxwriter.Workbook(path)
        bold = workbook.add_format({'bold': True})
        worksheet = workbook.add_worksheet()
        if self.measure_mode is "complex":
            worksheet.write(0, 0, 'Line Coordinates', bold)
            worksheet.write(0, 1, 'Length in px', bold)
            worksheet.write(0, 2, 'Length in mm', bold)
            worksheet.write(0, 3, 'Center of Line', bold)
            worksheet.write(0, 4, 'Distance to next Center in px', bold)
            worksheet.write(0, 5, 'Distance to next Center in mm', bold)
            worksheet.write(0, 6, 'Conversion Factor in mm', bold)
            worksheet.write(1, 6, self.conversion_factor)
            for ii in range(100):
                if self.lines[ii][1][1] is not None:
                    worksheet.write(ii+1, 0, str(self.lines[ii][0]) + str(self.lines[ii][1]))
                if self.lengths[ii] is not None:
                    worksheet.write(ii+1, 1, np.round(self.lengths[ii],5))
                    worksheet.write(ii+1, 2, np.round(self.lengths[ii]*self.conversion_factor,5))
                if self.centers[ii][1] is not None:
                    worksheet.write(ii+1, 3, str(self.centers[ii]))
                if self.dists[ii] is not None:
                    worksheet.write(ii+1, 4, np.round(self.dists[ii],5))
                    worksheet.write(ii+1, 5, np.round(self.dists[ii]*self.conversion_factor,5))
        else:
            worksheet.write(0, 0, 'Point Coordinates', bold)
            worksheet.write(0, 1, 'Distance to next Point in px', bold)
            worksheet.write(0, 2, 'Distance to next Point in mm', bold)
            worksheet.write(0, 3, 'Cumulative Distance in px', bold)
            worksheet.write(0, 4, 'Cumulative Distance in mm', bold)
            worksheet.write(0, 5, 'Conversion Factor in mm', bold)
            worksheet.write(1, 5, self.conversion_factor)
            cc = 0
            for ii in range(100):
                if self.centers[ii][1] is not None:
                    worksheet.write(cc+1, 0, str(self.centers[ii]))
                if self.dists[ii] is not None:
                    worksheet.write(cc+1, 1, np.round(self.dists[ii],5))
                    worksheet.write(cc+1, 2, np.round(self.dists[ii]*self.conversion_factor,5))   
                    worksheet.write(cc+1, 3, np.round(self.cum_dists[ii],5))
                    worksheet.write(cc+1, 4, np.round(self.cum_dists[ii]*self.conversion_factor,5))   
                if self.centers[ii][1] is not None:
                    cc = cc+1
        workbook.close()   
        self._new_filename()
    
    def __read_file(self):
        self.__reset_lines()
        if self.load_recent:
            path = os.path.dirname(self.get_selected_data_cube_path())
            path = path + "/_measuring/*.xlsx"
            files = glob.glob(path)
            if len(files) >0:
                path = max(files, key=os.path.getctime)   
                dfs = pd.read_excel(path, sheet_name=None)
                df = dfs["Sheet1"]
                if "Point Coordinates" in df.columns:
                    self.measure_mode = "simple"
                    coords = list(df["Point Coordinates"])
                    for ii, coord in enumerate(coords):
                        Xc = int(coord.replace("(", "").replace(")", "").split(", ")[0])
                        Yc = int(coord.replace("(", "").replace(")", "").split(", ")[1])
                        self.centers[self.line_index] = (Xc, Yc)
                        self.line_index = self.line_index + 1
                        if self.line_index == 100:
                            self.line_index = 0 
                        if np.any(np.isnan(df.iloc[ii, 1])):
                            self.line_index = self.line_index + 1
                            if self.line_index == 100:
                                self.line_index = 0 
                elif "Line Coordinates" in df.columns:
                    self.measure_mode = "complex"
                    lines = list(df["Line Coordinates"])
                    for ii, line in enumerate(lines):
                        X1 = int(line.replace("]", "").replace(" ", "").replace("[", "").replace("(", "").replace(")", ",").split(",")[0])
                        X2 = int(line.replace("]", "").replace(" ", "").replace("[", "").replace("(", "").replace(")", ",").split(",")[1])
                        X3 = int(line.replace("]", "").replace(" ", "").replace("[", "").replace("(", "").replace(")", ",").split(",")[2])
                        X4 = int(line.replace("]", "").replace(" ", "").replace("[", "").replace("(", "").replace(")", ",").split(",")[3])
                        self.lines[self.line_index] = [(X1, X2), (X3, X4)]
                        self.line_index = self.line_index + 1
                        if self.line_index == 100:
                            self.line_index = 0
                self.__update_all_listboxes()
                self._build_eudis_text()
                self._draw_points()
        else:
            path = os.path.dirname(self.get_selected_data_cube_path())
            path = path + "/_measuring"+"/" + self.filename + '.xlsx'
            if os.path.exists(path):
                dfs = pd.read_excel(path, sheet_name=None)
                df = dfs["Sheet1"]
                if "Point Coordinates" in df.columns:
                    self.measure_mode = "simple"
                    coords = list(df["Point Coordinates"])
                    for ii, coord in enumerate(coords):
                        Xc = int(coord.replace("(", "").replace(")", "").split(", ")[0])
                        Yc = int(coord.replace("(", "").replace(")", "").split(", ")[1])
                        self.centers[self.line_index] = (Xc, Yc)
                        self.line_index = self.line_index + 1
                        if self.line_index == 100:
                            self.line_index = 0 
                        if np.any(np.isnan(df.iloc[ii, 1])):
                            self.line_index = self.line_index + 1
                            if self.line_index == 100:
                                self.line_index = 0 
                    
                elif "Line Coordinates" in df.columns:
                    self.measure_mode = "complex"
                    lines = list(df["Line Coordinates"])
                    for ii, line in enumerate(lines):
                        X1 = int(line.replace("]", "").replace(" ", "").replace("[", "").replace("(", "").replace(")", ",").split(",")[0])
                        X2 = int(line.replace("]", "").replace(" ", "").replace("[", "").replace("(", "").replace(")", ",").split(",")[1])
                        X3 = int(line.replace("]", "").replace(" ", "").replace("[", "").replace("(", "").replace(")", ",").split(",")[2])
                        X4 = int(line.replace("]", "").replace(" ", "").replace("[", "").replace("(", "").replace(")", ",").split(",")[3])
                        self.lines[self.line_index] = [(X1, X2), (X3, X4)]
                        self.line_index = self.line_index + 1
                        if self.line_index == 100:
                            self.line_index = 0
            self.__update_all_listboxes()
            self._build_eudis_text()
            self._draw_points()
                
        
    def _new_filename(self):
        self.counter = self.counter +1
        if not self.name_unique:
            if self.measure_mode is "simple":
                self.filename = "_measuring_results_SIMPLE_"+str(self.counter)
            else:
                self.filename = "_measuring_results_MIDDLE_"+str(self.counter)
        else:
                self.filename = self.filename_unique
        self._insert_filename()
    
    def __save_measure_and_next(self):
        self.__save_image()
        self.__save_xlsx()
        self.__next()

    # ------------------------------------------ MEASUREING (NAVIGATION) ---------------------------------------------
    
    def __switch_measure_mode(self, event = None):
        if self.measure_mode is "simple":
            self.measure_mode = "complex"
        else:
            self.measure_mode = "simple"
        self.__reset_lines()
        self._build_titles()
        self._build_eudis_text()
        self.counter = 0
        self._new_filename()
        
    def __cut_line(self, event = None):
        if self.measure_mode is  "simple":
            if self.line_index is not 0:
                self.line_index = self.line_index +1
                
    # --------------------------------------- MISC ----------------------------------
        
    def __info(self): 
        info = self.listener.modules[INFO].measure_info
        title = "Measure Tool"
        make_info(title=title, info=info)