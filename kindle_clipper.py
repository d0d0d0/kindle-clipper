#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
from docx import Document
from docx.shared import Inches

class Clipper:

	def __init__(self):
		self.clippings = None
		self.notebook = {}
		self.book_list = []
		self.dictionary = []

	def load_file(self, input):
		self.clippings = open(input, 'r', encoding='utf-8').read()
		self.create_notebook()

	def list_books(self):
		self.book_list = [book for book, _ in self.notebook.items()]

	def create_notebook(self):
		notebook = {}

		for c in filter(None, self.clippings.split("==========\n")):
			lines = list(filter(None, c.split("\n")))

			if len(lines) < 3: # there is no text
				continue 

			header, meta, text = filter(None, lines)
			
			if " " not in text: # if it is just a word
				text = re.sub(r'[^\w\s]', '', text)
				self.dictionary.append(text)
				continue

			book, writer = header[:-1].rsplit(" (", 1)
			book = re.sub('/[\x00-\x1F\x7F]/u','', book) # encode to ascii

			indicators = meta.split(" | ")

			page = 0 if len(indicators) < 3 else indicators[0].split("page ")[-1]
			date = (indicators[-1].split("Added on ")[-1]).rsplit(" ", 2)[0]

			note = {"page": page, "date": date, "text": text}

			if book not in notebook:
				notebook[book] = {"writer": writer, "notes": []}

			notebook[book]["notes"].append(note)

		self.notebook = notebook
		return notebook

	def find_notes_by_book(self, book):
		partial_notebook = {}
		for k,v in self.notebook.items():
			if book in k:
				partial_notebook[k] = v

		return partial_notebook

	def find_notes_by_writer(self, writer):
		partial_notebook = {}
		for k,v in self.notebook.items():
			if writer in v["writer"]:
				partial_notebook[k] = v

		return partial_notebook

	def write_notes(self, notebook, out, type="docx", is_dictionary=False):

		if type == "txt":
			doc = "Reading Notes\n\n"
			for k,v in notebook.items():
				doc += "%s\n%s\n\n" %(k, v["writer"])
				for n in v["notes"]:
					doc += "- %s (on p.%s at %s)\n" %(n["text"], n["page"], n["date"])
				doc += "\n"

			f = open(out + ".txt", 'w+')
			f.write(doc)
			f.close()

		else:
			document = Document()
			document.add_heading('Reading Notes', 0)
			for k,v in notebook.items():
				document.add_heading(k, level=2)
				document.add_heading(v["writer"], level=4)
				for n in v["notes"]:
					t = "%s (on p.%s at %s)\n" %(n["text"], n["page"], n["date"])
					document.add_paragraph(t, style='List Bullet')

			if is_dictionary:
				document.add_heading("Dictionary", level=2)
				document.add_paragraph(", ".join(self.dictionary))

			document.save(out + ".docx")
