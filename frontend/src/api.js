import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
})

// Add error interceptor for better error messages
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNREFUSED' || error.message.includes('Network Error')) {
      error.message = 'Cannot connect to backend server. Make sure the backend is running on http://localhost:8000'
    }
    return Promise.reject(error)
  }
)

export const regexToNFA = async (regex) => {
  const response = await api.post('/regex/to-nfa', { regex })
  return response.data
}

export const nfaToDFA = async (nfaData) => {
  const response = await api.post('/nfa/to-dfa', nfaData)
  return response.data
}

export const minimizeDFA = async (dfaData) => {
  const response = await api.post('/dfa/minimize', dfaData)
  return response.data
}

export const cfgFirstFollow = async (productions) => {
  // productions is already the object { "S": ["aSb", "ab"] }
  const response = await api.post('/cfg/first-follow', { productions })
  return response.data
}

export const cfgPredictiveTable = async (productions) => {
  // productions is already the object { "S": ["aSb", "ab"] }
  const response = await api.post('/cfg/predictive-table', { productions })
  return response.data
}

export default api

