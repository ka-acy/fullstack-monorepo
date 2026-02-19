"use client";

import { supabase } from "@/lib/supabase/client";
import type { Session } from "@supabase/supabase-js";
import { useEffect, useState } from "react";

type Profile = {
  id: string;
  email: string | null;
  display_name: string | null;
  created_at: string;
};

export default function Home() {
  const [items, setItems] = useState<Profile[]>([]);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [session, setSession] = useState<Session | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function signUp() {
    setError(null);
    const { error: authError } = await supabase.auth.signUp({ email, password });
    if (authError) setError(authError.message);
  }

  async function signIn() {
    setError(null);
    const { error: authError } = await supabase.auth.signInWithPassword({ email, password });
    if (authError) setError(authError.message);
  }

  async function signOut() {
    setError(null);
    const { error: authError } = await supabase.auth.signOut();
    if (authError) setError(authError.message);
  }

  async function loadProfileForToken(token: string) {
    const res = await fetch("/api/profiles/me", {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store",
    });

    if (!res.ok) {
      setError(`HTTP ${res.status}: ${await res.text()}`);
      return;
    }

    const data = await res.json();
    setItems(data.items ? data.items : [data]);
  }

  useEffect(() => {
    let active = true;

    const applySession = async (nextSession: Session | null) => {
      if (!active) return;
      setSession(nextSession);
      if (nextSession?.access_token) {
        await loadProfileForToken(nextSession.access_token);
      } else {
        setItems([]);
      }
    };

    void supabase.auth.getSession().then(({ data }) => {
      void applySession(data.session ?? null);
    });

    const { data: sub } = supabase.auth.onAuthStateChange((_event, nextSession) => {
      void applySession(nextSession);
    });

    return () => {
      active = false;
      sub.subscription.unsubscribe();
    };
  }, []);

  async function updateMyProfile() {
    const token = session?.access_token;
    if (!token) {
      setError("Sign in first");
      return;
    }

    const res = await fetch("/api/profiles/me", {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ display_name: displayName }),
    });

    if (!res.ok) {
      setError(await res.text());
      return;
    }

    await loadProfileForToken(token);
  }

  return (
    <main className="p-8 space-y-6 max-w-xl">
      <h1 className="text-2xl font-bold">Auth + Profiles</h1>

      <div className="space-y-2">
        <input
          className="border rounded px-2 py-1 w-full"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="email"
        />
        <input
          className="border rounded px-2 py-1 w-full"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="password"
        />

        <div className="flex gap-2">
          <button type="button" className="border px-3 py-1" onClick={signUp}>
            Sign up
          </button>
          <button type="button" className="border px-3 py-1" onClick={signIn}>
            Sign in
          </button>
          <button type="button" className="border px-3 py-1" onClick={signOut}>
            Sign out
          </button>
        </div>

        <div className="text-sm">Signed in: {session ? "Yes" : "No"}</div>
      </div>

      <div className="flex gap-2">
        <input
          className="border px-2 py-1"
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
          placeholder="display name"
        />
        <button className="border px-3 py-1" onClick={updateMyProfile}>
          Update Profile
        </button>
      </div>

      {error && <pre className="bg-red-50 border p-3 rounded">{error}</pre>}

      <pre className="bg-gray-100 p-4 rounded overflow-auto">{JSON.stringify(items, null, 2)}</pre>
    </main>
  );
}
