import React, { useState } from 'react'
import Controls from './components/Controls'
import GraphView from './components/GraphView'
import CFGView from './components/CFGView'
import './App.css'

function App() {
  const [automataData, setAutomataData] = useState(null)
  const [cfgData, setCfgData] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <header className="bg-white shadow-md">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-800">
            Automata & Compiler Visualizer
          </h1>
          <p className="text-gray-600 mt-2">
            Visualize NFA, DFA, and Context-Free Grammar parsing
          </p>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Controls Panel */}
          <div className="lg:col-span-1">
            <Controls
              setAutomataData={setAutomataData}
              setCfgData={setCfgData}
              setError={setError}
              setLoading={setLoading}
            />
          </div>

          {/* Visualization Panel */}
          <div className="lg:col-span-2">
            {loading && (
              <div className="bg-white rounded-lg shadow-lg p-8 text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
                <p className="mt-4 text-gray-600">Processing...</p>
              </div>
            )}

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
                <p className="text-red-800 font-semibold">Error:</p>
                <p className="text-red-600">{error}</p>
              </div>
            )}

            {automataData && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-bold mb-4 text-gray-800">
                  Automata Visualization
                </h2>
                <GraphView data={automataData} />
              </div>
            )}

            {cfgData && (
              <div className="bg-white rounded-lg shadow-lg p-6 mt-6">
                <h2 className="text-2xl font-bold mb-4 text-gray-800">
                  CFG Analysis
                </h2>
                <CFGView data={cfgData} />
              </div>
            )}

            {!automataData && !cfgData && !loading && !error && (
              <div className="bg-white rounded-lg shadow-lg p-12 text-center">
                <p className="text-gray-500 text-lg">
                  Enter a regular expression, NFA, DFA, or CFG to visualize
                </p>
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="bg-white mt-12 py-6 text-center text-gray-600">
        <p>Automata & Compiler Visualizer © 2024</p>
      </footer>
    </div>
  )
}

export default App

