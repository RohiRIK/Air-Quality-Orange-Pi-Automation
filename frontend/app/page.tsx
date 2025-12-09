import Dashboard from '@/components/Dashboard';

export default function Home() {
  return (
    <main className="min-h-screen bg-[url('/bg-pattern.svg')] bg-fixed bg-cover">
      <div className="absolute inset-0 bg-slate-900/90" />
      <div className="relative z-10">
        <Dashboard />
      </div>
    </main>
  );
}