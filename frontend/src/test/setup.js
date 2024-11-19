// src/test/setup.js
import '@testing-library/jest-dom'

// Mock fetch if needed
global.fetch = vi.fn()

// Clean up after each test
afterEach(() => {
  vi.clearAllMocks()
})