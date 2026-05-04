const KEY = 'query_history'
const MAX = 20

export function loadHistory() {
  try {
    return JSON.parse(localStorage.getItem(KEY)) || []
  } catch {
    return []
  }
}

export function saveHistory(entry) {
  const list = loadHistory()
  list.unshift({ text: entry.text, sql: entry.sql, time: Date.now() })
  if (list.length > MAX) list.pop()
  localStorage.setItem(KEY, JSON.stringify(list))
}

export function clearHistory() {
  localStorage.removeItem(KEY)
}
