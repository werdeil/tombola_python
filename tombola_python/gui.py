#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'werdeil'

from Tkinter import *
from ttk import Progressbar
import tkFileDialog
from tkMessageBox import showinfo, showerror
import tombola
import time
import tkFont


class InterfaceGauche(LabelFrame):
    """Left frame of the GUI, giving the buttons and the current price and winner"""
    def __init__(self, tk_frame, police, **kwargs):
        LabelFrame.__init__(self, tk_frame, text="Tirage", font=police, **kwargs)
        self.waiting_time = 10

        self.message = Label(self, text="Appuyez sur le bouton pour lancer le tirage", font=police)
        self.message.grid(column=0, row=0, columnspan=2)

        self.bouton_quitter = Button(self, text="Quitter", command=self.quit, font=police)
        self.bouton_quitter.grid(column=0, row=1, pady=10)

        self.bouton_cliquer = Button(self, text="Lancer!", fg="red",
                                     command=self.click, font=police)
        self.bouton_cliquer.grid(column=1, row=1)

        self.message_price = Label(self, text="Tirage pour:", font=police)
        self.price = Label(self, text='', bg="white", width=40, height=1, font=police)
        self.message_price.grid(column=0, row=3)
        self.price.grid(column=1, row=3, columnspan=1, padx=10, pady=10)

        self.message_name = Label(self, text="Le gagnant est:", font=police)
        self.name = Label(self, text="", bg="white", width=40, height=1, font=police)
        self.message_name.grid(column=0, row=4)
        self.name.grid(column=1, row=4, columnspan=1, pady=10)
        
        self.parent_name = self.winfo_parent()
        self.parent = self._nametowidget(self.parent_name)

        # Part waiting time
        self.interval = Label(self, text="Intervalle entre tirages (s)", font=police)
        self.interval.grid(column=0, row=6, columnspan=1, pady=10)
        self.v = StringVar()
        self.v.set(self.waiting_time)
        self.interval_length = Entry(self, textvariable=self.v,  width=5, justify=CENTER, font=police)
        self.interval_length.grid(column=1, row=6, columnspan=1)
        self.progress_bar = Progressbar(self, length=300)
        self.progress_bar.grid(column=0, row=8, columnspan=2, pady=10)
        self.nb_players_text = Label(self, text="Nombre de joueurs", font=police)
        self.nb_players_text.grid(column=0, row=10, columnspan=1, pady=10)
        self.nb_players = Label(self, text="0", font=police)
        self.nb_players.grid(column=1, row=10, columnspan=1, pady=10)
        self.nb_prices_text = Label(self, text="Nombre de prix restants", font=police)
        self.nb_prices_text.grid(column=0, row=11, columnspan=1, pady=10)
        self.nb_prices = Label(self, text="0", font=police)
        self.nb_prices.grid(column=1, row=11, columnspan=1, pady=10)

        # police=tkFont.Font(self, size=12)#, family='Courier')
        # self.config(, font=police)
        # for i in range(5):
        # self.grid_rowconfigure(2, weight=1)
        # self.grid_rowconfigure(5, weight=1)
        # self.grid_rowconfigure(7, weight=1)
        # self.grid_rowconfigure(9, weight=1)
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

    def click(self):
        """When click is selected, the tombola starts"""
        try:
            self.waiting_time = int(self.v.get())
        except ValueError:
            showerror("Error", "L'intervalle doit être un nombre")
            return
        self.progress_bar['maximum'] = self.waiting_time+0.01
        self.interval_length.config(state=DISABLED)
        self.parent.draw_tombola(self.waiting_time)

        if not self.parent.list_prices:
            self.bouton_cliquer.config(state=DISABLED)
            self.price["text"] = "Tous les lots ont été tirés"
            self.name["text"] = ""
            self.update()
            
    def update_nb_players(self):        
        self.nb_players["text"] = len(self.parent.list_names)
        self.nb_players.update()
        
    def update_nb_prices(self):        
        self.nb_prices["text"] = len(self.parent.list_prices)
        self.nb_prices.update()


