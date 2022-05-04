from HyperGuiModules.utility import *
import numpy as np
from tkinter import filedialog, messagebox
import os
import glob


class SourceAndOutput:
    def __init__(self, source_and_output_frame, listener):
        # Root
        self.root = source_and_output_frame

        # Listener
        self.listener = listener

        # GUI
        self.select_data_cube_button = None
        self.select_output_dir_button = None
        self.render_data_cube_button = None
        self.change_hypergui_folder_version_number_editText = None
        self.selection_listbox = None
        self.data_cube_path_label = None
        self.output_dir_label = None
        self.delete_button = None
        self.sub_dir = ""
        self.info_label = None

        # Data
        self.data_cubes = []
        self.data_cube_paths = []
        self.data_cube_path_label = None
        self.path_label = None
        self.live = False
        self.sub_dirs = []
        self.sub_dir_list = []

        # Widget Initialization
        self._init_widgets()

    # ---------------------------------------------------- GETTERS ---------------------------------------------------

    def get_selected_data_cube_path(self):
        index = self.selection_listbox.curselection()[0]
        return self.data_cube_paths[index]

    def get_selected_data_paths(self):
        selection = self.selection_listbox.curselection()
        selected_data_paths = [self.data_cube_paths[i] for i in selection]
        return selected_data_paths

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widgets(self):
        self._build_select_dir_button()
        self._build_select_superdir_button()
        self._build_render_button()
        self._build_selection_box()
        self._build_delete_button()
        self._build_info_label()
        self._build_change_hypergui_folder_version_number_editText()
        self._build_live_button()

    # --------------------------------------------------- BUILDERS ---------------------------------------------------


    def _build_live_button(self):
        self.live_button = make_button(self.root, text='Live', width=5, command=self.__update_live_checkbox,
                                               row=0, column=1, columnspan=1, inner_pady=5, outer_padx=5,
                                               outer_pady=5, rowspan=1)
        self.live_button["bg"] = "white"
        
    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Source and Output', command=self.__info, width=15)

    def _build_select_dir_button(self):
        self.select_data_cube_button = make_button(self.root, text="Select Data\nDirectory",
                                                   command=self.__add_data_cube_dir, inner_padx=10, inner_pady=10,
                                                   outer_padx=15, row=1, column=0, width=11, outer_pady=(0, 5))

    def _build_select_superdir_button(self):
        self.select_data_cube_button = make_button(self.root, text="Select Data\nSuperdirectory",
                                                   command=self.__add_data_cube_dirs, inner_padx=10, inner_pady=10,
                                                   outer_padx=15, row=2, column=0, width=11, outer_pady=(0, 5))

    def _build_delete_button(self):
        self.delete_button = make_button(self.root, text="Remove Data\nCube", command=self.__delete_selected_data_cube,
                                         inner_padx=10, inner_pady=10, outer_padx=15, row=3, column=0, width=11,
                                         outer_pady=(0, 5))

    def _build_render_button(self):
        self.render_data_cube_button = make_button(self.root, text="Render Data\nCube",
                                                   command=self.__render_cube, inner_padx=10, inner_pady=10,
                                                   outer_padx=15, row=4, column=0, width=11, outer_pady=(0, 15))

    def _build_selection_box(self):
        self.selection_listbox = make_listbox(self.root, row=1, column=1, rowspan=4, padx=(0, 15), pady=(0, 15), width =32)
        self.selection_listbox.bind('<<ListboxSelect>>', self.__update_selected_data_cube)
        
    def _build_change_hypergui_folder_version_number_editText(self):
        self.change_hypergui_folder_version_number_text = make_text(self.root, content="Output: " + self.listener.output_folder_hypergui, bg=tkcolour_from_rgb(BACKGROUND), column=0, row=5,
                                    width=35, columnspan=2, padx=(5, 5), pady=(5, 5))
        self.hypergui_folder_version_number_editText = make_entry(self.root, row=6, column=0, width=35, columnspan=2, padx=(5, 5), pady=(5, 5))
        self.hypergui_folder_version_number_editText.bind('<Return>', self.__update_hypergui_folder_version_number)
        self.hypergui_folder_version_number_editText.insert(END, self.listener.output_folder_hypergui[10::])


    # -------------------------------------------------- CALLBACKS ---------------------------------------------------

    def __info(self):
        info = self.listener.modules[INFO].source_output_info
        title = "Source & Output Information"
        make_info(title=title, info=info)
    
    def __update_hypergui_folder_version_number(self, event):
        print("__update_hypergui_folder_version_number")
        vn = self.hypergui_folder_version_number_editText.get()
        self.listener.set_output_folder_hypergui(vn)
        self._build_change_hypergui_folder_version_number_editText()
        self.listener.broadcast_new_hypergui_folder_to_prediction()

    def __update_selected_data_cube(self, event):
        pass
        # dc_path = self.get_selected_data_cube_path()
        # selected_paths = self.get_selected_data_paths()
        # self.listener.set_data_cube(dc_path)
        # self.listener.update_selected_paths(selected_paths)

    def __add_data_cube_dirs(self):
        super_dir = self.__get_path_to_dir("Please select folder containing all the data folders.")
        sub_dirs = self.__get_sub_folder_paths(super_dir)
        for sub_dir in sub_dirs:
            self.__add_data_cube(sub_dir)

    def __add_data_cube_dir(self):
        dc_dir_path = self.__get_path_to_dir("Please select a folder containing data.")
        self.__add_data_cube(dc_dir_path)

    def __add_data_cube(self, sub_dir):
        contents = os.listdir(sub_dir)
        dc_path = [sub_dir + "/" + i for i in contents if "SpecCube.dat" in i]  # takes first data cube it finds
        if len(dc_path) > 0:
            dc_path = dc_path[0]
            if dc_path in self.data_cube_paths:
                messagebox.showerror("Error", "That data has already been added.")
            else:
                data_cube = self.__process_data_cube(dc_path)

                # Add the new data to current class
                self.data_cube_paths.append(dc_path)
                self.data_cubes.append(data_cube)

                # Display the data cube
                concat_path = os.path.basename(os.path.normpath(dc_path))
                self.selection_listbox.insert(END, concat_path)
                self.selection_listbox.config(width=32)

                # Add data cube to listener for analysis
                #self.listener.submit_data_cube(data_cube, dc_path)
                #display(sys.getsizeof(self.listener))

    def __delete_selected_data_cube(self):
        if self.selection_listbox.size() > 0 and self.selection_listbox.curselection():
            index = self.selection_listbox.curselection()[0]
            self.selection_listbox.delete(index)
            self.listener.delete_analysis_result(self.data_cube_paths[index])
            self.data_cube_paths.pop(index)
            self.data_cubes.pop(index)
            #display(sys.getsizeof(self.listener))

    def __get_path_to_dir(self, title):
        if self.listener.dc_path is not None:
            p = os.path.dirname(os.path.dirname(self.listener.dc_path))
            path = filedialog.askdirectory(parent=self.root, title=title, initialdir=p)
        else:
            path = filedialog.askdirectory(parent=self.root, title=title)
        return path

    def __render_cube(self):
        for i in range(self.selection_listbox.size()):
            self.selection_listbox.itemconfig(i, foreground='black')
        index = self.selection_listbox.curselection()[0]
        self.selection_listbox.itemconfig(index, foreground='red')
        dc_path = self.get_selected_data_cube_path()
        data_cube = self.__process_data_cube(dc_path)
        self.listener.submit_data_cube(data_cube, dc_path)
        selected_paths = self.get_selected_data_paths()
        self.listener.set_data_cube(dc_path)
        self.listener.update_selected_paths(selected_paths)

    @staticmethod
    def __process_data_cube(path):
        if path == '' or path is None:
            return None
        if path[-12:] != "SpecCube.dat":
            messagebox.showerror("Error", "That's not a .dat file!")
            return None
        else:
            data = np.fromfile(path, dtype='>f')  # returns 1D array and reads file in big-endian binary format
            print(data[3:].size)
            if data[3:].size == 38880000:
                data_cube = data[3:].reshape(720, 540, 100)
            else:        
                data_cube = data[3:].reshape(640, 480, 100)  # reshape to data cube and ignore first 3 values
            return data_cube

    @staticmethod
    def __get_sub_folder_paths(path_to_main_folder, recursive = False): 
        #contents = os.listdir(path_to_main_folder)
        # Adds the path to the main folder in front for traversal
        #sub_folders = [path_to_main_folder + "/" + i for i in contents if bool(re.match('[\d/-_]+$', i))]
        sub_folders = sorted(glob.glob(path_to_main_folder+"/**/*SpecCube.dat", recursive = recursive))
        sub_folders = [os.path.dirname(string) for string in sub_folders]
        sub_folders.sort(key=lambda x: os.path.basename(x))
        return sub_folders
    
    def __update_live_checkbox(self, event = None):
        self.live= not self.live
        if self.live:
            self.listener.live = True
            self.live_button["text"] = "Stop"
            self.live_button["bg"] = "red"
            self.__add_live_folder()
        else:
            self.listener.live = False
            self.live_button["text"] = "Live"
            self.live_button["bg"] = "white"
        self.__start_watchdog()
    
    def __start_watchdog(self):
        if self.live:
            self.__watchdog()
            self.root.after(1000, self.__start_watchdog)
        else:
            pass
    
    def __watchdog(self):
        super_dir = self.live_folder
        sub_dirs = self.__get_sub_folder_paths(super_dir, True)
        if not self.sub_dirs == sub_dirs:
                print("watchdog start")
                self.sub_dirs = sub_dirs 
                self.__watch_folder()
        
    def __add_live_folder(self):
        self.live_folder= self.__get_path_to_dir("Please select folder to watch.")
    
    def __trash_list(self):
        self.data_cube_paths = []
        self.selection_listbox.delete(0,'end')
    
    def __watch_folder(self):
        super_dir = self.live_folder
        if len(self.__get_sub_folder_paths(super_dir, True))>0:
            sub_dir_list = self.__get_sub_folder_paths(super_dir, True)
            sub_dir = sub_dir_list[-1]
            print(sub_dir)
            if not sub_dir_list == self.sub_dir_list:
                self.sub_dir_list = sub_dir_list
                self.__trash_list()
                for cube in self.sub_dir_list:
                    self.__add_data_cube(cube)
                self.selection_listbox.selection_clear(0, END)
                #self.selection_listbox.select_set(self.current_dc_path) 
                self.selection_listbox.select_set("end") 
                if not sub_dir == self.sub_dir:
                    self.sub_dir = sub_dir
                    self.selection_listbox.event_generate("<<ListboxSelect>>")
                    self.__render_cube()
                    print("watchdog sleep")
