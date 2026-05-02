import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class OCRAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def extract_fields(self, file_path: str):
        """
        Uploads a PDF to Gemini and extracts invoice details.
        """
        sample_file = genai.upload_file(path=file_path, display_name="Invoice PDF")
        
        prompt = """
        Extract these invoice fields from the document in strict JSON format:
        - Invoice Number
        - Invoice Date
        - Due Date
        - Vendor Name
        - Vendor Address
        - Bill To Name
        - Bill To Address
        - Items (array of objects with description, quantity, unit_price, line_total)
        - Subtotal
        - Tax Amount
        - Total Amount
        - Currency
        - Payment Terms

        If a field is missing, return an empty string for text fields and an empty array for Items.
        Do not use the JSON literal null.
        Return ONLY valid JSON. Do not include any explanation or markdown.
        """
        
        response = self.model.generate_content([sample_file, prompt])
        
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        return text
