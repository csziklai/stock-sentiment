import StockSearch from "./components/StockSearch";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center w-full justify-center bg-zinc-50 font-sans dark:bg-black">
      {/* <h1>Enter stock name</h1> */}
      <StockSearch />
    </div>
  );
}