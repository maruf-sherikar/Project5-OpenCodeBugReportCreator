import axios from 'axios';

const API_BASE = 'http://localhost:3001/api';

export interface ConversionResponse {
    files: {
        fileName: string;
        fileType: 'page-object' | 'test-spec' | 'utility';
        content: string;
    }[];
    logs?: string[];
    error?: string;
}

export const convertCode = async (sourceCode: string, usePOM: boolean): Promise<ConversionResponse> => {
    try {
        const response = await axios.post(`${API_BASE}/convert`, {
            sourceCode,
            options: { usePageObjectModel: usePOM }
        });
        return response.data;
    } catch (error: any) {
        console.error("API Error:", error);
        return {
            files: [],
            error: error.response?.data?.error || error.message || "Unknown error occurred"
        };
    }
};
