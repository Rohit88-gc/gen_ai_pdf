from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import PyPDF2
from .openai_utils import get_openai_response
import sys

@login_required(login_url='/users/login/')
def upload_pdf(request):
    print("User authenticated in upload_pdf:", request.user.is_authenticated, file=sys.stderr)
    print("Session ID in upload_pdf:", request.session.session_key, file=sys.stderr)
    if request.method == "POST" and request.FILES.get("pdf_file"):
        print("POST received with file", file=sys.stderr)
        pdf_file = request.FILES["pdf_file"]
        with open(f"media/{pdf_file.name}", "wb+") as destination:
            for chunk in pdf_file.chunks():
                destination.write(chunk)
        pdf_reader = PyPDF2.PdfReader(f"media/{pdf_file.name}")
        text = "".join(page.extract_text() for page in pdf_reader.pages)
        request.session["pdf_text"] = text
        request.session.modified = True
        print("Redirecting to /smart_pdf/chat/ with session:", request.session.session_key, file=sys.stderr)
        response = redirect('/smart_pdf/chat/')
        response.set_cookie('sessionid', request.session.session_key, max_age=1209600, httponly=True)
        return response
    return render(request, "smart_pdf_app/home.html")

@login_required(login_url='/users/login/')
def chat(request):
    print("User authenticated in chat:", request.user.is_authenticated, file=sys.stderr)
    print("Session ID in chat:", request.session.session_key, file=sys.stderr)
    print("PDF text in session:", "exists" if "pdf_text" in request.session else "not found", file=sys.stderr)
    response = "Welcome! Ask a question about your PDF to get started."
    question = ""
    if request.method == "POST":
        question = request.POST.get("question", "").strip()
        if question:
            pdf_text = request.session.get("pdf_text", "")
            if pdf_text:
                context = pdf_text
                prompt = f"The following is the complete text from a PDF about networking: {context}. Answer the question '{question}' by rephrasing and explaining the relevant information in a natural, engaging paragraph with smooth transitions and vivid examples. Avoid copying the text verbatim or adding external knowledge."
            else:
                prompt = question
            try:
                raw_response = get_openai_response(prompt)
                response = f"Alright, let’s embark on an epic quest through the digital realm! {raw_response}"
            except Exception as e:
                print("Error in get_openai_response:", e, file=sys.stderr)
                response = "Sorry, I couldn’t process that. Please try again."
        else:
            response = "Whoa, throw me a question to kick off this adventure! 🔍"
    return render(request, "smart_pdf_app/chat1.html", {"response": response, "question": question})