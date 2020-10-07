# -*- coding: utf-8 -*-
# values-conv.py
# v2020-10-07, RTG
# Tested with Python 3.8.5
# Licence: free-for-all

# how to make a standalone executable bundle for win/lin: 
# python -m PyInstaller values-conv.py -F -w

import os
from tkinter import *
import tkinter.ttk as ttk

class Converter(Tk):

    buttons_settings = [
        {'text': "Загрузить", 'command': 'load_profile'},
        {'text': "Рассчитать", 'command': 'recalculate'},
        {'text': "Сохранить", 'command': 'save_profile'},
    ]

    # should to use short unique latin ids
    person_settings = [
        {'id':'name', 'value': "Иван", 'text': "Имя"},
        {'id':'span', 'value': "17.78", 'text': "Длина пяди, см"},
        {'id':'arm1', 'value': "71.12", 'text': "Длина аршина, см"},
        {'id':'palm', 'value': "10.16", 'text': "Ширина ладони, см"},
    ]

    # should to use short unique latin ids
    conversion_settings = [
    
        { 'text': "Длина локтя = {} сантиметров\n", 
          'formula': 'palm * 6', 
          'result_id':'elbow'},
          
        { 'text': "Три с половиной локтя = {} сантиметров\n", 
          'formula': '3.5 * elbow', 
          'result_id':'result_1'},
          
        { 'text': "Три с половиной локтя = {} ладоней\n", 
          'formula': 'result_1 / palm', 
          'result_id':'result_2'},
          
        { 'text': "Длина ложки (1.2 пяди) = {} сантиметров\n", 
          'formula': 'span * 1.2', 
          'result_id':'result_3'},
    ]


    def __init__(self):
    
        Tk.__init__(self)
        self.title("values-conv.py")
        self.geometry('350x400')

        # GUI: general framework

        self.title_lbl = Label(self, text="Конвертер величин из метрической системы в русскую")
        self.title_lbl.pack(side=TOP, fill=X,  expand=False)

        self.top_sep = ttk.Separator(self, orient=HORIZONTAL )
        self.top_sep.pack(side=TOP, fill=X, expand=False)

        middle_frame = Frame(self)
        middle_frame.pack(side=TOP, fill=X, expand=False)

        self.bottom_sep = ttk.Separator(self, orient=HORIZONTAL )
        self.bottom_sep.pack(side=TOP, fill=X, expand=False)
        
        text_frame = Frame(self)
        text_frame.pack(side=BOTTOM, fill=BOTH, expand=True)

        
        # GUI: frame with input fields

        input_frame = Frame(middle_frame)
        input_frame.pack(side=LEFT, fill=BOTH, expand=True)

        for person in self.person_settings:
        
            person['frame'] = Frame(input_frame)
            person['frame'].pack(side=TOP, fill=X, expand=True)
            
            person['label'] = Label( person['frame'], text=person['text'])
            person['label'].pack(side=LEFT)
            
            person['variable'] = StringVar()
            person['variable'].set( person['value'] )

            person['entry'] = Entry(person['frame'], width=15, textvariable=person['variable'])
            person['entry'].pack(side=RIGHT)


        # GUI: vertical separator in the middle

        self.middle_sep = ttk.Separator(middle_frame, orient=VERTICAL )
        self.middle_sep.pack(side=LEFT, fill=Y, expand=True)


        # GUI: frame with buttons

        button_frame = Frame(middle_frame)
        button_frame.pack(side=RIGHT, fill=Y, expand=True)
        
        for button in self.buttons_settings:
        
            button['object'] = Button( button_frame, text=button['text'], 
                command=getattr(self, button['command']))
            button['object'].grid(sticky="ew")
            
            #self.btn1.grid(column=0, row=0, sticky="ew")
            #self.btn1.pack()#side=TOP, fill=X, expand=True)
         

        # GUI: frame with text field

        self.text = Text(text_frame, width=1, height=1, borderwidth=5, 
            relief="flat", wrap=WORD) #, state="disabled")
        self.text.pack(side=LEFT, fill=BOTH, expand=True)
         
        self.scroll = Scrollbar(text_frame, command=self.text.yview)
        self.scroll.pack(side=LEFT, fill=Y)
         
        self.text.config(yscrollcommand=self.scroll.set)
        


    def save_profile(self):

        person_name = self.person_settings[0]['value'] 
        file_name = os.path.join(os.getcwd(), person_name + '.txt')
        
        text = self.text.get(1.0, END)

        with open(file_name,'wb') as f_obj:
        
            f_obj.write(text.encode('utf8'))


    def load_profile(self):

        person_name = self.person_settings[0]['value'] 
        file_name = os.path.join(os.getcwd(), person_name + '.txt')
        
        self.text.delete(1.0, END)
        
        if not os.path.isfile(file_name):
        
            self.text.insert(1.0, f"Ошибка: нет файла \"{file_name}\" !")
            
        else:
        
            with open(file_name,'rb') as f_obj:
                text = f_obj.read().decode('utf8')
                
            self.text.insert(1.0, text)
        

    def recalculate(self):

        self.text.delete(1.0, END)
        local_values_dict = {}
        strings = []

        for person in self.person_settings:
            try:
                local_values_dict[person['id']] = float(person['value'])
            except:
                pass
            strings.append( f"{person['text']}: {person['value']}\n" )

        strings.append('\n\n')
            
        for conv in self.conversion_settings:
            result = eval(conv['formula'], local_values_dict)
            local_values_dict[conv['result_id']] = result
            strings.append( conv['text'].format( round(result, 3) ) )

        for string in strings:
            self.text.insert(END, string)



if __name__ == "__main__":
    app = Converter()
    app.mainloop()
    
    