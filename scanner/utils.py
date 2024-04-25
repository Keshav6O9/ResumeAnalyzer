import base64
import io
import os
import google.generativeai as genai

import pdf2image



genai.configure(api_key="")
def get_gemini_response(input,pdf_content,prompt):
    llm = genai.GenerativeModel('gemini-pro-vision')
    response=llm.generate_content([input,pdf_content[0],prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read(),poppler_path="./poppler-24.02.0/Library/bin")

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role by comparing skills.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
In the resume, look for the following information:
- Relevant Skills:
- Company Name of Applicant:
- Job Title of Applicant:
- Job Description provided:
Remember to assess how well the candidate's skills match the job requirements and provide insightful feedback on their strengths and areas of improvement in relation to the job description.
For example, when evaluating a candidate's resume for a technical role, pay attention to whether their skills in programming languages align with the job's requirements. Mention specific instances where their experience directly relates to the job duties to provide a well-rounded assessment.
 
assessment : 
"""

input_prompt3 = """
You are an experienced ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. Your task is to evaluate the resume against the provided job description, giving the percentage of match if the resume aligns with the job requirements.
Starting with the percentage match, analyze the resume for key terms and qualifications mentioned in the job description. Provide a numerical value representing the percentage of alignment between the resume and the job requirements.
Next, identify keywords or phrases that are missing in the resume but are essential for the job role. Highlight these missing elements to help the candidate understand where they need to focus on improving their resume.
Conclude with your final thoughts on the overall fit of the candidate's resume with the job description. Offer constructive feedback or suggestions on how the candidate can enhance their resume to better align with the job requirements.
Example:
Percentage Match: 
Keywords Missing: 
Final Thoughts: 

"""
