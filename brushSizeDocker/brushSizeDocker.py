from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox, QSlider, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QValidator
from krita import DockWidget, Krita
from math import floor

DOCKER_NAME = 'Brush Size Docker'

# PRESETS
small_sizes = [1, 2.5, 5, 8]
medium_sizes = [10, 25, 50, 80]
large_sizes = [50, 100, 400, 900]

class FloatValidator(QValidator):
    def validate(self, input_str, pos):
        if not input_str:
            return (QValidator.Intermediate, input_str, pos)
        
        try:
            float(input_str)
            return (QValidator.Acceptable, input_str, pos)
        except ValueError:
            return (QValidator.Invalid, input_str, pos)

class BrushSizeDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_NAME)

        self.widget = QWidget(self)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 15, 0, 0)  # Reduce the margins around the layout

        self.size_inputs = []
        self.size_sliders = []

        # dropdown
        self.preset_selector = QComboBox(self)
        self.preset_selector.addItems(["Small", "Medium", "Large", "Current Brush"])
        self.preset_selector.setCurrentIndex(1)  # Set "Medium" as the default preset
        self.preset_selector.currentIndexChanged.connect(self.update_preset)

        self.layout.addWidget(self.preset_selector)

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

    def update_preset(self):
        preset = self.preset_selector.currentText().lower()
        if preset == "small":
            sizes = small_sizes
            self.recalculate_button.setVisible(False)
        elif preset == "medium":
            sizes = medium_sizes
            self.recalculate_button.setVisible(False)
        elif preset == "large":
            sizes = large_sizes
            self.recalculate_button.setVisible(False)
        elif preset == "current brush":
            sizes = self.calculate_current_brush_sizes()
            self.recalculate_button.setVisible(True)

        for i, size in enumerate(sizes):
            self.set_slider_range(i, size)
            self.size_inputs[i].setText(str(size))
            self.size_sliders[i].setValue(int(size))
            

    def set_slider_range(self, index, preset_value):
        if index == 0:
            min_val, max_val = max(1, preset_value - 30), min(999, preset_value + 30)
        elif index == 1:
            min_val, max_val = max(1, preset_value - 50), min(999, preset_value + 50)
        elif index == 2:
            min_val, max_val = max(1, preset_value - 100), min(999, preset_value + 100)
        elif index == 3:
            min_val, max_val = max(1, preset_value - 500), min(999, preset_value + 500)

        self.size_sliders[index].setRange(int(min_val), int(max_val))


    def calculate_current_brush_sizes(self):
        current_size = self.get_current_brush_size()
        if current_size is None:
            current_size = medium_sizes[2]  # Default to medium size if current size is not available

        size1 = max(0.5, min(999, floor(current_size / 5)))
        size2 = max(0.5, min(999, floor(current_size / 2)))
        size3 = current_size
        size4 = max(0.5, min(999, floor(current_size * 5 / 3)))

        return [size1, size2, size3, size4]

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
        self.set_brush_size(index)

    
    def canvasChanged(self, canvas):
        pass
