// src/components/__tests__/ConnectionTest.test.jsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import ConnectionTest from '../ConnectionTest'
import { AuthApi } from '../../services/authApi'

// Mock the api service
vi.mock('../../services/authApi')
authApi = new AuthApi()

describe('ConnectionTest Component', () => {
    beforeEach(() => {
        // Clear all mocks before each test
        vi.clearAllMocks()
    })

    test('renders component correctly', () => {
        render(<ConnectionTest />)
        
        // Check if main elements are rendered
        expect(screen.getByText('API Connection Test')).toBeInTheDocument()
        expect(screen.getByText('Test GET Request')).toBeInTheDocument()
        expect(screen.getByText('Test POST Request')).toBeInTheDocument()
        expect(screen.getByText('Back to Login')).toBeInTheDocument()
    })

    test('renders without initial responses', () => {
        render(<ConnectionTest />)
        
        expect(screen.queryByText(/GET Response/)).not.toBeInTheDocument()
        expect(screen.queryByText(/POST Response/)).not.toBeInTheDocument()
        expect(screen.queryByText('Loading...')).not.toBeInTheDocument()
        expect(screen.queryByText(/Error/)).not.toBeInTheDocument()
    })

    test('handles successful GET request', async () => {
        // Mock the API response
        const mockGetResponse = {
            status: 'connected',
            method: 'GET',
            message: 'Django and React are successfully connected!',
            timestamp: '2024-03-18T12:00:00Z',
            test_data: {
                number: 42,
                list: [1, 2, 3],
                nested: { key: 'value' }
            }
        }
        api.get.mockResolvedValueOnce(mockGetResponse)

        render(<ConnectionTest />)
        
        // Click the GET button
        fireEvent.click(screen.getByText('Test GET Request'))

        // Wait for the response to be displayed
        await waitFor(() => {
            expect(screen.getByText(/GET Response:/)).toBeInTheDocument()
            expect(screen.getByText(/"status": "connected"/)).toBeInTheDocument()
            expect(screen.getByText(/"method": "GET"/)).toBeInTheDocument()
        })

        // Verify API was called correctly
        expect(api.get).toHaveBeenCalledWith('test/')
        expect(api.get).toHaveBeenCalledTimes(1)
    })

    test('handles successful POST request', async () => {
        // Mock the API response
        const mockPostResponse = {
            status: 'received',
            method: 'POST',
            received_data: {
                testData: 'Hello from React!',
                timestamp: expect.any(String)
            },
            message: 'Data successfully received by Django!'
        }
        api.post.mockResolvedValueOnce(mockPostResponse)

        render(<ConnectionTest />)
        
        // Click the POST button
        fireEvent.click(screen.getByText('Test POST Request'))

        // Wait for the response to be displayed
        await waitFor(() => {
            expect(screen.getByText(/POST Response:/)).toBeInTheDocument()
            expect(screen.getByText(/"status": "received"/)).toBeInTheDocument()
            expect(screen.getByText(/"method": "POST"/)).toBeInTheDocument()
        })

        // Verify API was called correctly
        expect(api.post).toHaveBeenCalledWith('test/', expect.any(Object))
        expect(api.post).toHaveBeenCalledTimes(1)
    })

    test('shows loading state for GET request', async () => {
        api.get.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)))

        render(<ConnectionTest />)
        
        fireEvent.click(screen.getByText('Test GET Request'))

        expect(screen.getByText('Loading...')).toBeInTheDocument()

        await waitFor(() => {
            expect(api.get).toHaveBeenCalled()
        })
    })

    test('shows loading state for POST request', async () => {
        api.post.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)))

        render(<ConnectionTest />)
        
        fireEvent.click(screen.getByText('Test POST Request'))

        expect(screen.getByText('Loading...')).toBeInTheDocument()

        await waitFor(() => {
            expect(api.post).toHaveBeenCalled()
        })
    })

    test('handles GET request error', async () => {
        const errorMessage = 'Network error'
        api.get.mockRejectedValueOnce(new Error(errorMessage))

        render(<ConnectionTest />)
        
        fireEvent.click(screen.getByText('Test GET Request'))

        await waitFor(() => {
            expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument()
        })
    })

    test('handles POST request error', async () => {
        const errorMessage = '400 Bad Request'
        api.post.mockRejectedValueOnce(new Error(errorMessage))

        render(<ConnectionTest />)
        
        fireEvent.click(screen.getByText('Test POST Request'))

        await waitFor(() => {
            expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument()
        })
    })

    test('buttons are disabled during GET request', async () => {
        api.get.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)))

        render(<ConnectionTest />)
        
        const getButton = screen.getByText('Test GET Request')
        const postButton = screen.getByText('Test POST Request')

        fireEvent.click(getButton)

        expect(getButton).toBeDisabled()
        expect(postButton).toBeDisabled()

        await waitFor(() => {
            expect(getButton).not.toBeDisabled()
            expect(postButton).not.toBeDisabled()
        })
    })

    test('buttons are disabled during POST request', async () => {
        api.post.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)))

        render(<ConnectionTest />)
        
        const getButton = screen.getByText('Test GET Request')
        const postButton = screen.getByText('Test POST Request')

        fireEvent.click(postButton)

        expect(getButton).toBeDisabled()
        expect(postButton).toBeDisabled()

        await waitFor(() => {
            expect(getButton).not.toBeDisabled()
            expect(postButton).not.toBeDisabled()
        })
    })

    test('clears error on new request', async () => {
        api.get.mockRejectedValueOnce(new Error('First error'))
        api.get.mockResolvedValueOnce({ status: 'connected' })

        render(<ConnectionTest />)
        
        fireEvent.click(screen.getByText('Test GET Request'))
        
        await waitFor(() => {
            expect(screen.getByText(/Error: First error/)).toBeInTheDocument()
        })

        fireEvent.click(screen.getByText('Test GET Request'))
        expect(screen.queryByText(/Error: First error/)).not.toBeInTheDocument()
    })

    test('keeps previous responses visible', async () => {
        api.get.mockResolvedValueOnce({ status: 'get_success' })
        api.post.mockResolvedValueOnce({ status: 'post_success' })

        render(<ConnectionTest />)
        
        // Make GET request
        fireEvent.click(screen.getByText('Test GET Request'))
        
        await waitFor(() => {
            expect(screen.getByText(/"status": "get_success"/)).toBeInTheDocument()
        })

        // Make POST request
        fireEvent.click(screen.getByText('Test POST Request'))
        
        await waitFor(() => {
            expect(screen.getByText(/"status": "get_success"/)).toBeInTheDocument()
            expect(screen.getByText(/"status": "post_success"/)).toBeInTheDocument()
        })
    })

    test('back link has correct href', () => {
        render(<ConnectionTest />)
        
        const backLink = screen.getByText('Back to Login')
        expect(backLink).toHaveAttribute('href', '/login')
    })
})