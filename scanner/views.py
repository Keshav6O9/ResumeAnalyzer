from django.shortcuts import render
from .utils import get_gemini_response,input_prompt1,input_prompt3,input_pdf_setup
# Create your views here.

def home(request):
    return render(request,"index.html")

def ShowAnalysis(request):
    if request.method == "POST":
        resume_file = request.FILES['resume']
        jd = request.POST['jd']
        pdf_content = input_pdf_setup(resume_file) 
        response1=get_gemini_response(input_prompt1,pdf_content,jd)
        response2 =get_gemini_response(input_prompt3,pdf_content,jd)
        response = {'percentage':response2,'analysis':response1}
        return render(request,'index.html',response)
    return render(request,'index.html')
