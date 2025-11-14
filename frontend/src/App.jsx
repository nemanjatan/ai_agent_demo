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
                <li><strong>Title:</strong> {result.analysis.title || result.analysis.Title || 'Not extracted'}</li>
                <li><strong>Links Found:</strong> {result.analysis.links_count || result.analysis.linksCount || result.analysis['links_count'] || 'Not extracted'}</li>
                <li><strong>Has Navigation:</strong> {
                  result.analysis.has_navigation !== undefined ? (result.analysis.has_navigation ? 'Yes' : 'No') :
                  result.analysis.hasNavigation !== undefined ? (result.analysis.hasNavigation ? 'Yes' : 'No') :
                  result.analysis['has_navigation'] !== undefined ? (result.analysis['has_navigation'] ? 'Yes' : 'No') :
                  'Not extracted'
                }</li>
                <li><strong>Has Main Content:</strong> {
                  result.analysis.has_main_content !== undefined ? (result.analysis.has_main_content ? 'Yes' : 'No') :
                  result.analysis.hasMainContent !== undefined ? (result.analysis.hasMainContent ? 'Yes' : 'No') :
                  result.analysis['has_main_content'] !== undefined ? (result.analysis['has_main_content'] ? 'Yes' : 'No') :
                  'Not extracted'
                }</li>
                <li><strong>Page Type:</strong> {result.analysis.page_type || result.analysis.pageType || result.analysis['page_type'] || 'Not extracted'}</li>
              </ul>
              {/* Debug info - remove in production */}
              {process.env.NODE_ENV === 'development' && (
                <details style={{ marginTop: '1rem', fontSize: '0.8rem', color: '#666' }}>
                  <summary>Debug: Raw analysis data</summary>
                  <pre style={{ background: '#f5f5f5', padding: '0.5rem', borderRadius: '4px', overflow: 'auto' }}>
                    {JSON.stringify(result.analysis, null, 2)}
                  </pre>
                </details>
              )}
            </div>
          )}

          {result.patterns && result.patterns.length > 0 && (
            <div className="patterns">
              <h2 style={{ marginBottom: '1rem', color: '#333' }}>
                🎯 Generated Behavior Patterns
              </h2>
              {result.patterns.map((pattern, index) => (
                <div key={index} className="pattern" style={{ 
                  marginBottom: '2rem', 
                  padding: '1.5rem', 
                  backgroundColor: '#f9f9f9', 
                  borderRadius: '8px',
                  border: '1px solid #e0e0e0'
                }}>
                  <h3 style={{ 
                    marginBottom: '1rem', 
                    color: '#2c3e50',
                    fontSize: '1.2rem',
                    fontWeight: '600'
                  }}>
                    Pattern {pattern.number || index + 1}: {pattern.title || `Pattern ${index + 1}`}
                  </h3>
                  {pattern.steps && pattern.steps.length > 0 ? (
                    <div className="pattern-sequence" style={{ whiteSpace: 'pre-wrap' }}>
                      <div style={{ marginBottom: '1rem' }}>
                        <strong style={{ color: '#555', display: 'block', marginBottom: '0.5rem' }}>Steps:</strong>
                        {pattern.steps.map((step, stepIndex) => (
                          <div key={stepIndex} style={{ 
                            marginBottom: '0.75rem', 
                            paddingLeft: '1rem',
                            padding: '0.5rem',
                            backgroundColor: '#fff',
                            borderRadius: '4px',
                            borderLeft: '3px solid #4a90e2'
                          }}>
                            {step}
                          </div>
                        ))}
                      </div>
                      {pattern.expected_outcome && (
                        <div style={{ 
                          marginTop: '1rem',
                          padding: '0.75rem',
                          backgroundColor: '#e8f5e9',
                          borderRadius: '4px',
                          borderLeft: '3px solid #4caf50'
                        }}>
                          <strong style={{ color: '#2e7d32' }}>Expected Outcome:</strong>
                          <div style={{ marginTop: '0.25rem', color: '#1b5e20' }}>
                            {pattern.expected_outcome}
                          </div>
                        </div>
                      )}
                    </div>
                  ) : pattern.description ? (
                    <div className="pattern-sequence" style={{ whiteSpace: 'pre-wrap' }}>
                      {pattern.description}
                    </div>
                  ) : null}
                </div>
              ))}
            </div>
          )}

          {result.full_response && (
            <div className="pattern" style={{ marginTop: '2rem' }}>
              <h3>📝 Full Agent Response</h3>
              <div 
                className="pattern-sequence" 
                style={{ 
                  whiteSpace: 'pre-wrap', 
                  maxHeight: '600px', 
                  overflow: 'auto',
                  backgroundColor: '#f9f9f9',
                  padding: '1rem',
                  borderRadius: '4px',
                  border: '1px solid #e0e0e0',
                  fontFamily: 'monospace',
                  fontSize: '0.9rem',
                  lineHeight: '1.5'
                }}
              >
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
