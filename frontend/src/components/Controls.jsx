import React, { useState } from 'react'
import {
  regexToNFA,
  nfaToDFA,
  minimizeDFA,
  cfgFirstFollow,
  cfgPredictiveTable,
} from '../api'

function Controls({ setAutomataData, setCfgData, setError, setLoading }) {
  const [activeTab, setActiveTab] = useState('regex')
  const [regex, setRegex] = useState('')
  const [nfaInput, setNfaInput] = useState({
    states: 'q0,q1,q2',
    alphabet: 'a,b',
    start_state: 'q0',
    accept_states: 'q2',
    transitions: 'q0:a->q1;q1:b->q2',
  })
  const [dfaInput, setDfaInput] = useState({
    states: 'q0,q1,q2',
    alphabet: 'a,b',
    start_state: 'q0',
    accept_states: 'q2',
    transitions: 'q0:a->q1;q1:b->q2',
  })
  const [cfgInput, setCfgInput] = useState({
    productions: 'S:aSb|ab',
  })

  const handleRegexSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setAutomataData(null)

    try {
      const result = await regexToNFA(regex)
      setAutomataData(result)
    } catch (err) {
      const errorMsg = err.response?.data?.message || err.message || 'Error processing regex'
      if (errorMsg.includes('Cannot connect') || errorMsg.includes('Network Error')) {
        setError('Cannot connect to backend server. Please make sure the backend is running on http://localhost:8000')
      } else {
        setError(errorMsg)
      }
    } finally {
      setLoading(false)
    }
  }

  const handleNFAToDFA = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setAutomataData(null)

    try {
      // Parse NFA input
      const states = nfaInput.states.split(',').map((s) => s.trim())
      const alphabet = nfaInput.alphabet.split(',').map((s) => s.trim())
      const transitions = parseTransitions(nfaInput.transitions, true)

      const nfaData = {
        states,
        alphabet,
        start_state: nfaInput.start_state.trim(),
        accept_states: nfaInput.accept_states.split(',').map((s) => s.trim()),
        transitions,
      }

      const result = await nfaToDFA(nfaData)
      setAutomataData(result)
    } catch (err) {
      const errorMsg = err.response?.data?.message || err.message || 'Error converting NFA to DFA'
      if (errorMsg.includes('Cannot connect') || errorMsg.includes('Network Error')) {
        setError('Cannot connect to backend server. Please make sure the backend is running on http://localhost:8000')
      } else {
        setError(errorMsg)
      }
    } finally {
      setLoading(false)
    }
  }

  const handleMinimizeDFA = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setAutomataData(null)

    try {
      // Parse DFA input
      const states = dfaInput.states.split(',').map((s) => s.trim())
      const alphabet = dfaInput.alphabet.split(',').map((s) => s.trim())
      const transitions = parseTransitions(dfaInput.transitions, false)

      const dfaData = {
        states,
        alphabet,
        start_state: dfaInput.start_state.trim(),
        accept_states: dfaInput.accept_states.split(',').map((s) => s.trim()),
        transitions,
      }

      const result = await minimizeDFA(dfaData)
      setAutomataData(result)
    } catch (err) {
      const errorMsg = err.response?.data?.message || err.message || 'Error minimizing DFA'
      if (errorMsg.includes('Cannot connect') || errorMsg.includes('Network Error')) {
        setError('Cannot connect to backend server. Please make sure the backend is running on http://localhost:8000')
      } else {
        setError(errorMsg)
      }
    } finally {
      setLoading(false)
    }
  }

  const handleCFGSubmit = async (type) => {
    setLoading(true)
    setError(null)
    setCfgData(null)

    try {
      // Parse CFG productions: "S:aSb|ab,A:aA|ε"
      const productions = {}
      const lines = cfgInput.productions.split(',')
      for (const line of lines) {
        const trimmedLine = line.trim()
        if (!trimmedLine) continue
        const [lhs, rhs] = trimmedLine.split(':')
        if (lhs && rhs) {
          productions[lhs.trim()] = rhs.split('|').map((r) => r.trim()).filter((r) => r)
        }
      }

      // Validate that we have at least one production
      if (Object.keys(productions).length === 0) {
        setError('Please enter valid productions. Format: S:aSb|ab')
        setLoading(false)
        return
      }

      let result
      if (type === 'first-follow') {
        result = await cfgFirstFollow(productions)
      } else {
        result = await cfgPredictiveTable(productions)
      }
      setCfgData(result)
    } catch (err) {
      const errorMsg = err.response?.data?.message || err.message || 'Error processing CFG'
      if (errorMsg.includes('Cannot connect') || errorMsg.includes('Network Error')) {
        setError('Cannot connect to backend server. Please make sure the backend is running on http://localhost:8000')
      } else {
        setError(errorMsg)
      }
    } finally {
      setLoading(false)
    }
  }

  const parseTransitions = (transStr, isNFA) => {
    const transitions = {}
    const transList = transStr.split(';')

    for (const trans of transList) {
      const parts = trans.split('->')
      if (parts.length === 2) {
        const [from_symbol, toStatesStr] = parts
        const [fromState, symbol] = from_symbol.split(':')
        const toStates = toStatesStr.split(',').map((s) => s.trim())

        if (!transitions[fromState.trim()]) {
          transitions[fromState.trim()] = {}
        }
        if (isNFA) {
          transitions[fromState.trim()][symbol.trim()] = toStates
        } else {
          // DFA: only one state
          transitions[fromState.trim()][symbol.trim()] = toStates[0]
        }
      }
    }

    return transitions
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="mb-4 border-b border-gray-200">
        <nav className="flex space-x-2">
          {['regex', 'nfa', 'dfa', 'cfg'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 font-medium text-sm rounded-t-lg ${
                activeTab === tab
                  ? 'bg-indigo-600 text-white'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              {tab.toUpperCase()}
            </button>
          ))}
        </nav>
      </div>

      {/* Regex Tab */}
      {activeTab === 'regex' && (
        <form onSubmit={handleRegexSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Regular Expression
            </label>
            <input
              type="text"
              value={regex}
              onChange={(e) => setRegex(e.target.value)}
              placeholder="e.g., (a|b)*ab"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
            <p className="text-xs text-gray-500 mt-1">
              Supports: *, |, concatenation, parentheses
            </p>
          </div>
          <button
            type="submit"
            className="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Convert to NFA
          </button>
        </form>
      )}

      {/* NFA to DFA Tab */}
      {activeTab === 'nfa' && (
        <form onSubmit={handleNFAToDFA} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              States (comma-separated)
            </label>
            <input
              type="text"
              value={nfaInput.states}
              onChange={(e) => setNfaInput({ ...nfaInput, states: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Alphabet (comma-separated)
            </label>
            <input
              type="text"
              value={nfaInput.alphabet}
              onChange={(e) => setNfaInput({ ...nfaInput, alphabet: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Start State
            </label>
            <input
              type="text"
              value={nfaInput.start_state}
              onChange={(e) => setNfaInput({ ...nfaInput, start_state: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Accept States (comma-separated)
            </label>
            <input
              type="text"
              value={nfaInput.accept_states}
              onChange={(e) => setNfaInput({ ...nfaInput, accept_states: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Transitions (format: q0:a{'>'}q1;q1:b{'>'}q2)
            </label>
            <input
              type="text"
              value={nfaInput.transitions}
              onChange={(e) => setNfaInput({ ...nfaInput, transitions: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700"
          >
            Convert to DFA
          </button>
        </form>
      )}

      {/* DFA Minimize Tab */}
      {activeTab === 'dfa' && (
        <form onSubmit={handleMinimizeDFA} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              States (comma-separated)
            </label>
            <input
              type="text"
              value={dfaInput.states}
              onChange={(e) => setDfaInput({ ...dfaInput, states: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Alphabet (comma-separated)
            </label>
            <input
              type="text"
              value={dfaInput.alphabet}
              onChange={(e) => setDfaInput({ ...dfaInput, alphabet: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Start State
            </label>
            <input
              type="text"
              value={dfaInput.start_state}
              onChange={(e) => setDfaInput({ ...dfaInput, start_state: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Accept States (comma-separated)
            </label>
            <input
              type="text"
              value={dfaInput.accept_states}
              onChange={(e) => setDfaInput({ ...dfaInput, accept_states: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Transitions (format: q0:a{'>'}q1;q1:b{'>'}q2)
            </label>
            <input
              type="text"
              value={dfaInput.transitions}
              onChange={(e) => setDfaInput({ ...dfaInput, transitions: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700"
          >
            Minimize DFA
          </button>
        </form>
      )}

      {/* CFG Tab */}
      {activeTab === 'cfg' && (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Productions (format: S:aSb|ab,A:aA|ε)
            </label>
            <textarea
              value={cfgInput.productions}
              onChange={(e) => setCfgInput({ ...cfgInput, productions: e.target.value })}
              rows="4"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              placeholder="S:aSb|ab"
            />
            <p className="text-xs text-gray-500 mt-1">
              Format: NonTerminal:rule1|rule2,NonTerminal2:rule1|rule2
            </p>
          </div>
          <button
            onClick={() => handleCFGSubmit('first-follow')}
            className="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 mb-2"
          >
            Compute FIRST & FOLLOW
          </button>
          <button
            onClick={() => handleCFGSubmit('predictive')}
            className="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700"
          >
            Build Predictive Table
          </button>
        </div>
      )}
    </div>
  )
}

export default Controls

