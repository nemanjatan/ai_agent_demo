import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [url, setUrl] = useState('https://metro-manhattan.com')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  const handleAnalyze = async () => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      // Use environment variable or default to localhost
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await axios.post(`${apiUrl}/api/analyze`, {
        url: url
      })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <div className="header">
        <h1>🤖 AI Agent Browser Automation</h1>
        <p>Analyze websites and generate realistic user behavior patterns</p>
      </div>

      <div className="form-section">
        <div className="form-group">
          <label htmlFor="url">Website URL</label>
          <input
            type="text"
            id="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            disabled={loading}
          />
        </div>
        <button
          className="button"
          onClick={handleAnalyze}
          disabled={loading || !url}
        >
          {loading ? 'Analyzing...' : 'Analyze Website'}
        </button>
      </div>

      {error && (
        <div className="error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {loading && (
        <div className="loading">
          <p>🔄 Agent is analyzing the website...</p>
          <p style={{ fontSize: '0.9rem', marginTop: '0.5rem', opacity: 0.7 }}>
            This may take 30-60 seconds
          </p>
        </div>
      )}

      {result && (
        <div className="results-section">
          {result.analysis && (
            <div className="analysis-info">
              <h3>📊 Page Analysis</h3>
              <ul>
                <li><strong>Title:</strong> {result.analysis.title || 'Not extracted'}</li>
                <li><strong>Links Found:</strong> {result.analysis.links_count || 'Not extracted'}</li>
                <li><strong>Has Navigation:</strong> {result.analysis.has_navigation !== undefined ? (result.analysis.has_navigation ? 'Yes' : 'No') : 'Not extracted'}</li>
                <li><strong>Has Main Content:</strong> {result.analysis.has_main_content !== undefined ? (result.analysis.has_main_content ? 'Yes' : 'No') : 'Not extracted'}</li>
                <li><strong>Page Type:</strong> {result.analysis.page_type || 'Not extracted'}</li>
              </ul>
            </div>
          )}

          {result.patterns && result.patterns.length > 0 && (
            <div className="patterns">
              <h2 style={{ marginBottom: '1rem', color: '#333' }}>
                🎯 Generated Behavior Patterns
              </h2>
              {result.patterns.map((pattern, index) => (
                <div key={index} className="pattern">
                  <h3>Pattern {pattern.number || index + 1}: {pattern.title || `Pattern ${index + 1}`}</h3>
                  {pattern.description && (
                    <div className="pattern-sequence" style={{ whiteSpace: 'pre-wrap' }}>
                      {pattern.description}
                    </div>
                  )}
                  {!pattern.description && (
                    <div className="pattern-sequence">
                      {JSON.stringify(pattern, null, 2)}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {result.full_response && (
            <div className="pattern" style={{ marginTop: '2rem' }}>
              <h3>Full Agent Response</h3>
              <div className="pattern-sequence" style={{ whiteSpace: 'pre-wrap' }}>
                {result.full_response}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default App
