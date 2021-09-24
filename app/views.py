from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.core.files.images import ImageFile
from PyPDF2 import PdfFileWriter, PdfFileReader
from pdf2image import convert_from_path
import os
from .models import *
import shutil
from PIL import ImageFile
import pytesseract
import cv2
import re
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


poppler_path = r"C:\Program Files\poppler-0.68.0\bin"

# Create your views here.
def index(request):
    if request.method == 'POST':
        pdfs = request.FILES.getlist('pdf')
        print(pdfs)
        for pdf in pdfs:
            file = Files.objects.create(user=request.user, pdf=pdf)
            file.save()
            pdftoimages(file)
            try:
                shutil.rmtree("imag/")
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

        return redirect('mybooks')
    else:
        return render(request, "app/index.html")

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password = password)
        if user is not None:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
        else:
            return redirect('login')
    else:
        return render(request, "app/login.html")

def signup(request):
    if request.method == 'POST':
        # username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1'] == request.POST['password2']
        if password:
            user = User.objects.create_user(username = email, email=email, password=request.POST['password1'])
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
        else:
            return redirect('signup')
    return render(request, "app/signup.html")

def logout(request):
    auth.logout(request)
    return redirect('/')

def mybooks(request):
    if request.user.is_authenticated:
        # print(request.user.id)
        pdfs = Files.objects.filter(user_id=request.user.id)
        # print(pdfs)
        # for i in pdfs:
        #     print(i.id)
        return render(request, "app/mybooks.html",{
            "pdfs": pdfs,
        })
    else:
        return redirect('login')

def profile(request):
    return render(request, "app/profile.html")

def edit(request, id, page):
    img = Image.objects.filter(pdf_id = id)        
    
    if request.method == 'POST':
        text = request.POST['editor1']
        txt = Text.objects.get(image_id = img[page-1].id)
        txt.text = text
        txt.save()
        
    text = Text.objects.get(image_id = img[page-1].id)  
    
    texts = text.text.split("\n\n")

    with open('D:\python_work\Django\gronthon\media\BengaliWordList_40.txt', encoding="utf8") as f:
        lines = [line.rstrip() for line in f]        
    
    return render(request, "app/edit.html", {
        "texts": texts,
        "id":id,        
        "page":page,
        "previous": page-1,
        "next": page+1,
        "image": text.image,
    })

def pdftoimages(pdf):
    pages = convert_from_path(pdf.pdf.path)
    
    print("this ", pdf)

    ouotputDir = "imag/"
    if not os.path.exists(ouotputDir):
            os.makedirs(ouotputDir)

    inputpdf = PdfFileReader(open(pdf.pdf.path, "rb"))
    
    save_path = 'imag'

    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        file_name = "document-page%s.pdf" % i
        completeName = os.path.join(save_path, file_name)
        with open(completeName, "wb") as outputStream:
            output.write(outputStream)
    c = 0
    for i in range(inputpdf.numPages):
        file = "imag/document-page%s.pdf" % i
        c = c + 1
        convert(file, ouotputDir, c, pdf)

def convert(file, ouotputDir, c, pdf):
        if not os.path.exists(ouotputDir):
            os.makedirs(ouotputDir)
        pages = convert_from_path(file)
        ouotputDir = "media/pics/"        
        for page in pages:
            myfile = str(pdf) + str(c) + '.jpg'  
            page.save("media/"+myfile, 'JPEG')
            print("my ", myfile)            
            i = Image.objects.create(pdf=pdf)
            i.image = myfile
            i.save()
            ImageToText("media/"+myfile, i)

def ImageToText(img, i):
    # print(img)   
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    img = cv2.imread(img)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    text = pytesseract.image_to_string(img_rgb, lang='ben')
    # text = text.split("\n")


    t = Text.objects.create(image=i)
    t.text = text
    t.save()
    # print(text)            


def download(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    pages = Image.objects.filter(pdf_id = 163)
    for page in pages:
        text = Text.objects.filter(image_id=page.id)
        print(text[0].text)

        p.drawString(100, 100, text[0].text)

    # Close the PDF object cleanly, and we're done.
    # p.showPage()
    # p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

def epudownload(requset, id):
    pages = Image.objects.filter(pdf_id = id)
    for page in pages:
        text = Text.objects.filter(image_id = page)
        print(text[0].text)
    
    
    # def ConvertRtfToDocx(rootDir, file):
    # word = win32com.client.Dispatch("Word.Application")
    # wdFormatDocumentDefault = 16
    # wdHeaderFooterPrimary = 1
    # doc = word.Documents.Open(rootDir + "\\" + file)
    # for pic in doc.InlineShapes:
    #     pic.LinkFormat.SavePictureWithDocument = True
    # for hPic in doc.sections(1).headers(wdHeaderFooterPrimary).Range.InlineShapes:
    #     hPic.LinkFormat.SavePictureWithDocument = True
    # doc.SaveAs(str(rootDir + "\\refman.docx"), FileFormat=wdFormatDocumentDefault)
    # doc.Close()
    # word.Quit()

    return redirect('mybooks')