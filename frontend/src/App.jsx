// App.jsx
import { useState, useEffect } from 'react';
import './App.css'


function App() {
  const [runs, setRuns] = useState([]);
  const [selectedRun, setSelectedRun] = useState(null);
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch all runs on component mount
  useEffect(() => {
    fetchRuns();
  }, []);

  const fetchRuns = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/runs');
      const data = await response.json();
      setRuns(data);
    } catch (err) {
      setError('Failed to fetch runs');
      console.error(err);
    }
  };

  // Handle run selection
  const handleRunClick = async (run) => {
    setSelectedRun(run);
    setLoading(true);
    setError(null);
    
    try {
      // Fetch metrics for this run
      const response = await fetch(`http://localhost:8000/api/runs/${run.id}/metrics`);
      const data = await response.json();
      setMetrics(data);
    } catch (err) {
      setError('Failed to fetch metrics');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      {/* Title Bar */}
      <header className="title-bar">
        <h1>Photon</h1>
        <div className="title-bar-actions">
          <span>{runs.length} runs in database</span>
          <button onClick={fetchRuns}>Refresh</button>
        </div>
      </header>
      
      {/* Main Layout */}
      <div className="content-area">
        {/* Sidebar */}
        <aside className="sidebar">
          <div className="sidebar-header">
            <h2>Experiments</h2>
          </div>
          
          <div className="runs-list">
            {runs.length === 0 ? (
              <p className="no-runs">No runs yet</p>
            ) : (
              runs.map(run => (
                <div 
                  key={run.id}
                  className={`run-card ${selectedRun?.id === run.id ? 'selected' : ''}`}
                  onClick={() => handleRunClick(run)}
                >
                  <div className="run-name">{run.name}</div>
                  <div className="run-info">
                    <span className="run-project">📁 {run.project}</span>
                    <span className="run-status">{run.status}</span>
                  </div>
                  <div className="run-time">
                    {new Date(run.created_at).toLocaleDateString()}
                  </div>
                </div>
              ))
            )}
          </div>
        </aside>
        
        {/* Main Content */}
        <main className="main-content">
          {!selectedRun ? (
            <div className="empty-state">
              <h2>No Run Selected</h2>
              <p>Select a run from the sidebar to view its metrics</p>
            </div>
          ) : loading ? (
            <div className="loading-state">
              <p>Loading metrics...</p>
            </div>
          ) : error ? (
            <div className="error-state">
              <p>Error: {error}</p>
            </div>
          ) : (
            <div className="run-details">
              <div className="run-header">
                <h2>{selectedRun.name}</h2>
                <div className="run-metadata">
                  <span>Run ID: #{selectedRun.id}</span>
                  <span>Project: {selectedRun.project}</span>
                  <span>Status: {selectedRun.status}</span>
                </div>
              </div>
              
              <div className="metrics-section">
                <h3>Metrics ({metrics.length} steps)</h3>
                
                {metrics.length === 0 ? (
                  <p>No metrics logged for this run</p>
                ) : (
                  <div className="metrics-display">
                    {/* Summary of latest metrics */}
                    {metrics.length > 0 && (
                      <div className="latest-metrics">
                        <h4>Latest Values (Step {metrics[metrics.length - 1]?.step})</h4>
                        <div className="metric-cards">
                          {Object.entries(metrics[metrics.length - 1]?.metrics || {}).map(([key, value]) => (
                            <div key={key} className="metric-card">
                              <div className="metric-name">{key}</div>
                              <div className="metric-value">
                                {typeof value === 'number' ? value.toFixed(4) : value}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    {/* Table of all metrics */}
                    <div className="metrics-table-container">
                      <h4>All Metrics</h4>
                      <table className="metrics-table">
                        <thead>
                          <tr>
                            <th>Step</th>
                            {metrics.length > 0 && Object.keys(metrics[0].metrics).map(key => (
                              <th key={key}>{key}</th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {metrics.map((metric, idx) => (
                            <tr key={idx}>
                              <td>{metric.step}</td>
                              {Object.values(metric.metrics).map((value, i) => (
                                <td key={i}>
                                  {typeof value === 'number' ? value.toFixed(4) : value}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;