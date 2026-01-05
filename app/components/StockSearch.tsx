"use client";

//import { Input } from "@heroui/react";
import ArrowCircleRightOutlinedIcon from '@mui/icons-material/ArrowCircleRightOutlined';
import { useEffect, useState } from "react";
//import { useLocation, useNavigate } from 'react-router-dom';

export default function StockSearch() {
    //const location = useLocation();
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<Array<{ ticker: string; name: string }>>([]);
    const [selected, setSelected] = useState(false);
    const [selectedStock, setSelectedStock] = useState<{
        ticker: string;
        name: string
    } | null>(null);

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

    const handleNext = async (e: React.MouseEvent) => {
        e.preventDefault();
        if (!selectedStock) return;

        await fetch("http://127.0.0.1:8000/stock-sentiment", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(selectedStock),
        });
    };

    return (

        <div className="relative w-80">
            <h1 className="relative bottom-10 text-center text-lg">
                Enter stock name</h1>
            <input
                type="text"
                placeholder="Search for a stock"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full h-10 rounded-md border border-gray-300 px-3 focus:outline-none focus:ring-2 focus:ring-black"
            />


            {results.length > 0 && (
                <div className="absolute top-full mt-1 w-full rounded border bg-white shadow">
                    {results.map((r) => (
                        <div
                            key={r.ticker}
                            className="cursor-pointer px-3 py-2 text-black hover:bg-gray-100"
                            onClick={() => {
                                setQuery(`${r.ticker} — ${r.name}`);
                                setResults([]);
                                setSelected(true);
                                setSelectedStock({ ticker: r.ticker, name: r.name });

                            }}
                        >
                            <strong>{r.ticker}</strong> — {r.name}
                        </div>
                    ))}
                </div>
            )}
            {selected &&
                (<ArrowCircleRightOutlinedIcon
                    color="success"
                    className="absolute top-26/50 left-83 cursor-pointer"
                    onClick={handleNext}
                // className="relative left-3"


                />)}
        </div>
    );
}
