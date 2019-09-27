#!/usr/bin/python3
# -*- coding: utf-8 -*-

import getpass
from docx import Document
from docx.shared import Inches

temp = "%s\n%s\n\n"
user = getpass.getuser()
fname = "/media/%s/Kindle/documents/My Clippings.txt" % (user)

class Clipper:

	def __init__(self, inp=fname):
		self.clippings = open(inp, 'r', encoding='utf-8-sig').read()
		self.notebook = None

	def createNotebook(self):
		notebook = {}
		for c in filter(None, self.clippings.split("==========\n")):
			header, meta, text = filter(None, c.split("\n"))

			book, writer = header[:-1].split(" (")
			
			smeta = meta.split(" | ")
			page = smeta[0].split("Page ")[-1]
			date = smeta[2].split("Added on ")[-1]

			note = {"page": page, "date": date, "text": text}

			if book not in notebook:
				notebook[book] = {"writer": writer, "notes": []}

			notebook[book]["notes"].append(note)

		self.notebook = notebook
		return notebook

	def findNotesByBook(self, book):
		partial_notebook = {}
		for k,v in self.notebook.items():
			if book in k:
				partial_notebook[k] = v

		return partial_notebook


	def findNotesByWriter(self, writer):
		partial_notebook = {}
		for k,v in self.notebook.items():
			if writer in v["writer"]:
				partial_notebook[k] = v

		return partial_notebook

	def writeNotes(self, notebook, out, type="txt"):
		if type == "txt":
			doc = "Reading Notes\n\n"
			for k,v in notebook.items():
				doc += temp %(k, v["writer"])
				for n in v["notes"]:
					doc += "- %s (on p.%s at %s)\n" %(n["text"], n["page"], n["date"])
				doc += "\n"

			f = open(out + ".txt", 'w+')
			f.write(doc)
			f.close()
		elif type == "docx":
			document = Document()
			document.add_heading('Reading Notes', 0)
			for k,v in notebook.items():
				document.add_heading(k, level=2)
				document.add_heading(v["writer"], level=4)
				for n in v["notes"]:
					t = "%s (on p.%s at %s)\n" %(n["text"], n["page"], n["date"])
					document.add_paragraph(t, style='List Bullet')
			document.save(out + ".docx")

c = Clipper("./Kindle_Clippings_26.09.2019.txt")
nb = c.createNotebook()
# by_writer = c.findNotesByWriter("Jordan")
# by_book = c.findNotesByBook("12")
c.writeNotes(nb, "notebook", "docx")
