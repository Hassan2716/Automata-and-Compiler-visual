import React, { useMemo } from 'react'

function CFGView({ data }) {
  const parsingTableDisplay = useMemo(() => {
    if (!data?.parsing_table) return null
    
    // Collect all unique terminals from all non-terminals
    const allTerminals = new Set()
    Object.values(data.parsing_table).forEach(terminals => {
      Object.keys(terminals).forEach(terminal => allTerminals.add(terminal))
    })
    const sortedTerminals = Array.from(allTerminals).sort()
    
    return { sortedTerminals }
  }, [data?.parsing_table])

  if (!data) return null

  return (
    <div className="space-y-6">
      {/* FIRST Sets */}
      {data.first_sets && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-semibold text-lg mb-4">FIRST Sets</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(data.first_sets).map(([nonTerminal, firstSet]) => (
              <div key={nonTerminal} className="bg-white p-3 rounded border">
                <span className="font-medium text-indigo-600">FIRST({nonTerminal})</span>
                <span className="ml-2">= {'{'}{Array.from(firstSet).join(', ')}{'}'}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* FOLLOW Sets */}
      {data.follow_sets && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-semibold text-lg mb-4">FOLLOW Sets</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(data.follow_sets).map(([nonTerminal, followSet]) => (
              <div key={nonTerminal} className="bg-white p-3 rounded border">
                <span className="font-medium text-indigo-600">FOLLOW({nonTerminal})</span>
                <span className="ml-2">= {'{'}{Array.from(followSet).join(', ')}{'}'}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Predictive Parsing Table */}
      {data.parsing_table && parsingTableDisplay && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-semibold text-lg mb-4">Predictive Parsing Table</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border border-gray-300">
              <thead>
                <tr className="bg-indigo-100">
                  <th className="px-4 py-2 border border-gray-300 font-semibold">Non-Terminal</th>
                  {parsingTableDisplay.sortedTerminals.map((terminal) => (
                    <th
                      key={terminal}
                      className="px-4 py-2 border border-gray-300 font-semibold"
                    >
                      {terminal}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {Object.entries(data.parsing_table).map(([nonTerminal, terminals]) => (
                  <tr key={nonTerminal}>
                    <td className="px-4 py-2 border border-gray-300 font-medium">
                      {nonTerminal}
                    </td>
                    {parsingTableDisplay.sortedTerminals.map((terminal) => (
                      <td key={terminal} className="px-4 py-2 border border-gray-300">
                        {terminals[terminal]
                          ? Array.isArray(terminals[terminal])
                            ? terminals[terminal].join(' | ')
                            : terminals[terminal]
                          : '-'}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Steps */}
      {data.steps && (
        <div className="bg-blue-50 rounded-lg p-4">
          <h3 className="font-semibold mb-2">Steps:</h3>
          <ul className="list-disc list-inside text-sm">
            {data.steps.map((step, idx) => (
              <li key={idx}>{step}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default CFGView

