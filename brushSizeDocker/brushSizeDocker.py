from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QToolButton,
    QComboBox, QSlider, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from krita import DockWidget, Krita
from math import floor
from .settingsService import *
from .settingsUI import *
from .qtExtras import *

DOCKER_NAME = 'Brush Size Docker'

class BrushSizeDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_NAME)
        self.sv = SettingsService()
        self.setting_dialog = None
        self.setUI()

    def setUI(self):
        self.widget = QWidget(self)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 15, 0, 0)  # Reduce the margins around the layout

        self.size_inputs = []
        self.size_sliders = []
        
        # used to not update the brush size when changing presets
        # TODO: change this abomination
        self.presetChange = False
        
        # dropdown
        self.preset_selector = QComboBox(self)
        self.preset_selector.addItems(self.sv.getModes())
        self.preset_selector.setCurrentIndex(self.sv.getDefaultModeInt())
        self.preset_selector.currentIndexChanged.connect(self.update_preset)

        self.button_configure =  QToolButton() 
        self.button_configure.setIcon( Krita.instance().icon("configure-shortcuts") )
        self.button_configure.clicked.connect(self.openDialog)
        
        self.top_widget = QWidget()
        self.top_layout = QHBoxLayout() 
        self.top_layout.setContentsMargins(4, 0, 4, 0)

        self.top_layout.addWidget(self.preset_selector)
        self.top_layout.addWidget(self.button_configure)

        self.top_widget.setLayout(self.top_layout)
        self.layout.addWidget(self.top_widget)

        for i in range(4):
            row_layout = QHBoxLayout()

            button = QPushButton(f"Size {i+1}", self)
            button.setFixedWidth(60)  # Set fixed width for buttons
            button.clicked.connect(lambda checked, index=i: self.set_brush_size(index))

            input_field = QLineEdit(self)
            input_field.setFixedWidth(35)  # Set fixed width for input fields
            input_field.setValidator(FloatValidator())
            self.size_inputs.append(input_field)

            slider = QSlider(Qt.Horizontal, self)
            slider.valueChanged.connect(lambda value, index=i: self.update_input_from_slider(value, index))
            self.size_sliders.append(slider)

            row_layout.addWidget(button)
            row_layout.addWidget(input_field)
            row_layout.addWidget(slider)

            self.layout.addLayout(row_layout)

        self.recalculate_button = QPushButton("Recalculate", self)
        self.recalculate_button.clicked.connect(self.update_preset)
        self.recalculate_button.setVisible(False)
        self.layout.addWidget(self.recalculate_button)

        # Spacer to push the content to the top
        self.layout.addSpacerItem(QSpacerItem(150, 300, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)

        # Set initial preset to "Medium"
        self.update_preset()

    def openDialog(self):
        if self.setting_dialog == None:
            self.setting_dialog = SettingsUI(self.sv, self)
            self.setting_dialog.show() 
        elif self.setting_dialog.isVisible() == False : 
            self.setting_dialog.show() 
            #self.setting_dialog.loadDefault()
        else:
            pass
    
    def closeDialog(self):
        self.update_preset()


    def update_preset(self):
        self.presetChange = True
        preset = self.preset_selector.currentText().lower()
        if preset == "small":
            sizes = self.sv.getSmallSizes()
            self.recalculate_button.setVisible(False)
        elif preset == "medium":
            sizes = self.sv.getMediumSizes()
            self.recalculate_button.setVisible(False)
        elif preset == "large":
            sizes = self.sv.getLargeSizes()
            self.recalculate_button.setVisible(False)
        elif preset == "current brush":
            sizes = self.calculate_current_brush_sizes()
            self.recalculate_button.setVisible(True)
        elif preset == "custom":
            sizes = self.sv.getCustomSizes()
            self.recalculate_button.setVisible(False)
        
        
        for i, size in enumerate(sizes):
            self.set_slider_range(i, size, preset)
            self.size_inputs[i].setText(str(size))
            self.size_sliders[i].setValue(int(size))
            
        self.presetChange = False
            
    '''
        999 is hard coded max size it can be larger depending of krita config, some user can find this annoying
    '''
    def set_slider_range(self, index, preset_value, preset):
        if preset != "custom":
            if index == 0:
                min_val, max_val = max(1, preset_value - 30), min(999, preset_value + 30)
            elif index == 1:
                min_val, max_val = max(1, preset_value - 50), min(999, preset_value + 50)
            elif index == 2:
                min_val, max_val = max(1, preset_value - 100), min(999, preset_value + 100)
            elif index == 3:
                min_val, max_val = max(1, preset_value - 500), min(999, preset_value + 500)
        else:
            min_val, max_val = self.sv.getCustomRange(index)

        self.size_sliders[index].setRange(int(min_val), int(max_val))


    def calculate_current_brush_sizes(self):
        current_size = self.get_current_brush_size()
        if current_size is None:
            current_size = self.sv.getMediumSizes()[2]  # Default to medium size if current size is not available

        size1 = max(0.5, min(999, floor(current_size / 5)))
        size2 = max(0.5, min(999, floor(current_size / 2)))
        size3 = current_size
        size4 = max(0.5, min(999, floor(current_size * 5 / 3)))

        return [int(size1), int(size2), int(size3), int(size4)]

    def get_current_brush_size(self):
        window = Krita.instance().activeWindow()
        if window and window.views():
            view = window.views()[0]
            return view.brushSize() 
        return None
    
    def set_brush_size(self, index):
        input_value = self.size_inputs[index].text()
        if input_value:
            try:
                size = float(input_value)
                self.change_brush_size(size)
            except ValueError:
                pass  # Handle the error as needed

    def change_brush_size(self, size):
        window = Krita.instance().activeWindow()
        if window and window.views():
            window.views()[0].setBrushSize(size)

    def update_input_from_slider(self, value, index):
        self.size_inputs[index].setText(str(value))
        if not self.presetChange:
            self.set_brush_size(index)

    
    def canvasChanged(self, canvas):
        pass