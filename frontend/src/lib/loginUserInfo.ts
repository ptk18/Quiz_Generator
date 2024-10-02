import { writable } from "svelte/store";

interface User {
    id: number | null;
    name: string;
    email: string;
    isLoggedIn: boolean;
}

// Create the store
export const userInfo = writable<User>({
    id: null,
    name: "",
    email: "",
    isLoggedIn: false
});

// Optional: Add a function to get the current value synchronously
export function getCurrentUser(): User {
    let currentUser: User;
    userInfo.subscribe(value => {
        currentUser = value;
    })();
    return currentUser!;
}

