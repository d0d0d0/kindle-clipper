#!/usr/bin/python3
# -*- coding: utf-8 -*-

from kindle_clipper import Clipper

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import tkinter.messagebox as messagebox

class ClipperUI:

	def __init__(self):
		self.clipper = Clipper()
		self.selected_books = []

		self.init_main_screen()
		
	def init_main_screen(self):
		
		self.window = tk.Tk()
		self.window.title('Kindle Clipper')
		self.window.resizable(False, False)
		self.window.geometry('380x350')

		# open clippings button
		open_clippings_button = ttk.Button(self.window, text='Open clippings', command=self.open_clippings_handler)
		open_clippings_button.grid(column=0, row=0, sticky='w', padx=15, pady=15)

		# generate highlights
		self.generate_highlights_button = ttk.Button(self.window, text='Export selected', command=self.generate_highlights_handler, state=tk.DISABLED)
		self.generate_highlights_button.grid(column=1, row=0, sticky='w', padx=15, pady=15)

		# generate highlights
		self.generate_all_highlights_button = ttk.Button(self.window, text='Export all', command=self.generate_all_highlights_handler, state=tk.DISABLED)
		self.generate_all_highlights_button.grid(column=2, row=0, sticky='w', padx=15, pady=15)

		self.window.mainloop()

	def open_clippings_handler(self):

		file_name = fd.askopenfilename(filetypes=(('text files', '*.txt'), ('All Files', '*.*')))

		self.clipper.load_file(file_name)
		self.clipper.list_books()

		self.listbox = tk.Listbox(self.window, listvariable=tk.StringVar(value=self.clipper.book_list), height=15, selectmode='extended')
		self.listbox.grid(column=0, row=1, rowspan=4, columnspan=3, padx=10, pady=10, sticky='nwes')
		self.listbox.bind('<<ListboxSelect>>', self.select_book_event)

		scrollbar = tk.Scrollbar(self.window, orient="vertical", command=self.listbox.yview)
		scrollbar.grid(column=4, row=1, rowspan=4, sticky='ns')
		self.listbox.configure(yscrollcommand=scrollbar.set, scrollregion=self.listbox.bbox("end"))
		
		self.generate_all_highlights_button['state'] = tk.NORMAL

	def select_book_event(self, event):
		selected_indices = self.listbox.curselection()
		self.selected_books = [self.clipper.book_list[i] for i in selected_indices]

		if self.selected_books:
			self.generate_highlights_button['state'] = tk.NORMAL
		else:
			self.generate_highlights_button['state'] = tk.DISABLED

	def generate_highlights_handler(self):
		notebook = {}
		for book in self.selected_books:
			notebook.update(self.clipper.find_notes_by_book(str(book)))

		file_name = fd.asksaveasfilename(filetypes=(('document', '*.docx'), ('All Files', '*.*')))
		if file_name:
			messagebox.showinfo("Export completed",  "Selected highlights are extracted to %s.docx" %(file_name))
			self.clipper.write_notes(notebook, file_name)

	def generate_all_highlights_handler(self):
		file_name = fd.asksaveasfilename(filetypes=(('document', '*.docx'), ('All Files', '*.*')))
		
		if file_name:
			self.clipper.write_notes(self.clipper.notebook, file_name, is_dictionary=True)
			messagebox.showinfo("Export completed",  "All highlights are extracted to %s.docx" %(file_name))
			self.window.destroy()





