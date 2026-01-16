"use client";

//import { Input } from "@heroui/react";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

export default function DisplaySentiment() {
    type SentimentResult = unknown;
    const params = useSearchParams();
    const ticker = params.get("symbol"); // how does this work?

    const [data, setData] = useState<SentimentResult | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!ticker) return;

        const run = async () => {
            try {
                const res = await fetch("http://127.0.0.1:8000/stock-sentiment", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ ticker: ticker }),
                });
                console.log("tried");
                console.log(res);

                if (!res.ok) throw new Error("Request failed");
                console.log("res was ok?")
                const result = await res.json();
                setData(result);
            } catch (err) {
                setError("Failed to analyze sentiment")
            } finally {
                setLoading(false);
            }
        };
        run();

    }, [ticker]);

    if (loading) return <div>Analyzing sentiment...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div>
            <h1>{ticker} Sentiment</h1>
            <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
    );

}