class TableResults(LabelFrame):
    """Right frame of the GUI, giving the results of the already won prices"""
    def __init__(self, tk_frame, police, **kwargs):
        LabelFrame.__init__(self, tk_frame, text="Resultats", font=police, **kwargs)
        self.names_title = Label(self, text="Nom", bg="#D3D3D3", relief=GROOVE, width=40, font=police)
        self.names_title.grid(column=1, row=0)
        self.price_title = Label(self, text="Cadeau", bg="#D3D3D3", relief=GROOVE, width=40, font=police)
        self.price_title.grid(column=2, row=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)


class FenetreTombola(Tk):
    """Main window containing the 2 frames"""
    def __init__(self, **kwargs):
        Tk.__init__(self, **kwargs)
        self.police = tkFont.Font(self, size=9)
        self.list_names = []
        self.list_prices = []
        self.title("Tombola")
        self.interface = InterfaceGauche(self, self.police)
        self.interface.grid(column=0, row=0)
        self.results = TableResults(self, self.police)
        self.results.grid(column=1, row=0)
        self.interface.pack(fill=BOTH, expand=1, side=LEFT)
        self.results.pack(fill=BOTH, expand=1, side=LEFT)
        
        # Partie Menu de la fenetre
        self.menubar = Menu(self)

        self.menu1 = Menu(self.menubar, tearoff=0)
        self.menu1.add_command(label="Importer joueurs", command=self.load_names, font=self.police)
        self.menu1.add_command(label="Importer prix", command=self.load_prices, font=self.police)
        self.menu1.add_separator()
        self.menu1.add_command(label="Quitter", command=self.quit, font=self.police)
        self.menubar.add_cascade(label="Menu", menu=self.menu1, font=self.police)

        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="A propos", command=self.about, font=self.police)
        self.menubar.add_cascade(label="Aide", menu=self.menu2, font=self.police)

        self.config(menu=self.menubar)

    def draw_tombola(self, wait_time):
        i = 1
        label_name = []
        label_price = []
        while len(self.list_prices) > 0:
            # Get the next price and update left interface
            price = self.list_prices.pop(0)
            self.interface.price["text"] = price
            self.interface.name["text"] = ''

            # Wait before picking the winner
            for second in range(wait_time):
                self.interface.progress_bar.step()
                self.interface.progress_bar.update()
                time.sleep(1)

            self.update()  # to test if it is still necessary
            time.sleep(0.25)  # to test if it is still necessary

            # Draw the name of the winner and update all the fields
            name, self.list_names = tombola.draw_name(self.list_names)
            self.interface.name["text"] = name
            self.interface.progress_bar['value'] = 0
            self.interface.name.update()
            time.sleep(0.25)

            # Add the result in the right panel
            label_name.append(Label(self.results, text=name, relief=GROOVE, width=40, font=self.police))
            label_name[i-1].grid(column=1, row=i)
            label_price.append(Label(self.results, text=price, relief=GROOVE, width=40, font=self.police))
            label_price[i-1].grid(column=2, row=i)
            self.interface.update_nb_players()
            self.interface.update_nb_prices()
            self.results.update()

            # Write the results in the save file
            tombola.write_results('save.csv', name, price)
            time.sleep(0.25)
            i += 1

    def about(self):
        showinfo("About",
                 '''Tombola Python, Copyright (C) 2015 werdeil \n
Tombola Python comes with ABSOLUTELY NO WARRANTY.\n
This is free software, and you are welcome to redistribute it under certain conditions.''', parent=self)
        
    def load_names(self):
        """Returns an opened file in read mode."""
        filename = tkFileDialog.askopenfilename(filetypes=[('all files', '.*'), ('csv files', '.csv')],
                                                title='Importer la liste des joueurs', parent=self)
        if len(filename) != 0:
            self.list_names = tombola.import_lists(filename)
            self.interface.update_nb_players()
        
    def load_prices(self):
        """Returns an opened file in read mode."""
        filename = tkFileDialog.askopenfilename(filetypes=[('all files', '.*'), ('csv files', '.csv')],
                                                title='Importer la liste des prix', parent=self)
        if len(filename) != 0:
            self.list_prices = tombola.import_prices(filename)
            self.interface.update_nb_prices()
        
        
if __name__ == "__main__":
    frame = FenetreTombola()
    frame.mainloop()
