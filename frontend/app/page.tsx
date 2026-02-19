export default async function Home() {
  const res = await fetch("http://localhost:8000/ping", {
    cache: "no-store",
  });

  const data = await res.json();

  return (
    <main className="min-h-screen flex items-center justify-center">
      <h1 className="text-3xl font-bold">{data.message}</h1>
    </main>
  );
}
