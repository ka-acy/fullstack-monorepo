import { NextResponse, type NextRequest } from "next/server";

/**
 * Minimal placeholder for session refresh logic.
 * This keeps your build unblocked.
 *
 * Later, we can implement real Supabase auth session refresh
 * using @supabase/ssr or @supabase/auth-helpers-nextjs depending on your setup.
 */
export async function updateSession(request: NextRequest) {
  return NextResponse.next({
    request: {
      headers: request.headers,
    },
  });
}
