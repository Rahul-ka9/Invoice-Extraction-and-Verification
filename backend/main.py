from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import json
import tempfile
from agents.ocr_agent import OCRAgent
from agents.resolution_agent import ResolutionAgent
from agents.mail_agent import MailAgent

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ocr_agent = OCRAgent()
res_agent = ResolutionAgent()
mail_agent = MailAgent()

@app.post("/process-pdf")
async def process_pdf(file: UploadFile = File(...), owner_email: str = Form(None)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        shutil.copyfileobj(file.file, temp_pdf)
        file_path = temp_pdf.name

    owner_email = owner_email or os.getenv("OWNER_EMAIL")
    if not owner_email:
        raise HTTPException(status_code=400, detail="Owner email is required")
    
    try:
        # Step 1: OCR Extraction
        extracted_json_str = await ocr_agent.extract_fields(file_path)
        extracted_data = json.loads(extracted_json_str)
        
        # Step 2: Resolution/Verification
        verification_result = await res_agent.verify_extraction(file_path, extracted_json_str)
        
        # Step 3: Mail Reporting
        email_content = None
        if verification_result["status"] == "mismatch":
            email_content = mail_agent.send_mismatch_report(
                verification_result["extracted_fields"],
                verification_result["corrected_fields"],
                verification_result["reason"],
                verification_result.get("missing_fields", []),
                recipient=owner_email
            )
        else:
            success_email = {
                "to": owner_email,
                "subject": "PDF Extraction Successful",
                "body": f"Fields extracted and verified successfully:\n\n{json.dumps(verification_result['extracted_fields'], indent=2)}"
            }
            mail_agent.send_success_report(verification_result["extracted_fields"], recipient=owner_email)
            email_content = success_email
            
        return {
            "filename": file.filename,
            "extracted": verification_result["extracted_fields"],
            "corrected": verification_result["corrected_fields"],
            "missing_fields": verification_result.get("missing_fields", []),
            "status": verification_result["status"],
            "reason": verification_result.get("reason", ""),
            "mail_sent": True,
            "email_content": email_content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        try:
            os.remove(file_path)
        except Exception:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
