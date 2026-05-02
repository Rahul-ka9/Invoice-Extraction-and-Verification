# PDF Field Extractor with AI-Powered OCR

A full-stack application that extracts fields from PDF documents using Google Gemini API, verifies the extracted data, and notifies owners of any mismatches.

## Project Structure

```
Infy/
├── backend/
│   ├── agents/
│   │   ├── ocr_agent.py           # OCR extraction agent
│   │   ├── resolution_agent.py    # Verification/resolution agent
│   │   └── mail_agent.py          # Email notification agent
│   ├── main.py                     # FastAPI application
│   ├── requirements.txt
│   └── .env                        # Environment variables
└── frontend/
    ├── src/
    │   ├── App.jsx                # Main React component
    │   ├── main.jsx               # React entry point
    │   └── index.css              # Styling
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── README.md
```

## Features

### Backend (FastAPI + Python)

1. **OCR Agent** - Extracts fields from PDFs using Google Gemini API
2. **Resolution Agent** - Verifies extracted data and identifies mismatches
3. **Mail Agent** - Sends notifications to document owner
4. **API Endpoint** - `/process-pdf` for document processing

### Frontend (React + Vite)

- Modern, responsive UI with drag-and-drop file upload
- Real-time processing status
- Field comparison view (extracted vs. corrected)
- Download results as JSON
- Error handling and notifications

## Setup Instructions

### Backend Setup

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Configure environment variables in `.env`:
```
GEMINI_API_KEY=your_api_key_here
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
OWNER_EMAIL=owner@example.com
```

3. Run the FastAPI server:
```bash
python main.py
```
The API will be available at `http://localhost:8000`

### Frontend Setup

1. Install Node dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```
The UI will be available at `http://localhost:5173`

3. Build for production:
```bash
npm run build
```

## API Documentation

### POST /process-pdf

Upload a PDF file for processing.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Parameter: `file` (PDF file)


## Workflow

1. User uploads PDF via web UI
2. **OCR Agent** extracts fields using Gemini API
3. **Resolution Agent** verifies the extracted data
4. If mismatch found:
   - Corrected fields are identified
   - **Mail Agent** sends detailed report to owner
5. Results displayed in UI with comparison view

## Environment Variables

- `GEMINI_API_KEY` - Google Gemini API key
- `EMAIL_USER` - Gmail address for sending notifications
- `EMAIL_PASSWORD` - Gmail app-specific password
- `OWNER_EMAIL` - Email address to receive mismatch notifications

## Technology Stack

**Backend:**
- FastAPI - Web framework
- Google Generative AI - OCR/LLM
- Yagmail - Email service
- PyMuPDF - PDF processing

**Frontend:**
- React 18 - UI framework
- Vite - Build tool
- Axios - HTTP client

## Notes

- Requires a valid Google Gemini API key
- Gmail requires app-specific passwords for authentication
- PDFs are temporarily stored in a temporary system file during processing
- CORS is enabled for frontend-backend communication

## License

MIT
