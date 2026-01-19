from org.apache.pdfbox.Loader import loadPDF
from org.apache.pdfbox.text import PDFTextStripper

def getText(fileName, pdfBytes):
	"""Grab all of the text from the PDF
	
	Args:
	    fileName (str): The name of the PDF document
	    pdfBytes (str): Byte representation of PDF
	
	Returns:
	    List: List of page objects with page number and page text
	"""
	doc = loadPDF(pdfBytes)
	try:
		stripper = PDFTextStripper()
		pages = []

		for pageNum in range(1, doc.getNumberOfPages() + 1):
			stripper.setStartPage(pageNum)
			stripper.setEndPage(pageNum)

			text = stripper.getText(doc).strip()
			pages.append({
				"page": pageNum,
				"text": text
			})

		return pages
	finally:
		doc.close()