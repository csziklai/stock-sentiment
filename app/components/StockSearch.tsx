"use client";

import { Input } from "@heroui/react";
import { useEffect, useState } from "react";

export default function StockSearch() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<Array<{ ticker: string; name: string }>>([]);

    useEffect(() => {
        // if (query.length < 2) {
        //     setResults([]);
        //     return;
        // }

        const timeout = setTimeout(async () => {
            const res = await fetch(`http://127.0.0.1:8000/search?q=${query}`);
            const data = await res.json();
            setResults(data);
        }, 300); // debounce

        return () => clearTimeout(timeout);
    }, [query]);

    return (

        <div className="relative w-80">
            <h1 className="relative bottom-10 text-center text-lg">
                Enter stock name</h1>
            <div className="w-full">
                <Input
                    placeholder="Search for a stock"
                    variant="bordered"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
            </div>

            {results.length > 0 && (
                <div className="absolute top-full mt-1 w-full rounded border bg-white shadow">
                    {results.map((r) => (
                        <div
                            key={r.ticker}
                            className="cursor-pointer px-3 py-2 text-black hover:bg-gray-100"
                            onClick={() => {
                                setQuery(`${r.ticker} — ${r.name}`);
                                setResults([]);
                            }}
                        >
                            <strong>{r.ticker}</strong> — {r.name}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
