from openai import OpenAI
import PyPDF2 as pdf
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class ResumeAnalyzer:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  

    def extract_text_from_pdf(self, pdf_file):
        """Extract text from a PDF file."""
        try:
            reader = pdf.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF file: {e}")

    def analyze_resume(self, resume_text, job_description):
        """Analyze the resume based on the job description using OpenAI."""
        try:
            prompt = f"""
            You are an ATS system. Analyze this resume and return a JSON object.
            Format your response as a raw JSON object without any additional text or formatting.
            Use exactly this structure:
            {{
                "JD Match": "X%",
                "MissingKeywords": [],
                "Profile Summary": "",
                "Suggestions": []
            }}

            Resume:
            {resume_text}

            Job Description:
            {job_description}
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an ATS system. Respond only with valid JSON."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
                max_tokens=1000,
            )

            content = response.choices[0].message.content.strip()
            
            # Debug logging
            print("Raw API response:", content)
            
            try:
                parsed_json = json.loads(content)
                # Validate required fields
                required_fields = ["JD Match", "MissingKeywords", "Profile Summary", "Suggestions"]
                if all(field in parsed_json for field in required_fields):
                    return parsed_json
                else:
                    raise ValueError("Missing required fields in JSON response")
            except (json.JSONDecodeError, ValueError) as e:
                print(f"JSON parsing error: {str(e)}")
                return {
                    "JD Match": "0%",
                    "MissingKeywords": [],
                    "Profile Summary": "Error: Could not analyze resume",
                    "Suggestions": ["Error processing the resume. Please try again."]
                }
                
        except Exception as e:
            print(f"Analysis error: {str(e)}")
            raise Exception(f"Error analyzing resume: {e}")

# Example usage
if __name__ == "__main__":
    analyzer = ResumeAnalyzer()

    # Load job description and resume
    job_description = """
    We are looking for a software engineer with experience in Python, machine learning, and cloud computing.
    The ideal candidate should have strong problem-solving skills, experience with REST APIs, and familiarity with Docker and Kubernetes.
    """

    resume_path = "path/to/resume.pdf"  # Replace with the actual path to your resume

    try:
        # Extract text from the resume
        with open(resume_path, "rb") as pdf_file:
            resume_text = analyzer.extract_text_from_pdf(pdf_file)

        # Analyze the resume
        result = analyzer.analyze_resume(resume_text, job_description)
        print(result)  # Print the result as a dictionary
    except Exception as e:
        print(f"Error: {e}")