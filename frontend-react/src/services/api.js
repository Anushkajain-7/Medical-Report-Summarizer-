const API_BASE = "http://localhost:8000";

export const checkHealth = async () => {
    try {
        const res = await fetch(`${API_BASE}/health`);
        return res.ok;
    } catch {
        return false;
    }
};

export const fetchSampleReports = async () => {
    try {
        const res = await fetch(`${API_BASE}/sample-reports`);
        if (!res.ok) throw new Error("Failed to fetch sample reports");
        return await res.json();
    } catch (err) {
        console.error(err);
        return { reports: [] };
    }
};

export const analyzeReport = async (file, text, maxLength = 250, minLength = 50) => {
    const formData = new FormData();
    if (file) {
        formData.append("file", file);
    } else if (text) {
        formData.append("text", text);
    } else {
        throw new Error("Provide either a file or text input.");
    }
    formData.append("max_length", maxLength);
    formData.append("min_length", minLength);

    const res = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        body: formData,
    });

    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Analysis failed.");
    }
    return await res.json();
};

export const summarizeText = async (text, maxLength = 250, minLength = 50) => {
    const res = await fetch(`${API_BASE}/summarize`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, max_length: maxLength, min_length: minLength }),
    });

    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Summarization failed.");
    }
    return await res.json();
};

export const extractEntities = async (text) => {
    const res = await fetch(`${API_BASE}/ner`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
    });

    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "NER extraction failed.");
    }
    return await res.json();
};

export const computeRouge = async (reference, hypothesis) => {
    const res = await fetch(`${API_BASE}/rouge`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reference, hypothesis }),
    });

    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "ROUGE evaluation failed.");
    }
    return await res.json();
};
