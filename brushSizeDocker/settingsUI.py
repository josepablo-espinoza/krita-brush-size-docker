from PyQt5.QtWidgets import (
    QComboBox, QGridLayout, QLabel, QLineEdit, QFrame,
    QPushButton, QVBoxLayout, QDialog, QHBoxLayout
)
from .settingsService import *
from .qtExtras import *

class SettingsUI(QDialog):
    
    def __init__(self, settingsService: SettingsService, parent=None) -> None:
        super().__init__(parent)
        self.sv = settingsService
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()
        customValues = self.sv.getCustomSettings()

        # ComboBox
        combo_layout = QHBoxLayout()
        combo_label = QLabel("Default mode:")
        self.size_combobox = QComboBox()
        self.size_combobox.addItems(self.sv.getDropdown().keys())
        self.size_combobox.setCurrentIndex(self.sv.getDefaultModeInt())

        combo_layout.addWidget(combo_label, 1)
        combo_layout.addWidget(self.size_combobox, 3)
        main_layout.addLayout(combo_layout)

        main_layout.addWidget(self.size_combobox)

        # Custom Sizes Label and Horizontal Line
        custom_sizes_layout = QVBoxLayout()
        custom_sizes_label = QLabel("Custom Sizes")
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)
        
        custom_sizes_layout.addWidget(custom_sizes_label)
        custom_sizes_layout.addWidget(horizontal_line)

        main_layout.addLayout(custom_sizes_layout)

        # Table Layout
        table_layout = QGridLayout()

        # First row (headers)
        table_layout.addWidget(QLabel(''), 0, 0)
        table_layout.addWidget(QLabel('Size'), 0, 1)
        table_layout.addWidget(QLabel('Min Size'), 0, 2)
        table_layout.addWidget(QLabel('Max Size'), 0, 3)

        self.size_inputs = {}
        for i, key in enumerate(customValues.keys(), start=1):
            data = customValues[key]
            table_layout.addWidget(QLabel(f'Size {i}'), i, 0)
            
            size_input = QLineEdit(str(data['size']))
            min_input = QLineEdit(str(data['min']))
            max_input = QLineEdit(str(data['max']))
            
            size_input.setValidator(IntValidator())
            min_input.setValidator(IntValidator())
            max_input.setValidator(IntValidator())

            self.size_inputs[key] = {
                'size': size_input,
                'min': min_input,
                'max': max_input
            }

            table_layout.addWidget(size_input, i, 1)
            table_layout.addWidget(min_input, i, 2)
            table_layout.addWidget(max_input, i, 3)

        # Add table layout to the main layout
        main_layout.addLayout(table_layout)

        # Buttons
        button_layout = QGridLayout()
        self.save_button = QPushButton('Save')
        self.cancel_button = QPushButton('Cancel')
        button_layout.addWidget(self.save_button, 0, 0)
        button_layout.addWidget(self.cancel_button, 0, 1)

        # Add buttons to the main layout
        main_layout.addLayout(button_layout)


        # Set main layout
        self.setLayout(main_layout)

        # Connect the save button to a function to print the selected value
        self.save_button.clicked.connect(self.saveSettings)
        self.cancel_button.clicked.connect(self.cancelSettings)

    def emitCloseDialog(self):
        self.parent().closeDialog()
        self.done(0)

    def cancelSettings(self):
        self.emitCloseDialog()

    def saveSettings(self):
        
        defaultMode = self.sv.getDropdown()[self.size_combobox.currentText()]
        
        customSettings = {}
        for key, inputs in self.size_inputs.items():
            customSettings[key] = {
                'size': int(inputs['size'].text()),
                'min': int(inputs['min'].text()),
                'max': int(inputs['max'].text())
            }

        # save
        self.sv.saveSettings(defaultMode, customSettings)
        
        self.emitCloseDialog()