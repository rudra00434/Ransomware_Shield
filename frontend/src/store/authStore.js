import { create } from 'zustand';
import api from '../services/api';

const useAuthStore = create((set) => ({
    user: null,
    isAuthenticated: !!localStorage.getItem('access_token'),
    loading: false,
    error: null,

    login: async (email, password) => {
        set({ loading: true, error: null });
        try {
            const response = await api.post('/auth/login/', { email, password });
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);
            set({ isAuthenticated: true, user: { email }, loading: false });
            return true;
        } catch (err) {
            const errorMsg = err.response?.data?.detail || err.response?.data?.error || 'Invalid credentials';
            set({ error: typeof err.response?.data === 'string' ? err.response.data : errorMsg, loading: false });
            return false;
        }
    },

    register: async (email, password) => {
        set({ loading: true, error: null });
        try {
            await api.post('/auth/register/', { email, password });
            return await useAuthStore.getState().login(email, password);
        } catch (err) {
            let errorMsg = 'Registration failed or email already exists.';
            if (err.response?.data) {
                // If django sends an object of errors, map them
                const errData = err.response.data;
                const firstError = Object.values(errData)[0];
                if (Array.isArray(firstError)) {
                    errorMsg = firstError[0];
                } else if (typeof firstError === 'string') {
                    errorMsg = firstError;
                }
            }
            set({ error: errorMsg, loading: false });
            return false;
        }
    },

    logout: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        set({ user: null, isAuthenticated: false });
        window.location.href = '/login';
    }
}));

export default useAuthStore;
