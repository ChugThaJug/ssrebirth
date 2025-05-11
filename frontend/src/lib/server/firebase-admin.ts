// src/lib/server/firebase-admin.ts
import { getApps, initializeApp, cert, type App } from 'firebase-admin/app';
import { getAuth } from 'firebase-admin/auth';

let firebaseApp: App;

if (!getApps().length) {
  firebaseApp = initializeApp({
    credential: cert({
      projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
      clientEmail: import.meta.env.VITE_FIREBASE_CLIENT_EMAIL,
      privateKey: import.meta.env.VITE_FIREBASE_PRIVATE_KEY.replace(/\\n/g, '\n'),
    }),
  });
} else {
  firebaseApp = getApps()[0];
}

export const adminAuth = getAuth(firebaseApp);