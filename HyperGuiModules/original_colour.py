from HyperGuiModules.utility import *
from HyperGuiModules.constants import *
from skimage.draw import line_aa
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw
import numpy as np
import logging
import csv
import os
import math


class OGColour:
    def __init__(self, original_color_frame, listener):
        self.root = original_color_frame

        # Listener
        self.listener = listener
        self.segm = False
        self.recr = False
        self.label = [None]*10
        self.remove = [None]*10
        self.checkbox = [None]*10
        self.view_mid = [240, 320]
        self.zoom_factor = 1
        self.mouse_x = 320
        self.mouse_y = 240
    

        self.rgb_button = None
        self.rgb_checkbox = None
        self.rgb_checkbox_value_iv = IntVar()
        self.rgb_checkbox_value = False

        self.sto2_button = None
        self.sto2_checkbox = None
        self.sto2_checkbox_value_iv = IntVar()
        self.sto2_checkbox_value = False

        self.nir_button = None
        self.nir_checkbox = None
        self.nir_checkbox_value_iv = IntVar()
        self.nir_checkbox_value = False

        self.thi_button = None
        self.thi_checkbox = None
        self.thi_checkbox_value_iv = IntVar()
        self.thi_checkbox_value = False

        self.twi_button = None
        self.twi_checkbox = None
        self.twi_checkbox_value_iv = IntVar()
        self.twi_checkbox_value = False

        self.ohi_button = None
        self.ohi_checkbox = None
        self.ohi_checkbox_value_iv = IntVar()
        self.ohi_checkbox_value = False
        
        self.tli_button = None
        self.tli_checkbox = None
        self.tli_checkbox_value_iv = IntVar()
        self.tli_checkbox_value = False

        self.gs = False
        self.gs_dropdown = None
        self.gs_var = StringVar()
        self.gs_choices = ['CS (Colour Scale)', 'GS (Grey Scale)']

        self.mask_to_csv_button = None
        self.bin_mask_button = None

        self.save_label = None
        self.save_checkbox = None
        self.save_checkbox_value_iv = IntVar()
        self.save_checkbox_value = False
        self.segm_checkbox_value = IntVar()
        self.recr_checkbox_value = IntVar()
        self.save_as_tif_checkbox_value = IntVar()
        self.save_tif_bool = False
        self.save_coord_bool = False

        self.pt1_label = None
        self.pt1_remove = None
        self.pt1_checkbox = None
        self.pt1_checkbox_value = IntVar()

        self.pt2_label = None
        self.pt2_remove = None
        self.pt2_checkbox = None
        self.pt2_checkbox_value = IntVar()

        self.pt3_label = None
        self.pt3_remove = None
        self.pt3_checkbox = None
        self.pt3_checkbox_value = IntVar()

        self.pt4_label = None
        self.pt4_remove = None
        self.pt4_checkbox = None
        self.pt4_checkbox_value = IntVar()

        self.pt5_label = None
        self.pt5_remove = None
        self.pt5_checkbox = None
        self.pt5_checkbox_value = IntVar()

        self.pt6_label = None
        self.pt6_remove = None
        self.pt6_checkbox = None
        self.pt6_checkbox_value = IntVar()

        self.pt7_label = None
        self.pt7_remove = None
        self.pt7_checkbox = None
        self.pt7_checkbox_value = IntVar()

        self.pt8_label = None
        self.pt8_remove = None
        self.pt8_checkbox = None
        self.pt8_checkbox_value = IntVar()

        self.pt9_label = None
        self.pt9_remove = None
        self.pt9_checkbox = None
        self.pt9_checkbox_value = IntVar()

        self.pt10_label = None
        self.pt10_remove = None
        self.pt10_checkbox = None
        self.pt10_checkbox_value = IntVar()

        self.all_points_remove = None
        self.all_points_checkbox = None
        self.all_points_checkbox_value = IntVar()

        self.use_mask_button = None
        self.instant_save_button = None
        self.input_coords_button = None
        self.upload_mask_button = None

        self.coords_window = None
        self.input_points_title = None
        self.go_button = None

        self.input_pt1_title = None
        self.input_pt1_title_x = None
        self.input_pt1_x = None
        self.input_pt1_title_y = None
        self.input_pt1_y = None

        self.input_pt2_title = None
        self.input_pt2_title_x = None
        self.input_pt2_x = None
        self.input_pt2_title_y = None
        self.input_pt2_y = None

        self.input_pt3_title = None
        self.input_pt3_title_x = None
        self.input_pt3_x = None
        self.input_pt3_title_y = None
        self.input_pt3_y = None

        self.input_pt4_title = None
        self.input_pt4_title_x = None
        self.input_pt4_x = None
        self.input_pt4_title_y = None
        self.input_pt4_y = None

        self.input_pt5_title = None
        self.input_pt5_title_x = None
        self.input_pt5_x = None
        self.input_pt5_title_y = None
        self.input_pt5_y = None

        self.input_pt6_title = None
        self.input_pt6_title_x = None
        self.input_pt6_x = None
        self.input_pt6_title_y = None
        self.input_pt6_y = None

        self.input_pt7_title = None
        self.input_pt7_title_x = None
        self.input_pt7_x = None
        self.input_pt7_title_y = None
        self.input_pt7_y = None

        self.input_pt8_title = None
        self.input_pt8_title_x = None
        self.input_pt8_x = None
        self.input_pt8_title_y = None
        self.input_pt8_y = None

        self.input_pt9_title = None
        self.input_pt9_title_x = None
        self.input_pt9_x = None
        self.input_pt9_title_y = None
        self.input_pt9_y = None

        self.input_pt10_title = None
        self.input_pt10_title_x = None
        self.input_pt10_x = None
        self.input_pt10_title_y = None
        self.input_pt10_y = None

        self.original_image_graph = None
        self.original_image_data = None
        self.original_image = None
        self.image_array = None

        self.pop_up_graph = None
        self.pop_up_window = None
        self.pop_up_image = None
        self.pop_up = False
        self.input_pt_title_list = [None for ii in range(1000)] 
        self.input_pt_title_x_list = [None for ii in range(1000)] 
        self.input_pt_title_y_list = [None for ii in range(1000)] 
        self.input_pt_x_list = [None for ii in range(1000)]  
        self.input_pt_y_list = [None for ii in range(1000)]  
        
        self.tif_save_path = None
        self.tif_save_path_end = None
        self.automatic_names =True

        self.info_label = None

        # coords in dimensions of image, i.e. xrange=[1, 640], yrange=[1, 480]
        self.coords_list = [(None, None) for _ in range(1000000)]
        self.mask_raw = None

        self._init_widget()

        self.displayed_image_mode = RGB  # RGB by default
        self.rgb_button.config(foreground="red")

    # ---------------------------------------------- UPDATER AND GETTERS ----------------------------------------------

    def update_original_image(self, original_image_data):
        print(original_image_data.shape)
        self.original_image_data = original_image_data
        self._draw_points()
        self._update_tif_save_path()

    def get_bools(self):
        return [self.get_pt1_checkbox_value(), self.get_pt2_checkbox_value(), self.get_pt3_checkbox_value(),
                self.get_pt4_checkbox_value(), self.get_pt5_checkbox_value(), self.get_pt6_checkbox_value(),
                self.get_pt7_checkbox_value(), self.get_pt8_checkbox_value(), self.get_pt9_checkbox_value(),
                self.get_pt10_checkbox_value()] + [True for i in range (999990)]

    def get_pt1_checkbox_value(self):
        return not bool(self.pt1_checkbox_value.get())

    def get_pt2_checkbox_value(self):
        return not bool(self.pt2_checkbox_value.get())

    def get_pt3_checkbox_value(self):
        return not bool(self.pt3_checkbox_value.get())

    def get_pt4_checkbox_value(self):
        return not bool(self.pt4_checkbox_value.get())

    def get_pt5_checkbox_value(self):
        return not bool(self.pt5_checkbox_value.get())

    def get_pt6_checkbox_value(self):
        return not bool(self.pt6_checkbox_value.get())

    def get_pt7_checkbox_value(self):
        return not bool(self.pt7_checkbox_value.get())

    def get_pt8_checkbox_value(self):
        return not bool(self.pt8_checkbox_value.get())

    def get_pt9_checkbox_value(self):
        return not bool(self.pt7_checkbox_value.get())

    def get_pt10_checkbox_value(self):
        return not bool(self.pt8_checkbox_value.get())

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widget(self):
        self._build_gs_dropdown()
        self._build_mask_to_csv_button()
        self._build_upload_bin_mask_button()
        self._build_rgb()
        self._build_sto2()
        self._build_nir()
        self._build_thi()
        self._build_twi()
        self._build_tli()
        self._build_ohi()
        self._build_points()
        self._build_all_points()
        self._build_save()
        self._build_segm()
        self._build_recr()
        self._build_use_mask_button()
        self._build_instant_save_button()
        self._build_edit_coords_button()
        self._build_upload_mask_button()
        self._build_info_label()
        self._build_original_image(self.original_image_data)
        self._build_save_tif()
        self._build_tif_save_path_input()
        self._build_tif_save_path_text()
        self._build_autonames_button()

    # ---------------------------------------------- BUILDERS (DISPLAY) -----------------------------------------------

    def _build_rgb(self):
        self.rgb_button = make_button(self.root, text='RGB', width=3, command=self.__update_to_rgb, row=2, column=0,
                                      columnspan=1, inner_pady=2, outer_padx=(15, 5))
        self.rgb_checkbox = make_checkbox(self.root, "", row=2, column=0, columnspan=1, var=self.rgb_checkbox_value_iv,
                                          inner_padx=0, inner_pady=0, outer_padx=(0, 3), sticky=NE)
        self.rgb_checkbox.deselect()
        self.rgb_checkbox.bind('<Button-1>', self.__update_rgb_check_status)

    def _build_sto2(self):
        self.sto2_button = make_button(self.root, text='StO2', width=4, command=self.__update_to_sto2, row=2, column=1,
                                       columnspan=1, inner_pady=5, outer_padx=(0, 5))
        self.sto2_checkbox = make_checkbox(self.root, "", row=2, column=1, columnspan=1, var=self.sto2_checkbox_value_iv,
                                           inner_padx=0, inner_pady=0, outer_padx=(0, 3), sticky=NE)
        self.sto2_checkbox.deselect()
        self.sto2_checkbox.bind('<Button-1>', self.__update_sto2_check_status)

    def _build_nir(self):
        self.nir_button = make_button(self.root, text='NIR', width=3, command=self.__update_to_nir, row=2, column=2,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5))
        self.nir_checkbox = make_checkbox(self.root, "", row=2, column=2, columnspan=1, var=self.nir_checkbox_value_iv,
                                          inner_padx=0, inner_pady=0, outer_padx=(0, 3), sticky=NE)
        self.nir_checkbox.deselect()
        self.nir_checkbox.bind('<Button-1>', self.__update_nir_check_status)

    def _build_thi(self):
        self.thi_button = make_button(self.root, text='THI', width=3, command=self.__update_to_thi, row=2, column=3,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5))
        self.thi_checkbox = make_checkbox(self.root, "", row=2, column=3, columnspan=1, var=self.thi_checkbox_value_iv,
                                          inner_padx=0, inner_pady=0, outer_padx=(0, 3), sticky=NE)
        self.thi_checkbox.deselect()
        self.thi_checkbox.bind('<Button-1>', self.__update_thi_check_status)

    def _build_twi(self):
        self.twi_button = make_button(self.root, text='TWI', width=3, command=self.__update_to_twi, row=2, column=4,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5))
        self.twi_checkbox = make_checkbox(self.root, "", row=2, column=4, columnspan=1, var=self.twi_checkbox_value_iv,
                                          inner_padx=0, inner_pady=0, outer_padx=(0, 3), sticky=NE)
        self.twi_checkbox.deselect()
        self.twi_checkbox.bind('<Button-1>', self.__update_twi_check_status)
        
    def _build_tli(self):
        self.tli_button = make_button(self.root, text='TLI', width=3, command=self.__update_to_tli, row=2, column=5,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5))
        self.tli_checkbox = make_checkbox(self.root, "", row=2, column=5, columnspan=1, var=self.tli_checkbox_value_iv,
                                          inner_padx=0, inner_pady=0, outer_padx=(0, 3), sticky=NE)
        self.tli_checkbox.deselect()
        self.tli_checkbox.bind('<Button-1>', self.__update_tli_check_status)
        
    def _build_ohi(self):
        self.ohi_button = make_button(self.root, text='OHI', width=3, command=self.__update_to_ohi, row=2, column=6,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5))
        self.ohi_checkbox = make_checkbox(self.root, "", row=2, column=6, columnspan=1, var=self.ohi_checkbox_value_iv,
                                          inner_padx=0, inner_pady=0, outer_padx=(0, 3), sticky=NE)
        self.ohi_checkbox.deselect()
        self.ohi_checkbox.bind('<Button-1>', self.__update_ohi_check_status)


    # ----------------------------------------------- BUILDERS (POINTS) -----------------------------------------------

    def _build_all_points(self):
        # remove
        self.all_points_remove = make_button(self.root, text='x', width=1, command=lambda: self.__remove_pt('all'),
                                             row=2, column=9, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10,
                                             highlightthickness=0)
        
        self.last_point_remove = make_button(self.root, text='undo last', width=10, command=lambda: self.__remove_pt('last'),
                                             row=2, column=8, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10,
                                             highlightthickness=0)
        # checkbox
        self.all_points_checkbox = make_checkbox(self.root, "", row=2, column=10, columnspan=1,
                                                 var=self.all_points_checkbox_value, inner_padx=0, inner_pady=0,
                                                 outer_padx=(0, 15), sticky=W)
        self.all_points_checkbox.deselect()
        self.all_points_checkbox.bind('<Button-1>', self.__update_all_points_checked)

    def _build_points(self):
        self._build_pt1()
        self._build_pt2()
        self._build_pt3()
        self._build_pt4()
        self._build_pt5()
        self._build_pt6()
        self._build_pt7()
        self._build_pt8()
        self._build_pt9()
        self._build_pt10()

    def _build_ptn(self, num, var):
        # label
        # display points on interval [1, max] because ??????
        if self.coords_list[num] == (None, None):
            self.label[num] = make_text(self.root, content="Pt " + str(num) + ': ' + str(self.coords_list[num]),
                              bg=tkcolour_from_rgb(BACKGROUND), column=7, row=num + 3, width=18, columnspan=3,
                              padx=0, state=NORMAL, text = self.label[num])
        else:
            self.label[num] = make_text(self.root,
                              content="Pt " + str(num) + ': ' + str(tuple(x + 1 for x in self.coords_list[num])),
                              bg=tkcolour_from_rgb(BACKGROUND), column=7, row=num + 3, width=18, columnspan=3, padx=0,
                              state=NORMAL, text = self.label[num])
        # remove
        self.remove[num] = make_button(self.root, text='x', width=1, command=lambda: self.__remove_pt(num + 1), row=num + 3,
                             column=9, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10,
                             highlightthickness=0, button = self.remove[num])
        # checkbox
        self.checkbox[num] = make_checkbox(self.root, "", row=num + 3, column=10, columnspan=1, var=var, inner_padx=0,
                                 inner_pady=0,
                                 outer_padx=(0, 15), sticky=W, checkbox = self.checkbox[num])
        return self.label[num], self.remove[num], self.checkbox[num]

    def _build_pt1(self):
        # text
        self.pt1_label, self.pt1_remove, self.pt1_checkbox = self._build_ptn(0, self.pt1_checkbox_value)
        self.pt1_checkbox.deselect()
        self.pt1_checkbox.bind('<Button-1>', self.__update_pt1_checked)

    def _build_pt2(self):
        # text
        self.pt2_label, self.pt2_remove, self.pt2_checkbox = self._build_ptn(1, self.pt2_checkbox_value)
        self.pt2_checkbox.deselect()
        self.pt2_checkbox.bind('<Button-1>', self.__update_pt2_checked)

    def _build_pt3(self):
        # text
        self.pt3_label, self.pt3_remove, self.pt3_checkbox = self._build_ptn(2, self.pt3_checkbox_value)
        self.pt3_checkbox.deselect()
        self.pt3_checkbox.bind('<Button-1>', self.__update_pt3_checked)

    def _build_pt4(self):
        # text
        self.pt4_label, self.pt4_remove, self.pt4_checkbox = self._build_ptn(3, self.pt4_checkbox_value)
        self.pt4_checkbox.deselect()
        self.pt4_checkbox.bind('<Button-1>', self.__update_pt4_checked)

    def _build_pt5(self):
        self.pt5_label, self.pt5_remove, self.pt5_checkbox = self._build_ptn(4, self.pt5_checkbox_value)
        self.pt5_checkbox.deselect()
        self.pt5_checkbox.bind('<Button-1>', self.__update_pt5_checked)

    def _build_pt6(self):
        self.pt6_label, self.pt6_remove, self.pt6_checkbox = self._build_ptn(5, self.pt6_checkbox_value)
        self.pt6_checkbox.deselect()
        self.pt6_checkbox.bind('<Button-1>', self.__update_pt6_checked)

    def _build_pt7(self):
        self.pt7_label, self.pt7_remove, self.pt7_checkbox = self._build_ptn(6, self.pt7_checkbox_value)
        self.pt7_checkbox.deselect()
        self.pt7_checkbox.bind('<Button-1>', self.__update_pt7_checked)

    def _build_pt8(self):
        self.pt8_label, self.pt8_remove, self.pt8_checkbox = self._build_ptn(7, self.pt8_checkbox_value)
        self.pt8_checkbox.deselect()
        self.pt8_checkbox.bind('<Button-1>', self.__update_pt8_checked)

    def _build_pt9(self):
        self.pt9_label, self.pt9_remove, self.pt9_checkbox = self._build_ptn(8, self.pt9_checkbox_value)
        self.pt9_checkbox.deselect()
        self.pt9_checkbox.bind('<Button-1>', self.__update_pt9_checked)

    def _build_pt10(self):
        self.pt10_label, self.pt10_remove, self.pt10_checkbox = self._build_ptn(9, self.pt10_checkbox_value)
        self.pt10_checkbox.deselect()
        self.pt10_checkbox.bind('<Button-1>', self.__update_pt10_checked)

    # ----------------------------------------------- BUILDERS (MISC) -----------------------------------------------

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Original Image', command=self.__info, width=12)
        self.info_label.grid(columnspan=2, row=0, column=0, padx=(15, 0), pady=5)

    def _build_gs_dropdown(self):
        self.gs_var.set(self.gs_choices[0])
        self.gs_dropdown = OptionMenu(self.root, self.gs_var, *self.gs_choices, command=self.__update_gs)
        self.gs_dropdown.configure(highlightthickness=0, width=1, anchor='w', padx=15)
        self.gs_dropdown.grid(column=2, row=0, columnspan=1)

    def _build_mask_to_csv_button(self):
        self.mask_to_csv_button = make_button(self.root, text='Save bin. mask', width=8, command=self.__mask_to_csv,
                                              row=14, column=4, columnspan=3, inner_pady=5, outer_padx=5, outer_pady = 10)

    def _build_save(self):
        self.save_label = make_label(self.root, "Save", row=13, column=0, outer_padx=(12, 0),
                                     outer_pady=(10, 15), inner_padx=10, inner_pady=5, rowspan = 2)
        self.save_checkbox = make_checkbox(self.root, text="", row=13, column=0, var=self.save_checkbox_value_iv,
                                           sticky=NE, inner_padx=0, inner_pady=0, outer_pady=(10, 15),
                                           outer_padx=(54, 0))
        self.save_checkbox.deselect()
        self.save_checkbox.bind('<Button-1>', self.__update_save_with_scale_check_status)
        
    def _build_segm(self):
        self.segm_label = make_label(self.root, "segm", row=1, column=0, outer_padx=(12, 0),
                                     outer_pady=(10, 15), inner_padx=10, inner_pady=5, rowspan = 1)
        self.segm_checkbox = make_checkbox(self.root, text="", row=1, column=0, var=self.segm_checkbox_value,
                                           sticky=NE, inner_padx=0, inner_pady=0, outer_pady=(10, 15),
                                           outer_padx=(54, 0))
        self.segm_checkbox.deselect()
        self.segm_checkbox.bind('<Button-1>', self.__update_segm_check_status)
        
    def _build_recr(self):
        self.recr_label = make_label(self.root, "recr", row=1, column=1, outer_padx=(12, 0),
                                     outer_pady=(10, 15), inner_padx=10, inner_pady=5, rowspan = 1)
        self.recr_checkbox = make_checkbox(self.root, text="", row=1, column=1, var=self.recr_checkbox_value,
                                           sticky=NE, inner_padx=0, inner_pady=0, outer_pady=(10, 15),
                                           outer_padx=(54, 0))
        self.recr_checkbox.deselect()
        self.recr_checkbox.bind('<Button-1>', self.__update_recr_check_status)
        
    def _build_save_tif(self):
        self.save_as_tif_label = make_button(self.root, "Save as Tif", row=1, column=9, outer_padx=(5, 5),
                                     outer_pady=(5, 5), inner_padx=10, inner_pady=5, rowspan = 1, columnspan=2, command = lambda: self.__save_tif(True))
        self.save_as_tif_checkbox = make_checkbox(self.root, text="", row=1, column=9, var=self.save_as_tif_checkbox_value,
                                           sticky=NE, inner_padx=0, inner_pady=0, outer_pady=(5, 5),
                                           outer_padx=(5, 5), columnspan=2)
        self.save_as_tif_checkbox.deselect()
        self.save_as_tif_checkbox.bind('<Button-1>', self.__update_save_tif_checkbox_status)

    def _build_upload_bin_mask_button(self):
        self.bin_mask_button = make_button(self.root, text='Upload bin. mask', width=13,
                                           command=lambda: self.__upload_mask(binary=True), row=14, column=1,
                                           columnspan=3, inner_pady=5, outer_padx=5, outer_pady = 10)

    def _build_upload_mask_button(self):
        self.upload_mask_button = make_button(self.root, text='Upload coords', width=9,
                                              command=lambda: self.__upload_mask(binary=False),
                                              row=13, column=1, columnspan=3, inner_pady=5, outer_padx=0,
                                              outer_pady=0)

    def _build_instant_save_button(self):
        self.instant_save_button = make_button(self.root, text='Save coords', width=9, command=self.__save_coords,
                                               row=13, column=4, columnspan=3, inner_pady=5, outer_padx=5,
                                               outer_pady=0)

    def _build_edit_coords_button(self):
        self.input_coords_button = make_button(self.root, text='Edit coords', width=9, command=self.__input_coords,
                                               row=13, column=7, columnspan=1, inner_pady=5, outer_padx=5,
                                               outer_pady=0, rowspan=2)

    def _build_use_mask_button(self):
        self.use_mask_button = make_button(self.root, text='Use mask', width=9, command=self.__use_coords, row=13,
                                           column=8, columnspan=3, inner_pady=5, outer_padx=5,
                                           outer_pady=0, rowspan=2)
    
    def _build_tif_save_path_text(self, text = ""):
                self.tif_save_path_text =  make_text(self.root, content="Tif-Name: " + text, bg=tkcolour_from_rgb(BACKGROUND), column=3, row=0,
                                    width=65, columnspan=8, pady = (5,5), padx=(5,5))
                self.tif_save_path_text.configure(font=("Courier", 7, "italic"))
        
    def _build_tif_save_path_input(self):
        self.tif_save_path_input = make_entry(self.root, row=1, column=3, width=25, pady=(5, 5), padx=(5, 5), columnspan=6)
        self.tif_save_path_input.bind('<Return>', self._update_tif_save_path_ext)
        
    def _build_autonames_button(self):
        self.autonames_button = make_button(self.root, text='Auto', width=3, command=self.__switch_autoname,
                                               row=1, column=8, columnspan=1, inner_pady=0, outer_padx=5,
                                               outer_pady=5, rowspan=1)

    # ---------------------------------------------- BUILDERS (IMAGE) -----------------------------------------------

    def _build_original_image(self, data):
        
        if data is None:
            # Placeholder
            self.original_image = make_label(self.root, "original image placeholder", row=3, column=0, rowspan=10,
                                             columnspan=7, inner_pady=80, inner_padx=120, outer_padx=(15, 10),
                                             outer_pady=(15, 10))
        else:
            print(data.shape)
            if self.gs:
                data = np.asarray(rgb_image_to_hsi_array(self.original_image_data)).reshape((480, 640))
            logging.debug("BUILDING ORIGINAL COLOUR IMAGE...")
            (self.original_image_graph, self.original_image, self.image_array) = \
                make_image(self.root, data, row=3, column=0, columnspan=7, rowspan=10, lower_scale_value=None,
                           upper_scale_value=None, color_rgb=BACKGROUND, original=True, figheight=2.5, figwidth=3.5,
                           gs=self.gs)
            self.original_image.get_tk_widget().bind('<Button-2>', self.__pop_up_image)
            self.original_image.get_tk_widget().bind('<Button-1>', self.__get_coords)
            self.original_image.get_tk_widget().bind('<Key-q>', self.__get_coords)
            self.original_image.get_tk_widget().bind('<Key-r>', self.__get_coords)
            self.original_image.get_tk_widget().bind('<Key-w>', self.__zoom)
            self.original_image.get_tk_widget().bind('<+>', self.__zoom)
            self.original_image.get_tk_widget().bind('<Key-s>', self.__dezoom)
            self.original_image.get_tk_widget().bind('<Key-d>', self.__dezoom)
            self.original_image.get_tk_widget().bind('<Key-minus>', self.__dezoom)
            self.original_image.get_tk_widget().bind('<Leave>', self.__reset_mouse_position)
            self.original_image.get_tk_widget().bind('<Motion>', self.__update_mouse_position)
            if self.pop_up:
                self.pop_up_graph = self.original_image_graph
                self.pop_up_graph.set_size_inches(8, 8)
                self.pop_up_image = FigureCanvasTkAgg(self.pop_up_graph, master=self.pop_up_window)
                self.pop_up_image.draw()
                self.pop_up_image.get_tk_widget().grid(column=0, row=0)
                self.pop_up_image.get_tk_widget().bind('<Button-1>', self.__get_coords)
                self.pop_up_image.get_tk_widget().bind('<Key-q>', self.__get_coords)
                self.pop_up_image.get_tk_widget().bind('<Key-w>', self.__zoom)
                self.pop_up_image.get_tk_widget().bind('<+>', self.__zoom)
                self.pop_up_image.get_tk_widget().bind('<Key-s>', self.__dezoom)
                self.pop_up_image.get_tk_widget().bind('<Key-d>', self.__dezoom)
                self.pop_up_image.get_tk_widget().bind('<Key-minus>', self.__dezoom)
                self.pop_up_image.get_tk_widget().bind('<Leave>', self.__reset_mouse_position)
                self.pop_up_image.get_tk_widget().bind('<Motion>', self.__update_mouse_position_pop_up)
            
    def _update_tif_save_path(self, event = None):
        path = os.path.dirname(self.listener.current_rendered_result_path)
        self.tif_save_path_stem = path + '/' + self.listener.output_folder_hypergui +"/"
        if self.tif_save_path_end is None or self.automatic_names:
            self.tif_save_path_end = os.path.basename(path) + '_mask' + self.listener.output_folder_hypergui
        self.tif_save_path_input.delete(0,"end")
        self.tif_save_path_input.insert(0, self.tif_save_path_end)
        self.tif_save_path = self.tif_save_path_stem + self.tif_save_path_end + ".tif"
        self._build_tif_save_path_text(text  = self.tif_save_path_end)
            
    def _update_tif_save_path_ext(self, event = None):
        self.automatic_names = False
        path = os.path.dirname(self.listener.current_rendered_result_path)
        self.tif_save_path_stem = path + '/' + self.listener.output_folder_hypergui +"/"
        self.tif_save_path_end = self.tif_save_path_input.get()
        self.tif_save_path_input.delete(0,"end")
        self.tif_save_path_input.insert(0, self.tif_save_path_end)
        self.tif_save_path = self.tif_save_path_stem + self.tif_save_path_end + ".tif"
        self._build_tif_save_path_text(text = self.tif_save_path_end)      

    # --------------------------------------------------- DRAWING -----------------------------------------------------

    def _draw_points(self):
        if self.original_image_data is not None:
            copy_data = self.original_image_data.copy()
            not_none = [i for i in self.coords_list if i != (None, None) ]
            for point in not_none:
                y = int(point[0])
                x = int(point[1])
                for xi in range(-4, 5):
                    copy_data[(x + xi) % 480, y, :3] = BRIGHT_GREEN_RGB
                for yi in range(-4, 5):
                    copy_data[x, (y + yi) % 640, :3] = BRIGHT_GREEN_RGB
                idx = not_none.index(point)
                self._draw_a_line(not_none[idx - 1], not_none[idx], copy_data)
               
            left = self.view_mid[1] - 320
            bottom = self.view_mid[0] - 240
            right = left + 640
            top = bottom + 480
            print(copy_data.shape)
            im = Image.fromarray(copy_data.astype(np.uint8))
            im = im.resize((640*self.zoom_factor, 480*self.zoom_factor)) 
            im = im.crop((left, bottom, right, top))
            self._build_original_image(np.array(im))
            if len(not_none)>=1:
                pt1 = not_none[-1]
                pt2 = not_none[-2]
                a = pt1[0]-pt2[0]
                b = pt1[1]-pt2[1]
                c = np.sqrt(a*a + b*b)
            self.original_image.get_tk_widget().focus_force()

    @staticmethod
    def _draw_a_line(point1, point2, image):
        r0, c0 = point1
        r1, c1 = point2
        rr, cc, val = line_aa(c0, r0, c1, r1)
        for i in range(len(rr)):
            image[rr[i] % 480, cc[i] % 640] = (int(113 * val[i]), int(255 * val[i]), int(66 * val[i]))
        return image

    # --------------------------------------------------- CALLBACKS ---------------------------------------------------

    def __info(self):
        info = self.listener.modules[INFO].original_info
        title = "Original Image Information"
        make_info(title=title, info=info)

    # ------------------------------------------------------ MASK -----------------------------------------------------

    def __upload_mask(self, binary):
        mask_dir_path = filedialog.askopenfilename(parent=self.root, title="Please select a .csv file "
                                                                           "containing either a binary mask or the "
                                                                           "x and y coordinates of a mask.")
        if mask_dir_path[-4:] != ".csv":
            messagebox.showerror("Error", "That's not a .csv file!")

        if binary:
            self.__load_binary_mask(mask_dir_path)
        else:
            self.__load_mask(mask_dir_path)

    def __load_binary_mask(self, mask_path):
        self.coords_list = [(None, None) for ii in range(1000000)]
        self._build_points()
        self._draw_points()

        if self.listener.is_masked:
            self.listener.modules[ORIGINAL_COLOUR_DATA].empty_stats()
            self.listener.modules[NEW_COLOUR_DATA].empty_stats()
            self.listener.modules[RECREATED_COLOUR_DATA].empty_stats()
        self.mask_raw = np.genfromtxt(mask_path, delimiter=',')
        self.mask_raw = np.fliplr(self.mask_raw.T)
        self.listener.submit_mask(np.logical_not(self.mask_raw))

    def __load_mask(self, path):
        coords = []
        with open(path) as csvfile:
            read_csv = csv.reader(csvfile, delimiter=',')
            for row in read_csv:
                coords.append(((int(float(row[0]) - 1)), (int(float(row[1]) - 1))))
            csvfile.close()
        for i in range(1000000 - len(coords)):
            coords.append((None, None))
        self.coords_list = coords
        self._build_points()
        self._draw_points()
        self.__use_coords()

    def __use_coords(self):
        # produces a 640x480 8-bit mask
        if self.listener.is_masked:
            self.listener.modules[ORIGINAL_COLOUR_DATA].empty_stats()
            self.listener.modules[NEW_COLOUR_DATA].empty_stats()
            self.listener.modules[RECREATED_COLOUR_DATA].empty_stats()
        polygon = [point for point in self.coords_list if point != (None, None)]
        img = Image.new('L', (640, 480), 0)
        ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)
        self.mask_raw = np.array(img)
        self.mask_raw = np.fliplr(self.mask_raw.T)
        self.listener.submit_mask(np.logical_not(self.mask_raw))

    def __mask_to_csv(self):
        polygon = [point for point in self.coords_list if point != (None, None)]
        img = Image.new('L', (640, 480), 0)
        ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)
        mask_array = np.array(img)
        path = os.path.dirname(self.listener.current_rendered_result_path)
        if not os.path.exists(path + '/'+self.listener.output_folder_hypergui):
            os.mkdir(path + '/'+self.listener.output_folder_hypergui +"/")
        output_path = path + '/' + self.listener.output_folder_hypergui +"/mask" + '.csv'
        if os.path.exists(output_path):
            yn = messagebox.askquestion ('Verify','Are you sure you want to override mask.csv?',icon = 'warning')
            if yn == "yes":
                np.savetxt(output_path, mask_array, delimiter=",", fmt="%d")
        else:
            np.savetxt(output_path, mask_array, delimiter=",", fmt="%d")
        self.__save_tif()
        
    def __update_save_tif_checkbox_status(self, event):
        self.save_tif_bool = not self.save_tif_bool
        self.listener.update_saved(TIF, self.save_tif_bool)
        

    # --------------------------------------------- ADDING/REMOVING COORDS --------------------------------------------

    def __save_coords(self):
        path = os.path.dirname(self.listener.current_rendered_result_path)
        output_path = path + '/' + self.listener.output_folder_hypergui +"/MASK_COORDINATES" + '.csv'
        if os.path.exists(output_path):
            yn = messagebox.askquestion ('Verify','Are you sure you want to override MASK_COORDINATES.csv?',icon = 'warning')
            if yn == "yes":
                self.listener.instant_save_points()
        else:
            self.listener.instant_save_points()
        self.__save_tif()
            
    def __save_tif(self, from_button=False):
        self._update_tif_save_path()
        if self.save_tif_bool or from_button:
            polygon = [point for point in self.coords_list if point != (None, None)]
            if len(polygon) >= 2:
                img = Image.new('L', (640, 480), 0)
                ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)
                if not os.path.exists(self.tif_save_path_stem):
                    os.mkdir(self.tif_save_path_stem)
                output_path = self.tif_save_path
                mask_img = Image.fromarray(((np.array(img)*-1+1)*255).astype("uint8"), 'L')
                mask_img.save(output_path)
            else:
                print("Draw a mask to save TIF.")
        

    def __get_coords(self, event):
        
            #x = int((eventorigin.x - 30) * 640 / 296)
            #y = int((eventorigin.y - 18) * 480 / 221)
            #if 0 <= x < 640 and 0 <= y < 480:
            #    self.__add_pt((x, y))
        if not self.pop_up:
            pos = self.original_image_graph.axes[0].get_position()
        else:
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
            self.__add_pt((Xc, Yc))

    def __remove_pt(self, index):
        if index == 'all':
            self.coords_list = [(None, None) for _ in range(1000000)]
        elif index == 'last':
            counter = 0
            for element in self.coords_list:
                if element[0] is not None:
                    last_index = counter
                counter = counter + 1
            self.coords_list[last_index] = (None, None)
        else:
            self.coords_list[index - 1] = (None, None)
        self._build_points()
        self._draw_points()

    def __add_pt(self, pt):
        if self.coords_list.count((None, None)) != 0:
            index = self.coords_list.index((None, None))
            self.coords_list[index] = pt
            self._build_points()
            self._draw_points()
            self.__input_coord_n(index)
            
    def __remove_pt_n(self, index):
        if index == 'all':
            self.coords_list = [(None, None) for _ in range(1000000)]   
            for ii in range(1000):
                self.__input_coord_n(ii)
            self._build_points()
            self._draw_points()
        else:
            self.coords_list[index - 1] = (None, None)     
            self.__input_coord_n(index - 1)
            self._build_points()
            self._draw_points()
            
    def __reset_mouse_position(self, event):
        self.mouse_x = 320
        self.mouse_y = 240
        
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
        self.original_image.get_tk_widget().focus_force()
        
        
    def __update_mouse_position_pop_up(self, event):
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
        self.pop_up_image.get_tk_widget().focus_force()
        

    # ----------------------------------------------- UPDATERS (IMAGE) ------------------------------------------------

    def __update_to_rgb(self):
        self.rgb_button.config(foreground="red")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.displayed_image_mode = RGB
        self.listener.broadcast_to_original_image()

    def __update_to_sto2(self):
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="red")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.displayed_image_mode = STO2
        self.listener.broadcast_to_original_image()

    def __update_to_nir(self):
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="red")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.displayed_image_mode = NIR
        self.listener.broadcast_to_original_image()

    def __update_to_thi(self):
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="red")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.displayed_image_mode = THI
        self.listener.broadcast_to_original_image()

    def __update_to_twi(self):
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="red")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.displayed_image_mode = TWI
        self.listener.broadcast_to_original_image()

    def __update_to_tli(self):
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="red")
        self.ohi_button.config(foreground="black")
        self.displayed_image_mode = TLI
        self.listener.broadcast_to_original_image()

    def __update_to_ohi(self):
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="red")
        self.displayed_image_mode = OHI
        self.listener.broadcast_to_original_image()

    def __update_gs(self, event):
        if self.gs_var.get()[:2] == 'CS':
            self.gs = False
            self.update_original_image(self.original_image_data)
        elif self.gs_var.get()[:2] == 'GS':
            self.gs = True
            self.update_original_image(self.original_image_data)

    # ---------------------------------------------- UPDATERS (SAVING) ------------------------------------------------

    def __update_rgb_check_status(self, event):
        self.rgb_checkbox_value = not self.rgb_checkbox_value
        self.listener.update_saved(OG_RGB_DATA, self.rgb_checkbox_value)

    def __update_sto2_check_status(self, event):
        self.sto2_checkbox_value = not self.sto2_checkbox_value
        self.listener.update_saved(OG_STO2_DATA, self.sto2_checkbox_value)

    def __update_nir_check_status(self, event):
        self.nir_checkbox_value = not self.nir_checkbox_value
        self.listener.update_saved(OG_NIR_DATA, self.nir_checkbox_value)

    def __update_twi_check_status(self, event):
        self.twi_checkbox_value = not self.twi_checkbox_value
        self.listener.update_saved(OG_TWI_DATA, self.twi_checkbox_value)
        
    def __update_tli_check_status(self, event):
        self.tli_checkbox_value = not self.tli_checkbox_value
        self.listener.update_saved(OG_TLI_DATA, self.tli_checkbox_value)

    def __update_thi_check_status(self, event):
        self.thi_checkbox_value = not self.thi_checkbox_value
        self.listener.update_saved(OG_THI_DATA, self.thi_checkbox_value)
    
    def __update_ohi_check_status(self, event):
        self.ohi_checkbox_value = not self.ohi_checkbox_value
        self.listener.update_saved(OG_OHI_DATA, self.ohi_checkbox_value)

    def __update_save_with_scale_check_status(self, event):
        self.save_checkbox_value = not self.save_checkbox_value
        self.listener.update_saved(OG_IMAGE, self.save_checkbox_value)

    # ---------------------------------------------- UPDATERS (POINTS) ------------------------------------------------

    def __update_all(self, value):
        for point in [PT1, PT2, PT3, PT4, PT5, PT6, PT7, PT8, PT9, PT10]:
            self.listener.update_saved(point, value)

    def __update_all_points_checked(self, event):
        value = not bool(self.all_points_checkbox_value.get())
        if value:
            self.pt1_checkbox.select()
            self.pt2_checkbox.select()
            self.pt3_checkbox.select()
            self.pt4_checkbox.select()
            self.pt5_checkbox.select()
            self.pt6_checkbox.select()
            self.pt7_checkbox.select()
            self.pt8_checkbox.select()
            self.pt9_checkbox.select()
            self.pt10_checkbox.select()
        else:
            self.pt1_checkbox.deselect()
            self.pt2_checkbox.deselect()
            self.pt3_checkbox.deselect()
            self.pt4_checkbox.deselect()
            self.pt5_checkbox.deselect()
            self.pt6_checkbox.deselect()
            self.pt7_checkbox.deselect()
            self.pt8_checkbox.deselect()
            self.pt9_checkbox.deselect()
            self.pt10_checkbox.deselect()
        self.__update_all(value)

    def __update_pt1_checked(self, event):
        value = self.get_pt1_checkbox_value()
        self.listener.update_saved(PT1, value)

    def __update_pt2_checked(self, event):
        value = self.get_pt2_checkbox_value()
        self.listener.update_saved(PT2, value)

    def __update_pt3_checked(self, event):
        value = self.get_pt3_checkbox_value()
        self.listener.update_saved(PT3, value)

    def __update_pt4_checked(self, event):
        value = self.get_pt4_checkbox_value()
        self.listener.update_saved(PT4, value)

    def __update_pt5_checked(self, event):
        value = self.get_pt5_checkbox_value()
        self.listener.update_saved(PT5, value)

    def __update_pt6_checked(self, event):
        value = self.get_pt6_checkbox_value()
        self.listener.update_saved(PT6, value)

    def __update_pt7_checked(self, event):
        value = self.get_pt7_checkbox_value()
        self.listener.update_saved(PT7, value)

    def __update_pt8_checked(self, event):
        value = self.get_pt8_checkbox_value()
        self.listener.update_saved(PT8, value)

    def __update_pt9_checked(self, event):
        value = self.get_pt9_checkbox_value()
        self.listener.update_saved(PT9, value)

    def __update_pt10_checked(self, event):
        value = self.get_pt10_checkbox_value()
        self.listener.update_saved(PT10, value)

    # ------------------------------------------------- IMAGE POP-UP --------------------------------------------------

    def __pop_up_image(self, event):
        (self.pop_up_window, self.pop_up_image) = make_popup_image(self.original_image_graph, interactive=True)
        self.pop_up = True
        self.pop_up_image.get_tk_widget().bind('<Button-1>', self.__get_coords)
        self.pop_up_image.get_tk_widget().bind('<Key-w>', self.__zoom)
        self.pop_up_image.get_tk_widget().bind('<+>', self.__zoom)
        self.pop_up_image.get_tk_widget().bind('<Key-s>', self.__dezoom)
        self.pop_up_image.get_tk_widget().bind('<Key-d>', self.__dezoom)
        self.pop_up_image.get_tk_widget().bind('<Key-minus>', self.__dezoom)
        self.pop_up_image.get_tk_widget().bind('<Leave>', self.__reset_mouse_position)
        self.pop_up_image.get_tk_widget().bind('<Motion>', self.__update_mouse_position)
        self.pop_up_window.protocol("WM_DELETE_WINDOW", func=self.__close_pop_up)
        self.pop_up_window.attributes("-topmost", True)
        
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

    def __close_pop_up(self):
        self.pop_up = False
        self.pop_up_window.destroy()
        self._draw_points()

    # ------------------------------------------------- INPUT POP-UP --------------------------------------------------

    def __input_info(self):
        info = self.listener.modules[INFO].input_info
        title = "Coordinate Input Information"
        make_info(title=title, info=info)

    def __input_coord_n(self, num):
        rom = num % 200
        col = math.floor(num/200)*6
        title = make_text(self.coords_window, content="Pt " + str(num) + ': ', bg=tkcolour_from_rgb(BACKGROUND),
                          column=col+0, row=rom + 1, width=6, pady=(0, 3), padx=(15, 0))
        title_x = make_text(self.coords_window, content="x = ", bg=tkcolour_from_rgb(BACKGROUND), column=col+1, row=rom + 1,
                            width=4, pady=(0, 3))
        title_y = make_text(self.coords_window, content="y = ", bg=tkcolour_from_rgb(BACKGROUND), column=col+3, row=rom + 1,
                            width=4, pady=(0, 3), padx=(5, 0))
        input_x = make_entry(self.coords_window, row=rom + 1, column=col+2, width=5, columnspan=1, pady=(0, 3))
        input_y = make_entry(self.coords_window, row=rom + 1, column=col+4, width=5, columnspan=1, padx=(0, 15),
                             pady=(0, 3))
        if self.coords_list[num] != (None, None):
            input_x.insert(END, str(self.coords_list[num][0] + 1))
            input_y.insert(END, str(self.coords_list[num][1] + 1))
            
        remove = make_button(self.coords_window, text='x', width=1, command=lambda: self.__remove_pt_n(num + 1), row=rom +1,
                         column=col+5, highlightthickness=0)
        return title, title_x, title_y, input_x, input_y

    def __input_coords(self):
        self.coords_window_frame = Toplevel()
        self.coords_window_frame.geometry("+0+0")
        self.coords_window_frame.configure(bg=tkcolour_from_rgb(BACKGROUND))
        
        self.frame_canvas = Frame(self.coords_window_frame)
        self.frame_canvas.grid(row=2, column=11, columnspan = 2, pady=(5, 0), sticky='nw', rowspan = 250)
        self.frame_canvas.grid_propagate(False)
        self.canvas = Canvas(self.frame_canvas, bg="yellow")
        self.canvas.grid(row=0, column=1, sticky="news")
        vsb = Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        vsb.grid(row=0, column=0, rowspan=5, sticky='ns')
        
        self.canvas.configure(yscrollcommand=vsb.set)
        self.coords_window = Frame(self.canvas, bg="blue")
        self.canvas.create_window((0, 0), window=self.coords_window, anchor='nw')
        


        # title
        self.input_points_title = make_label_button(self.coords_window, text='Coordinate Input',
                                                    command=self.__input_info, width=14)
        self.input_points_title.grid(columnspan=3)

        # points
        for ii in range(1000):
            self.input_pt_title_list[ii], self.input_pt_title_x_list[ii], self.input_pt_title_y_list[ii], self.input_pt_x_list[ii], self.input_pt_y_list[ii] = \
                self.__input_coord_n(ii)

        # go button
        self.go_button = make_button(self.coords_window, text='Go', width=2, command=self.__use_inputted_coords, row=201,
                                     column=3, columnspan=5, inner_pady=5, outer_padx=(15, 15), outer_pady=(7, 15))
        self.all_remove = make_button(self.coords_window, text='x', width=1, command=lambda: self.__remove_pt_n('all'),
                                         row=0, column=5, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10,
                                         highlightthickness=0)
        self.coords_window.update_idletasks()
        self.frame_canvas.config(width=1350,
                            height=900)
        self.canvas.config(width=1300,
                            height=900)
        
        
        # Set the canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def __use_inputted_coords(self):
        coords = []
        for ii in range(1000):
            coords.append([self.input_pt_x_list[ii].get(), self.input_pt_y_list[ii].get()])
        coords = [(int(i[0]) - 1, int(i[1]) - 1) for i in coords if i[0] != '' and i[1] != '']
        if len(coords) > 0:
            xs = [i[0] for i in coords]
            ys = [i[1] for i in coords]
            if min(xs) >= 0 and max(xs) < 640 and min(ys) >= 0 and max(ys) < 480:
                coords = coords + [(None,None) for ii in range(1000-len(coords))]
                self.coords_list = coords +self.coords_list[1000::]
                self._build_points()
                self._draw_points()
            else:
                messagebox.showerror("Error", "x values must be on the interval [1, 640] and y values must be on the "
                                              "interval \n[1, 480].")
        self.coords_window_frame.destroy()
        
    def __switch_autoname(self):
        self.automatic_names=True
        self._update_tif_save_path()
    
    def __update_segm_check_status(self, event = None):
        self.segm = not self.segm
        self.listener.update_segm(self.segm)
        self.listener.broadcast_to_original_image()
    
    def __update_recr_check_status(self, event = None):
        self.recr = not self.recr
        self.listener.update_recr(self.recr)
        self.listener.broadcast_to_original_image()
        
    def __to_front(self, event = None):
        self.original_image.get_tk_widget().focus_force()