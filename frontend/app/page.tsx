export default async function Home() {
  const res = await fetch("http://localhost:3000/api/profiles/", { cache: "no-store" });
  const data = await res.json();

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">Profiles</h1>
      <pre className="bg-gray-100 p-4 rounded-lg overflow-auto">
        {JSON.stringify(data, null, 2)}
      </pre>
    </main>
  );
}
