// src/lib/server/auth.ts
import { adminAuth } from './firebase-admin';
import { prisma } from './prisma';
import type { RequestEvent } from '@sveltejs/kit';

export async function authenticateRequest(event: RequestEvent) {
  try {
    const authHeader = event.request.headers.get('Authorization');
    
    if (!authHeader?.startsWith('Bearer ')) {
      return null;
    }
    
    const token = authHeader.split('Bearer ')[1];
    const decodedToken = await adminAuth.verifyIdToken(token);
    
    // Get user from database
    const user = await prisma.user.findUnique({
      where: { firebaseUid: decodedToken.uid }
    });
    
    if (!user) {
      return null;
    }
    
    return user;
  } catch (error) {
    console.error('Auth verification error:', error);
    return null;
  }
}