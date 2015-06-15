#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'werdeil'

from Tkinter import *
import tkFileDialog
import tombola
import time


class InterfaceGauche(LabelFrame):
    '''Left frame of the GUI, giving the buttons and the current price and winner'''
    def __init__(self, tk_frame, waiting_time, **kwargs):
        LabelFrame.__init__(self, tk_frame, text="Tirage", **kwargs)
        self.waiting_time = waiting_time

        self.message = Label(self, text="Appuyez sur le bouton pour lancer le tirage")
        self.message.grid(column=0, row=0, columnspan=2)

        self.bouton_quitter = Button(self, text="Quitter", command=self.quit)
        self.bouton_quitter.grid(column=0, row=1, pady=10)

        self.bouton_cliquer = Button(self, text="Lancer!", fg="red",
                                     command=self.click)
        self.bouton_cliquer.grid(column=1, row=1)

        self.message_price = Label(self, text="Tirage pour:")
        self.price = Label(self, text='', bg="white", width=30, height=1)
        self.message_price.grid(column=0, row=2)
        self.price.grid(column=1, row=2, columnspan=1, padx=10, pady=10)

        self.message_name = Label(self, text="Le gagnant est:")
        self.name = Label(self, text="", bg="white", width=30, height=1)
        self.message_name.grid(column=0, row=4)
        self.name.grid(column=1, row=4, columnspan=1, pady=10)
        
        self.parent_name = self.winfo_parent()
        self.parent = self._nametowidget(self.parent_name)

        # partie sablier
        self.next_draw = Label(self, text="Prochain tirage dans")
        self.next_draw.grid(column=0, row=6, columnspan=1)
        self.next_wait = Label(self, text="%s s" % self.waiting_time)
        self.next_wait.grid(column=1, row=6, columnspan=1)
        self.nb_players_text = Label(self, text="Nombre de joueurs")
        self.nb_players_text.grid(column=0, row=8, columnspan=1)
        self.nb_players = Label(self, text="0")
        self.nb_players.grid(column=1, row=8, columnspan=1)
        self.nb_prices_text = Label(self, text="Nombre de prix restants")
        self.nb_prices_text.grid(column=0, row=9, columnspan=1)
        self.nb_prices = Label(self, text="0")
        self.nb_prices.grid(column=1, row=9, columnspan=1)

        # for i in range(5):
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

    def click(self):
        '''When click is selected, the tombola starts'''
       
        self.parent.draw_tombola(self.waiting_time)

        if not self.parent.list_prices:
            self.bouton_cliquer.config(state=DISABLED)
            self.next_wait["text"] = "Tous les lots ont été tirés"
            self.update()
            
    def update_nb_players(self):        
        self.nb_players["text"] = len(self.parent.list_names)
        self.nb_players.update()
        
    def update_nb_prices(self):        
        self.nb_prices["text"] = len(self.parent.list_prices)
        self.nb_prices.update()


class TableResults(LabelFrame):
    '''Right frame of the GUI, giving the results of the already won prices'''
    def __init__(self, tk_frame, **kwargs):
        LabelFrame.__init__(self, tk_frame, text="Resultats", **kwargs)
        self.names_title = Label(self, text="Nom")
        self.names_title.grid(column=0, row=0)
        self.names = Label(self, text="")
        self.names.grid(column=0, row=1)
        self.price_title = Label(self, text="Cadeau")
        self.price_title.grid(column=1, row=0)
        self.prices = Label(self, text="")
        self.prices.grid(column=1, row=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


class FenetreTombola(Tk):
    '''Main window containing the 2 frames'''
    def __init__(self, waiting_time, **kwargs):
        Tk.__init__(self, **kwargs)
        # self.geometry("810x520")
        self.list_names = []
        self.list_prices = []
        self.title("Tombola")
        self.interface = InterfaceGauche(self, waiting_time)
        self.interface.grid(column=0, row=0)
        self.results = TableResults(self)
        self.results.grid(column=1, row=0)
        self.interface.pack(fill=BOTH, expand=1, side=LEFT)
        self.results.pack(fill=BOTH, expand=1, side=LEFT)
        
        # Partie Menu de la fenetre
        self.menubar = Menu(self)

        self.menu1 = Menu(self.menubar, tearoff=0)
        self.menu1.add_command(label="Importer prix", command=self.load_prices)
        self.menu1.add_command(label="Importer joueurs", command=self.load_names)
        self.menu1.add_separator()
        self.menu1.add_command(label="Quitter", command=self.quit)
        self.menubar.add_cascade(label="Fichier", menu=self.menu1)

        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="A propos", command=self.alert)
        self.menubar.add_cascade(label="Aide", menu=self.menu2)

        self.config(menu=self.menubar)
        
        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '.csv'
        options['filetypes'] = [('all files', '.*'), ('csv files', '.csv')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.csv'
        options['parent'] = self
        options['title'] = 'This is a title'

    def draw_tombola(self, wait_time):
        while len(self.list_prices) > 0:
            price = self.list_prices.pop(0)
            self.interface.price["text"] = price
            self.interface.name["text"] = ''
            countdown = wait_time
            for i in range(countdown+1):
                self.interface.next_wait["text"] = "%s s" % countdown
                self.interface.next_wait.update()
                time.sleep(1)
                countdown -= 1
            self.update()
            time.sleep(0.25)
            name, self.list_names = tombola.draw_name(self.list_names)
            self.interface.name["text"] = name
            self.interface.name.update()
            time.sleep(1)

            self.results.names["text"] += "%s\n" % name
            self.results.prices["text"] += "%s\n" % price
            self.interface.update_nb_players()
            self.interface.update_nb_prices()
            self.results.update()
            tombola.write_results('save.csv', name, price)
            time.sleep(1)

    def alert(self):
        from tkMessageBox import *
        showinfo("alerte", "Bravo!")
        
    def load_names(self):
        """Returns an opened file in read mode."""
        self.list_names = tombola.import_lists(tkFileDialog.askopenfilename(**self.file_opt))
        self.interface.update_nb_players()
        
    def load_prices(self):
        """Returns an opened file in read mode."""
        self.list_prices = tombola.import_prices(tkFileDialog.askopenfilename(**self.file_opt))
        self.interface.update_nb_prices()
        
        
if __name__ == "__main__":
    # list_names = tombola.import_lists("list_names_test.csv")
    # list_prices = ['pen', 'bag', 'wallet'] # To be corrected to import it from a csv too
    frame = FenetreTombola(10) # The waiting time shall be parametrisable in the gui

    frame.mainloop()
