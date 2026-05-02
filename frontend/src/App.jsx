import { useState, useRef } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [ownerEmail, setOwnerEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [notification, setNotification] = useState(null)
  const fileInputRef = useRef(null)

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 5000)
  }

  const handleEmailChange = (e) => {
    setOwnerEmail(e.target.value)
  }

  const handleFileSelect = (e) => {
    const file = e.target.files?.[0]
    if (file) {
      if (file.type === 'application/pdf') {
        setSelectedFile(file)
        setError(null)
      } else {
        setError('Please select a PDF file')
        showNotification('Only PDF files are allowed', 'error')
      }
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    e.currentTarget.classList.add('active')
  }

  const handleDragLeave = (e) => {
    e.currentTarget.classList.remove('active')
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.currentTarget.classList.remove('active')
    const file = e.dataTransfer.files?.[0]
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file)
      setError(null)
    } else {
      setError('Please drop a PDF file')
      showNotification('Only PDF files are allowed', 'error')
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first')
      return
    }

    if (!ownerEmail || !ownerEmail.includes('@')) {
      setError('Please enter a valid owner email address')
      return
    }

    setLoading(true)
    setError(null)
    const formData = new FormData()
    formData.append('file', selectedFile)
    formData.append('owner_email', ownerEmail)

    try {
      const response = await axios.post('/api/process-pdf', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setResults(response.data)
      showNotification('PDF processed successfully!', 'success')
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to process PDF'
      setError(errorMsg)
      showNotification(errorMsg, 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setSelectedFile(null)
    setResults(null)
    setError(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  return (
    <div className="container">
      <div className="header">
        <h1>📄 PDF Field Extractor</h1>
        <p>Extract and verify document fields with AI-powered OCR</p>
      </div>

      <div className="content">
        {notification && (
          <div className={`notification ${notification.type}`}>
            {notification.message}
          </div>
        )}

        {error && <div className="error-message">{error}</div>}

        {!results ? (
          <>
            <div
              className="upload-section"
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <div className="upload-icon">📁</div>
              <h3>Upload PDF Document</h3>
              <p>Drag and drop your PDF here or click to select</p>
              {selectedFile && (
                <p style={{ color: '#28a745', fontWeight: 'bold' }}>
                  ✓ {selectedFile.name}
                </p>
              )}
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                onChange={handleFileSelect}
              />
            </div>

            <div style={{ marginBottom: '20px', textAlign: 'center' }}>
              <label style={{ display: 'block', marginBottom: '8px', color: '#333' }}>
                Owner Email for notification
              </label>
              <input
                type="email"
                value={ownerEmail}
                onChange={handleEmailChange}
                placeholder="owner@example.com"
                style={{
                  width: '100%',
                  maxWidth: '420px',
                  padding: '12px 14px',
                  borderRadius: '8px',
                  border: '1px solid #ccc',
                  fontSize: '1rem'
                }}
              />
            </div>

            <div style={{ textAlign: 'center' }}>
              <button
                className="btn btn-primary"
                onClick={handleUpload}
                disabled={!selectedFile || loading}
              >
                {loading ? (
                  <>
                    <span className="spinner" style={{ display: 'inline-block', width: '20px', height: '20px', marginRight: '10px' }}></span>
                    Processing...
                  </>
                ) : (
                  '🚀 Process PDF'
                )}
              </button>
            </div>
          </>
        ) : (
          <div className="results-section">
            <div className="file-info">
              <p>
                <strong>File:</strong> {results.filename}
              </p>
              <p>
                <strong>Status:</strong>{' '}
                {results.status === 'correct' ? (
                  <span style={{ color: '#28a745' }}>✓ Fields Verified</span>
                ) : (
                  <span style={{ color: '#dc3545' }}>⚠ Mismatch Detected</span>
                )}
              </p>
            </div>

            <div className={`result-status ${results.status}`}>
              <span className="status-icon">
                {results.status === 'correct' ? '✓' : '⚠'}
              </span>
              <span>
                {results.status === 'correct'
                  ? 'All fields extracted and verified successfully'
                  : 'Mismatch detected - corrected fields provided'}
              </span>
            </div>

            {results.status === 'mismatch' && (
              <>
                {results.reason && (
                  <div className="mismatch-reason">
                    <strong>Reason for Mismatch:</strong>
                    {results.reason}
                  </div>
                )}
                {results.missing_fields?.length > 0 && (
                  <div className="missing-fields">
                    <strong>Missing Fields:</strong>
                    <ul>
                      {results.missing_fields.map((field) => (
                        <li key={field}>{field}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </>
            )}

            <div className="field-comparison">
              <div className="field-group">
                <h4>Extracted Fields</h4>
                {Object.entries(results.extracted || {}).map(([key, value]) => (
                  <div key={key}>
                    <div className="field-label">{key}</div>
                    <div className="field-value">
                      {typeof value === 'object' ? (
                        <pre style={{ fontSize: '0.8em', margin: 0, whiteSpace: 'pre-wrap' }}>
                          {JSON.stringify(value, null, 2)}
                        </pre>
                      ) : (
                        value || 'N/A'
                      )}
                    </div>
                  </div>
                ))}
              </div>

              {results.status === 'mismatch' && (
                <div className="field-group">
                  <h4>Corrected Fields</h4>
                  {Object.entries(results.corrected || {}).map(([key, value]) => (
                    <div key={key}>
                      <div className="field-label">{key}</div>
                      <div className="field-value" style={{ background: '#d4edda' }}>
                        {typeof value === 'object' ? (
                          <pre style={{ fontSize: '0.8em', margin: 0, whiteSpace: 'pre-wrap' }}>
                            {JSON.stringify(value, null, 2)}
                          </pre>
                        ) : (
                          value || 'N/A'
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {results.mail_sent && (
              <div style={{ marginTop: '30px', padding: '20px', background: '#e8f4f8', borderRadius: '8px', border: '2px solid #0084ff' }}>
                <h3 style={{ marginTop: 0, color: '#0084ff' }}>📧 Email Notification</h3>
                <div style={{ background: 'white', padding: '15px', borderRadius: '6px', marginBottom: '15px', fontFamily: 'monospace', fontSize: '0.9em' }}>
                  <p><strong>To:</strong> {results.email_content?.to}</p>
                  <p><strong>Subject:</strong> {results.email_content?.subject}</p>
                  <div style={{ borderTop: '1px solid #ddd', paddingTop: '15px', marginTop: '15px', whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
                    {results.email_content?.body}
                  </div>
                </div>
              </div>
            )}

            <div className="action-buttons">
              <button
                className="btn btn-primary"
                onClick={handleReset}
              >
                Process Another PDF
              </button>
              <button
                className="btn btn-secondary"
                onClick={() => {
                  const dataStr = JSON.stringify(results, null, 2)
                  const element = document.createElement('a')
                  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(dataStr))
                  element.setAttribute('download', `extraction_results.json`)
                  element.style.display = 'none'
                  document.body.appendChild(element)
                  element.click()
                  document.body.removeChild(element)
                }}
              >
                Download Results
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
