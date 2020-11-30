from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLineEdit, QToolButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QLayout, QGridLayout

import threading
from convert import Convert
import keyboard

class Button(QToolButton):

    def __init__(self, text, callback):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)
        self.clicked.connect(callback)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(size.width() + 100)
        return size


class Converter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.convert = Convert()

        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        '''
        buttonGroups = {
            'English -> Korean (QWERTY)' : 'EngToKor',
            'Korean -> English (QWERTY)' : 'KorToEng',
        }
        '''
        EngToKor = Button('English -> Korean (QWERTY)',
                          lambda: self.setModeAndText('English -> Korean (QWERTY)', 'EngToKor'))
        mainLayout.addWidget(EngToKor, 0, 0)

        KorToEng = Button('Korean -> English (QWERTY)',
                          lambda: self.setModeAndText('Korean -> English (QWERTY)', 'KorToEng'))
        mainLayout.addWidget(KorToEng, 1, 0)
        
        stopConvert = Button('Stop Convert', lambda: self.setModeAndText('Disabled','Disabled'))
        mainLayout.addWidget(stopConvert, 2, 0)

        self.display = QLineEdit()
        self.setModeAndText('Disabled', 'Disabled')
        self.display.setReadOnly(True)
        mainLayout.addWidget(self.display, 3, 0)

        self.setLayout(mainLayout)

        self.setWindowTitle('Converter')
        
        keyboardThread = threading.Thread(target=self.keyboardStart) 
        keyboardThread.daemon = True
        keyboardThread.start() # keyboard.wait()도 루프, gui도 루프이므로 threading을 해줘야 함.

    def keyboardStart(self): 
        keyboard.hook(self.convert.convert)
        keyboard.wait()
        
        
    def setModeAndText(self, text, mode): # 버튼을 누를 때 연결될 함수. 상태를 보여주고 mode를 바꿈.
        self.display.setText('Current status: ' + text)
        self.convert.setMode(mode)
        #print(self.convert.getMode())

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    conv = Converter()
    conv.show()
    sys.exit(app.exec_())
            
            
    
