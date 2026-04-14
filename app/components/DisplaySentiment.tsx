"use client";

//import { Input } from "@heroui/react";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

export default function DisplaySentiment() {
    type SentimentResult = Array<unknown>;
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

    if (loading) return (
        <div className="flex h-screen items-center justify-center">
            <p className="text-xl">Analyzing sentiment </p>
            <span className="inline-flex gap-1">
                <span className="text-xl animate-pulse [animation-delay:0ms]">.</span>
                <span className="text-xl animate-pulse [animation-delay:200ms]">.</span>
                <span className="text-xl animate-pulse [animation-delay:400ms]">.</span>
            </span>
        </div>);
    if (error) return <div>{error}</div>;

    return (
        <div className="relative top-30">
            <h1 className="text-center text-4xl p-8 pb-14">{ticker}</h1>
            <div className="grid grid-cols-2 gap-x-24 max-w-2xl mx-auto text-left justify-items-center">

                <div className="space-y-2">
                    <p className="font-bold text-xl">Sentiment</p>
                    <p className="">{data["sentiment"]}</p>
                </div>

                <div className="space-y-2">
                    <p className="font-bold text-xl">Score</p>
                    <p className="">{data["score"]}</p>
                </div>

            </div>
            <p className="font-bold text-xl">Top articles</p>


            {/* <pre>{JSON.stringify(data, null, 2)}</pre> */}
        </div>
    );

}