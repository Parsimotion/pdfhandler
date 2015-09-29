"""
Routes and views for the flask application.
"""

from FlaskWebProject import app
from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
from flask import Flask, send_file, request
from StringIO import StringIO
from urllib2 import Request, urlopen

class PdfRetriever:
    def get(self, url):
        remoteFile = urlopen(Request(url)).read()
        memoryFile = StringIO(remoteFile)
        return PdfFileReader(memoryFile)

@app.route("/merge")
def merge():
    urls = request.args.get('urls').split(",")

    merger = PdfFileMerger()
    pdfRetriever = PdfRetriever()

    for url in urls:
        pdfFile = pdfRetriever.get(url)
        merger.append(pdfFile)

    strIO = StringIO()
    merger.write(strIO)
    strIO.seek(0)
    return send_file(strIO, attachment_filename="download.pdf", as_attachment=False)