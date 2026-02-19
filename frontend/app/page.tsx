"use client";

import { useEffect, useState } from "react";

type Profile = {
  id: string;
  email: string | null;
  display_name: string | null;
  created_at: string;
};

export default function Home() {
  const [items, setItems] = useState<Profile[]>([]);
  const [email, setEmail] = useState("test3@example.com");
  const [displayName, setDisplayName] = useState("Test 3");
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setError(null);
    const res = await fetch("/api/profiles/", { cache: "no-store" });
    const data = await res.json();
    setItems(data.items ?? []);
  }

  async function createOne() {
    setError(null);
    const res = await fetch("/api/profiles/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, display_name: displayName }),
    });

    if (!res.ok) {
      const txt = await res.text();
      setError(txt);
      return;
    }
    await load();
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <main className="p-8 space-y-4">
      <h1 className="text-2xl font-bold">Profiles</h1>

      <div className="flex gap-2">
        <input
          className="border rounded px-2 py-1"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="email"
        />
        <input
          className="border rounded px-2 py-1"
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
          placeholder="display name"
        />
        <button className="border rounded px-3 py-1" onClick={createOne}>
          Create
        </button>
      </div>

      {error ? (
        <pre className="bg-red-50 border p-3 rounded">{error}</pre>
      ) : null}

      <pre className="bg-gray-100 p-4 rounded overflow-auto">
        {JSON.stringify(items, null, 2)}
      </pre>
    </main>
  );
}
