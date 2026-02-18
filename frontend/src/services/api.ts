import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

// In a real app, this would be managed by a Context or Redux
let authToken: string | null = null;

export const setAuthToken = (token: string) => {
    authToken = token;
};

const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add token
apiClient.interceptors.request.use((config) => {
    if (authToken) {
        config.headers.Authorization = `Bearer ${authToken}`;
    }
    return config;
});

export interface Activity {
    id: string;
    activity_type: string;
    description: string;
    carbon_estimate: number;
    confidence_score: number;
    timestamp: string;
    raw_data?: string;
}

export const activityService = {
    getAll: async (skip: number = 0, limit: number = 50) => {
        const response = await apiClient.get<Activity[]>(`/activities?skip=${skip}&limit=${limit}`);
        return response.data;
    },

    uploadBatch: async (file: File) => {
        const formData = new FormData();
        formData.append('file', file);
        const response = await apiClient.post('/batch/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
    }
};
