import StockSearch from "./components/StockSearch";

export default function Home() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column' }} className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <h1>Enter stock name</h1>
      <StockSearch />
    </div>
  );
}