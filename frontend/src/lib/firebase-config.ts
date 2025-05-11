// src/lib/firebase-config.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { writable, derived } from 'svelte/store';

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

// Create a user store
function createUserStore() {
  const { subscribe, set } = writable(null);
  
  auth.onAuthStateChanged(async (firebaseUser) => {
    if (firebaseUser) {
      try {
        const token = await firebaseUser.getIdToken();
        
        // Call our backend to create/sync user
        const response = await fetch('/api/auth/register', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (response.ok) {
          const data = await response.json();
          set({ ...firebaseUser, dbUser: data.user, token });
        } else {
          set(firebaseUser);
        }
      } catch (error) {
        console.error('Error syncing user with backend:', error);
        set(firebaseUser);
      }
    } else {
      set(null);
    }
  });
  
  return { subscribe };
}

export const user = createUserStore();
export const isAuthenticated = derived(user, $user => $user !== null);