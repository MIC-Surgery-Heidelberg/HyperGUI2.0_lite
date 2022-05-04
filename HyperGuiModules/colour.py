from HyperGuiModules.utility import *
from matplotlib.pyplot import cm
import matplotlib
matplotlib.use("TkAgg")


class Colour:
    def __init__(self, colour_frame, listener):
        self.root = colour_frame

        # Listener
        self.listener = listener

        self.greybar = None
        self.colourbar = None
        self.high_low = None

        self.info_label = None

        self._init_widget()

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widget(self):
        self._build_greybar()
        self._build_colourbar()
        self._build_info_label()
        self._build_high_low()

    # --------------------------------------------------- BUILDERS ---------------------------------------------------

    def _build_greybar(self):
        colour_fig = Figure(figsize=(2, 0.25))
        axes = colour_fig.add_subplot(111)

        cmap = cm.get_cmap('gray')
        self.greybar = cmap(np.arange(cmap.N))

        axes.imshow([self.greybar], extent=[0, 500, 0, 55])
        axes.get_yaxis().set_visible(False)
        axes.get_xaxis().set_visible(False)

        colour_fig.patch.set_facecolor(rgb_to_rgba(BACKGROUND))
        colour_fig.set_tight_layout('True')
        image = FigureCanvasTkAgg(colour_fig, master=self.root)
        image.draw()
        image.get_tk_widget().grid(column=0, row=1, padx=0, pady=0)

    def _build_colourbar(self):
        colour_fig = Figure(figsize=(2, 0.25))
        axes = colour_fig.add_subplot(111)
        #scale = np.loadtxt('scale.txt', delimiter = ",")
        #c_scale = [list(li/255)[0:3] for li in scale]
        #c_scale.reverse()
        #color_scale = matplotlib.colors.ListedColormap(c_scale)
        #cmap = color_scale
        #cmap = cm.get_cmap('jet')
        
        R1 = np.linspace(0,0,20)
        B1 = np.linspace(0,0,20)
        G1 = np.linspace(100/256,255/256,20) 
        R2 = np.linspace(0,0,20)
        B2 = np.linspace(0,255/256,20)
        G2 = np.linspace(255/256,0,20) 
        R3 = np.linspace(0,255/256,20)
        B3 = np.linspace(255/256,255/256,20)
        G3 = np.linspace(0,0,20) 
        R4 = np.linspace(255/256,255/256,20)
        B4 = np.linspace(255/256,0,20)
        G4 = np.linspace(0,0,20) 
        R5 = np.linspace(255/256,100/256,20)
        B5 = np.linspace(0,0,20)
        G5 = np.linspace(0,0,20) 
        R = np.hstack([R1, R2, R3, R4, R5])
        B = np.hstack([B1, B2, B3, B4, B5])
        G = np.hstack([G1, G2, G3, G4, G5])
        colors = [(R[idx], B[idx], G[idx]) for idx in range(100)]
        n_bin = 100  # Discretizes the interpolation into bins
        cmap_name = 'my_list'
        color_scale = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)
        cmap = color_scale

        self.colourbar = cmap(np.arange(cmap.N))

        axes.imshow([self.colourbar], extent=[0, 500, 0, 55])
        axes.get_yaxis().set_visible(False)
        axes.get_xaxis().set_visible(False)

        colour_fig.patch.set_facecolor(rgb_to_rgba(BACKGROUND))
        colour_fig.set_tight_layout('True')
        image = FigureCanvasTkAgg(colour_fig, master=self.root)
        image.draw()
        image.get_tk_widget().grid(column=0, row=2, padx=0, pady=0)

    def _build_high_low(self):
        self.high_low = make_text(self.root, content="Low               High", bg=tkcolour_from_rgb(BACKGROUND),
                                  column=0, row=3, width=22, columnspan=1, padx=(23, 15), pady=(0, 15))

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Colour Scale', command=self.__info, width=11)
        self.info_label.grid(pady=(15, 10), padx=(0, 60))

    # -------------------------------------------------- CALLBACKS ---------------------------------------------------

    def __info(self):
        info = self.listener.modules[INFO].colour_info
        title = "Colour Information"
        make_info(title=title, info=info)
