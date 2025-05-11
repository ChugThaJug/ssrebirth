// src/lib/firebase.ts
import { initializeApp } from 'firebase/app';
import { getAuth, onAuthStateChanged, type User } from 'firebase/auth';
import { writable, derived } from 'svelte/store';

// Ensure environment variables are actually available
const apiKey = import.meta.env.VITE_FIREBASE_API_KEY;
const authDomain = import.meta.env.VITE_FIREBASE_AUTH_DOMAIN;
const projectId = import.meta.env.VITE_FIREBASE_PROJECT_ID;
const storageBucket = import.meta.env.VITE_FIREBASE_STORAGE_BUCKET;
const messagingSenderId = import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID;
const appId = import.meta.env.VITE_FIREBASE_APP_ID;

// Check if required environment variables are present
if (!apiKey || !authDomain || !projectId) {
  console.error('Firebase configuration is missing or incomplete. Check your environment variables.');
}

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey,
  authDomain,
  projectId,
  storageBucket,
  messagingSenderId,
  appId
};

console.log('Firebase Config:', { 
  apiKey: apiKey ? 'PRESENT' : 'MISSING',
  authDomain: authDomain ? 'PRESENT' : 'MISSING',
  projectId: projectId ? 'PRESENT' : 'MISSING'
});

// Initialize Firebase only if we have the required keys
let app;
let auth;
try {
  app = initializeApp(firebaseConfig);
  auth = getAuth(app);
  console.log('Firebase initialized successfully');
} catch (error) {
  console.error('Firebase initialization error:', error);
}

// Create a user store
function createUserStore() {
  const { subscribe, set } = writable<User | null>(null);
  
  let unsubscribe = () => {};
  
  // Only set up auth state listener if Firebase was initialized
  if (auth) {
    unsubscribe = onAuthStateChanged(auth, (firebaseUser) => {
      set(firebaseUser);
    });
  } else {
    console.warn('Auth is not initialized, user store will not update');
  }
  
  return {
    subscribe,
    unsubscribe
  };
}

export const user = createUserStore();
export const isAuthenticated = derived(user, ($user) => $user !== null);
export { auth };