const API_BASE = "http://localhost:8000";

/**
 * Verifies system connectivity and backend health.
 */
export const checkHealth = async () => {
    try {
        const res = await fetch(`${API_BASE}/health`);
        return res.ok;
    } catch {
        return false;
    }
};

/**
 * Main analysis orchestration. Sends medical reports (file or text) 
 * for clinical pattern inference and interpretation.
 */
export const analyzeReport = async (file, text) => {
    const formData = new FormData();
    if (file) {
        formData.append("file", file);
    } else if (text) {
        formData.append("text", text);
    } else {
        throw new Error("Please provide a clinical document to begin.");
    }

    const res = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        body: formData,
    });

    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        // Handle common backend errors
        if (res.status === 401) throw new Error("Authentication failed. Please check your HF_API_TOKEN in the backend .env file.");
        if (res.status === 400) throw new Error(err.detail || "The document could not be processed.");
        throw new Error(err.detail || "The intelligence engine encountered an error.");
    }
    
    return await res.json();
};
