// src/components/__tests__/ConnectionTest.test.jsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import ConnectionTest from '../ConnectionTest'
import { api } from '../../services/api'

// Mock the api service
vi.mock('../../services/api')

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

    test('shows loading state', async () => {
        // Make the API call take some time
        api.get.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)))

        render(<ConnectionTest />)
        
        // Click the GET button
        fireEvent.click(screen.getByText('Test GET Request'))

        // Check if loading message appears
        expect(screen.getByText('Loading...')).toBeInTheDocument()

        // Wait for loading to finish
        await waitFor(() => {
            expect(api.get).toHaveBeenCalled()
        })
    })

    test('handles API error', async () => {
        // Mock an API error
        const errorMessage = 'Network error'
        api.get.mockRejectedValueOnce(new Error(errorMessage))

        render(<ConnectionTest />)
        
        // Click the GET button
        fireEvent.click(screen.getByText('Test GET Request'))

        // Wait for error message to appear
        await waitFor(() => {
            expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument()
        })
    })

    test('buttons are disabled during loading', async () => {
        // Make the API call take some time
        api.get.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)))

        render(<ConnectionTest />)
        
        const getButton = screen.getByText('Test GET Request')
        const postButton = screen.getByText('Test POST Request')

        // Click GET button
        fireEvent.click(getButton)

        // Check if buttons are disabled
        expect(getButton).toBeDisabled()
        expect(postButton).toBeDisabled()

        // Wait for loading to finish
        await waitFor(() => {
            expect(getButton).not.toBeDisabled()
            expect(postButton).not.toBeDisabled()
        })
    })
})