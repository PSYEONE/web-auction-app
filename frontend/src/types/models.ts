// User interfaces
export interface User {
    id: number;
    username: string;
    email: string;
    profile_image: string | null;
}

export interface UserProfile extends User {
    date_of_birth: string | null;
}

// Auction interfaces
export interface Bid {
    id: number;
    item: number;
    bidder: User;
    amount: string;
    timestamp: string;
}

export interface Question {
    id: number;
    item: number;
    author: User;
    question_text: string;
    timestamp: string;
    reply_text: string | null;
    reply_timestamp: string | null;
}

export interface Item {
    id: number;
    owner: User;
    title: string;
    description: string;
    starting_price: string;
    image: string;
    end_date: string;
    is_active: boolean;
    bids: Bid[];
    questions: Question[];
    highest_bid: string | null;
}

// API request types
export interface BidCreate {
    amount: string;
}

export interface QuestionCreate {
    question_text: string;
}

export interface ReplyCreate {
    reply_text: string;
}

export interface ItemCreate {
    title: string;
    description: string;
    starting_price: string;
    image: File;
    end_date: string;
}

export interface ProfileUpdate {
    email: string;
    date_of_birth: string | null;
    profile_image?: File;
}