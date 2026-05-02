import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class ResolutionAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def verify_extraction(self, file_path: str, extracted_data_str: str):
        """
        Verifies if the extracted invoice fields match the PDF document.
        """
        extracted_data = json.loads(extracted_data_str)
        required_fields = [
            "Invoice Number",
            "Invoice Date",
            "Due Date",
            "Currency",
            "Payment Terms",
            "Vendor Name",
            "Vendor Address",
            "Bill To Name",
            "Bill To Address",
            "Subtotal",
            "Tax Amount",
            "Total Amount",
            "Items"
        ]

        def is_missing(value):
            return value is None or value == "" or value == []

        local_missing_fields = [key for key in required_fields if is_missing(extracted_data.get(key))]

        sample_file = genai.upload_file(path=file_path, display_name="Verification PDF")
        
        prompt = f"""
        A previous OCR extraction produced these invoice fields:
        {extracted_data_str}

        Compare these extracted values against the PDF document exactly.
        Additionally, validate the data for consistency:
        - Check if subtotal + tax = total amount
        - Ensure all calculations are mathematically correct
        - Verify that quantities and prices make sense
        - Detect any missing required fields from the extraction

        If every field is correct, present, and the data is consistent, return status "correct" and set corrected_fields equal to extracted_fields.
        If any value is wrong, missing, or inconsistent, return status "mismatch" and provide corrected_fields with the accurate values.
        If any required field is missing in the extraction, include it in missing_fields.

        Output ONLY a JSON object with the following structure:
        {{
            "status": "correct" | "mismatch",
            "extracted_fields": {{ ...original fields... }},
            "corrected_fields": {{ ...corrected fields... }},
            "missing_fields": ["field1", "field2", ...],
            "reason": "clear explanation of any mismatch or inconsistency"
        }}
        """
        
        response = self.model.generate_content([sample_file, prompt])
        
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        response_data = json.loads(text)
        response_missing = response_data.get("missing_fields") or []
        combined_missing = sorted(set(response_missing + local_missing_fields))

        if combined_missing:
            response_data["missing_fields"] = combined_missing
            response_data["status"] = "mismatch"
            if response_data.get("reason"):
                if "missing" not in response_data["reason"].lower():
                    response_data["reason"] += "; missing required fields detected."
            else:
                response_data["reason"] = "Missing required fields detected."

        response_data["extracted_fields"] = response_data.get("extracted_fields", extracted_data)
        response_data["corrected_fields"] = response_data.get("corrected_fields", response_data["extracted_fields"])
        response_data["missing_fields"] = response_data.get("missing_fields", [])

        return response_data
