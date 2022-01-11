import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton

class Calculator(QWidget):
    def __init__(self):
        super(Calculator, self).__init__()


        self.is_correct = True
        self.op = ''

        self.vbox = QVBoxLayout(self)
        self.hbox_input = QHBoxLayout()
        self.hbox_first = QHBoxLayout()
        self.hbox_second = QHBoxLayout()
        self.hbox_third = QHBoxLayout()
        self.hbox_fourth = QHBoxLayout()
        self.hbox_result = QHBoxLayout()

        self.vbox.addLayout(self.hbox_input)
        self.vbox.addLayout(self.hbox_first)
        self.vbox.addLayout(self.hbox_second)
        self.vbox.addLayout(self.hbox_third)
        self.vbox.addLayout(self.hbox_fourth)
        self.vbox.addLayout(self.hbox_result)



        self.input = QLineEdit(self)
        self.hbox_input.addWidget(self.input)

        self.b_0 = QPushButton("0", self)
        self.hbox_first.addWidget(self.b_0)

        self.b_1 = QPushButton("1", self)
        self.hbox_first.addWidget(self.b_1)

        self.b_2 = QPushButton("2", self)
        self.hbox_first.addWidget(self.b_2)

        self.b_3 = QPushButton("3", self)
        self.hbox_first.addWidget(self.b_3)

        self.b_4 = QPushButton("4", self)
        self.hbox_second.addWidget(self.b_4)

        self.b_5 = QPushButton("5", self)
        self.hbox_second.addWidget(self.b_5)

        self.b_6 = QPushButton("6", self)
        self.hbox_second.addWidget(self.b_6)

        self.b_7 = QPushButton("7", self)
        self.hbox_second.addWidget(self.b_7)

        self.b_8 = QPushButton("8", self)
        self.hbox_third.addWidget(self.b_8)

        self.b_9 = QPushButton("9", self)
        self.hbox_third.addWidget(self.b_9)

        self.b_dot = QPushButton(".", self)
        self.hbox_third.addWidget(self.b_dot)

        self.b_plus = QPushButton("+", self)
        self.hbox_fourth.addWidget(self.b_plus)

        self.b_minus = QPushButton("-", self)
        self.hbox_fourth.addWidget(self.b_minus)

        self.b_multiply = QPushButton("*", self)
        self.hbox_fourth.addWidget(self.b_multiply)

        self.b_divide = QPushButton("/", self)
        self.hbox_fourth.addWidget(self.b_divide)

        self.b_result = QPushButton("=", self)
        self.hbox_result.addWidget(self.b_result) #разметки всех кнопок

        self.b_clear = QPushButton("C", self)
        self.hbox_third.addWidget(self.b_clear)



        self.b_plus.clicked.connect(lambda: self._operation("+"))
        self.b_minus.clicked.connect(lambda: self._operation("-"))
        self.b_multiply.clicked.connect(lambda: self._operation("*"))
        self.b_divide.clicked.connect(lambda: self._operation("/"))
        self.b_result.clicked.connect(self._result) #при нажатии на кнопку запускаем функцию
        self.b_clear.clicked.connect(self._clear)

        self.b_dot.clicked.connect(lambda: self._button("."))
        self.b_0.clicked.connect(lambda: self._button("0")) # при клике добавляем в строку инпута символ
        self.b_1.clicked.connect(lambda: self._button("1"))
        self.b_2.clicked.connect(lambda: self._button("2"))
        self.b_3.clicked.connect(lambda: self._button("3"))
        self.b_4.clicked.connect(lambda: self._button("4"))
        self.b_5.clicked.connect(lambda: self._button("5"))
        self.b_6.clicked.connect(lambda: self._button("6"))
        self.b_7.clicked.connect(lambda: self._button("7"))
        self.b_8.clicked.connect(lambda: self._button("8"))
        self.b_9.clicked.connect(lambda: self._button("9"))


    def _button(self, param): #при нажатии на символ
        if  not self.is_correct: 
            self.input.setText('')
            self.is_correct = True
        
        line = self.input.text() #сносим в лайн все что есть в инпуте\
        self.input.setText(line + param) #устанавливаем в инпут то что было + новый символ
        if line.count('.') >= 1 and param == '.':
            self._incorrect()


    def _operation(self, op): #оператор
        if self.op == '' and self.input.text() != '' and self.is_correct: # если инпут не пустой и оператор пустой и выражение корректно
            self.num_1 = float(self.input.text()) #в нам1 сносим все что было в строке
            self.op = op # присваиваем переменной оператора само действие 
            self.input.setText('') # в инпут записываем ''

        else:
            self._incorrect()


    def _result(self):
        if self.is_correct and self.input.text() != '' and not (float(self.input.text()) == 0 and self.op == '/'):
            self.num_2 = float(self.input.text()) #в нам2 сносим все что было в строке
            if self.op == "+":
                self.input.setText(str(self.num_1 + self.num_2)) 
            if self.op == "-":
                self.input.setText(str(self.num_1 - self.num_2))
            if self.op == "*":
                self.input.setText(str(self.num_1 * self.num_2))
            if self.op == "/":
                self.input.setText(str(self.num_1 / self.num_2))
            self.op = ''
        else:
            self._incorrect()


    def _incorrect(self): # обнуляем
        self.input.setText('Invalid expression')
        self.num_1, self.num_2 = 0, 0 # переменные чисел
        self.line = '' # символы лайна
        self.op = '' # оператор
        self.is_correct = False # корректность выражения


    def _clear(self):
        self.input.setText("")
        self.num_1, self.num_2 = 0, 0
        self.line = ''
        self.op = ''
        self.is_correct = False



app = QApplication(sys.argv)

win = Calculator()
win.show()

sys.exit(app.exec_())