import api from './api';

export const scannerService = {
    uploadFile: async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        const response = await api.post('/scanner/upload/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
        return response.data;
    },

    getJobStatus: async (jobId) => {
        const response = await api.get(`/scanner/jobs/${jobId}/`);
        return response.data;
    }
};
