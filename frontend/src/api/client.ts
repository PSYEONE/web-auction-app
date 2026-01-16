import type {
    UserProfile,
    Item,
    Bid,
    Question,
    BidCreate,
    QuestionCreate,
    ReplyCreate,
    ItemCreate,
    ProfileUpdate,
} from '../types/models';

const API_BASE = '/api';

// Helper to get CSRF token from cookies
function getCsrfToken(): string {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const trimmed = cookie.trim();
        if (trimmed.startsWith(name + '=')) {
            return trimmed.substring(name.length + 1);
        }
    }
    return '';
}

// Generic fetch wrapper
async function apiFetch<T>(
    url: string,
    options: RequestInit = {}
): Promise<T> {
    const headers: Record<string, string> = {
        ...(options.headers as Record<string, string>),
    };

    // Add CSRF token for non-GET requests
    if (options.method && options.method !== 'GET') {
        headers['X-CSRFToken'] = getCsrfToken();
    }

    // Add Content-Type for JSON (not for FormData)
    if (options.body && !(options.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
    }

    const response = await fetch(url, {
        ...options,
        headers,
        credentials: 'include',
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }));
        throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
}

// API methods
export const api = {
    // Profile
    getProfile: () => apiFetch<UserProfile>(`${API_BASE}/profile/`),

    updateProfile: (data: ProfileUpdate) => {
        const formData = new FormData();
        formData.append('email', data.email);
        if (data.date_of_birth) formData.append('date_of_birth', data.date_of_birth);
        if (data.profile_image) formData.append('profile_image', data.profile_image);

        return apiFetch<UserProfile>(`${API_BASE}/profile/`, {
            method: 'PUT',
            body: formData,
        });
    },

    // Items
    getItems: (search?: string) => {
        const url = search ? `${API_BASE}/items/?search=${encodeURIComponent(search)}` : `${API_BASE}/items/`;
        return apiFetch<Item[]>(url);
    },

    getItem: (id: number) => apiFetch<Item>(`${API_BASE}/items/${id}/`),

    createItem: (data: ItemCreate) => {
        const formData = new FormData();
        formData.append('title', data.title);
        formData.append('description', data.description);
        formData.append('starting_price', data.starting_price);
        formData.append('end_date', data.end_date);
        formData.append('image', data.image);

        return apiFetch<Item>(`${API_BASE}/items/`, {
            method: 'POST',
            body: formData,
        });
    },

    // Bids
    placeBid: (itemId: number, data: BidCreate) =>
        apiFetch<Bid>(`${API_BASE}/items/${itemId}/bid/`, {
            method: 'POST',
            body: JSON.stringify(data),
        }),

    // Questions
    postQuestion: (itemId: number, data: QuestionCreate) =>
        apiFetch<Question>(`${API_BASE}/items/${itemId}/question/`, {
            method: 'POST',
            body: JSON.stringify(data),
        }),

    replyQuestion: (questionId: number, data: ReplyCreate) =>
        apiFetch<Question>(`${API_BASE}/questions/${questionId}/reply/`, {
            method: 'PATCH',
            body: JSON.stringify(data),
        }),
};