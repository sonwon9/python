from inko import Inko
import keys
import keyboard

class Convert:
    def __init__(self):
        self.__inko = Inko(allowDoubleConsonant=True) # __은 private 선언
        self.__mode = 'Disabled'
        self.__input = ''

    def getMode(self):
        return self.__mode

    def setMode(self, mode):
        self.__mode = mode

    def convert(self, e):
        if self.__mode == 'EngToKor':   # 영어를 한글로 변환하고 싶은 경우
            if e.event_type == 'down':  # 키보드 이벤트는 키를 누르는 경우와 뗀 경우가 있는데 누르는 경우만 기능 수행
                if e.name in keys.ENG:       # 입력한 키가 영어인 경우
                    self.__input += e.name # self.__input에 값 붙여줌
                    
                elif e.name == 'backspace':     # 입력한 키가 backspace인 경우    
                    if self.__input:   # self.__input이 빈 경우가 아니라면
                        self.__input = self.__input[:-1]  # self.__input의 끝을 지움
                        
                elif e.name in keys.SPECIAL:     # SPECIAL은 f1이나 num lock, shift 키 등을 모아둔 리스트
                    pass                         # 입력받은 키가 SPECIAL에 포함되면 아무것도 하지 않는다.
            
                else:                            # 입력받은 키가 숫자,'-','+','?' 등의 특수문자, enter나 spacebar인 경우
                    cnt = len(self.__input) + 1
                    korean = self.__inko.en2ko(self.__input)  # self.__input을 넘겨서 영어를 한글로 바꿈
                    for _ in range(cnt):                    
                        keyboard.send('backspace')          # 써져있던 문자들을 지운다.
                    keyboard.write(korean)                  # 그리고 그 자리에 korean을 입력해준다.
                    keyboard.send(e.name)
                    self.__input = ''                       # self.__input을 비운다.

        elif self.__mode == 'KorToEng': # 한글을 영어로 변환하고 싶은 경우
            if e.event_type == 'down': # 키보드 이벤트는 키를 누르는 경우와 뗀 경우가 있는데 누르는 경우만 기능 수행
                if e.name in keys.ENG: # 입력한 키가 영어로 바뀔 수 있는 키일때만 변환
                    keyboard.send('backspace')  # keyboard 모듈은 한글을 쳐도 영어로 인식되므로 지우고 영어로 써주면 끝
                    keyboard.write(e.name)
            
if __name__ == '__main__':
    c1 = Convert()
    #c1.setMode('EngToKor')
    #c1.setMode('KorToEng')
    keyboard.hook(c1.convert)
    keyboard.wait()     
                
            
        
