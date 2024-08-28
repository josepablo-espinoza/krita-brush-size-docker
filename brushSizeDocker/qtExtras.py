from PyQt5.QtGui import QValidator

class FloatValidator(QValidator):
    def validate(self, input_str, pos):
        if not input_str:
            return (QValidator.Intermediate, input_str, pos)
        
        try:
            float(input_str)
            return (QValidator.Acceptable, input_str, pos)
        except ValueError:
            return (QValidator.Invalid, input_str, pos)
        
class IntValidator(QValidator):
    def validate(self, input_str, pos):
        if not input_str:
            return (QValidator.Intermediate, input_str, pos)
        
        try:
            int(input_str)
            return (QValidator.Acceptable, input_str, pos)
        except ValueError:
            return (QValidator.Invalid, input_str, pos)