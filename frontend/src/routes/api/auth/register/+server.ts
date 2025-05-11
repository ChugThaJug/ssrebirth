// src/routes/api/auth/register/+server.ts
import { adminAuth } from '$lib/server/firebase-admin';
import { prisma } from '$lib/server/prisma';
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
  try {
    const authHeader = request.headers.get('Authorization');
    
    if (!authHeader?.startsWith('Bearer ')) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), { 
        status: 401,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    const token = authHeader.split('Bearer ')[1];
    const decodedToken = await adminAuth.verifyIdToken(token);
    
    // Check if user already exists in database
    const existingUser = await prisma.user.findUnique({
      where: { firebaseUid: decodedToken.uid }
    });
    
    if (existingUser) {
      return json({ user: existingUser });
    }
    
    // Create new user in database
    const newUser = await prisma.user.create({
      data: {
        firebaseUid: decodedToken.uid,
        email: decodedToken.email || '',
        displayName: decodedToken.name || '',
        photoURL: decodedToken.picture || null
      }
    });
    
    return json({ user: newUser });
  } catch (error) {
    console.error('Authentication error:', error);
    return new Response(JSON.stringify({ error: 'Authentication failed' }), { 
      status: 401,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};