// src/lib/quizStore.ts
import { writable } from 'svelte/store';

interface Quiz {
    q_id: number;
    user_id: number;
    score: number;
    total_questions: number;
    questions: {
        question: string;
        optionA: string;
        optionB: string;
        optionC: string;
        optionD: string;
        correctAns: string;
        userAnswer: string;
        isCorrect: boolean;
    }[];
}

// Update the store to hold Quiz or null
export const selectedQuiz = writable<Quiz | null>(null);
