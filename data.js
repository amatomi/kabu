const STOCK_DATA = {
    "retrieval_time": "2026/02/20 14:25",
    "rankings": {
        "値上がり率": [
            { "rank": 1, "code": "6356", "name": "日ギア", "price": "1,378", "change_pct": "+26.19%", "volume": "10,438,200", "per": "13.3", "pbr": "1.44", "yield": "0.58%" },
            { "rank": 2, "code": "6085", "name": "アーキテクツ", "price": "1,772", "change_pct": "+20.38%", "volume": "121,800", "per": "-", "pbr": "-", "yield": "-" },
            { "rank": 3, "code": "7719", "name": "東京衡機", "price": "480", "change_pct": "+20.00%", "volume": "2,642,200", "per": "18.5", "pbr": "2.18", "yield": "-" },
            { "rank": 4, "code": "421A", "name": "ムービン", "price": "2,008", "change_pct": "+4.58%", "volume": "450,200", "per": "22.5", "pbr": "3.12", "yield": "0.19%" },
            { "rank": 5, "code": "8705", "name": "日産証券G", "price": "297", "change_pct": "+4.58%", "volume": "2,142,300", "per": "11.2", "pbr": "0.95", "yield": "5.05%" },
            // ... (simulated more entries for the demo/walkthrough to reach 100 for the user to see the scrolling)
            ...Array.from({ length: 95 }, (_, i) => ({
                "rank": i + 6,
                "code": (1000 + i).toString(),
                "name": `銘柄サンプル ${i + 6}`,
                "price": (1000 + i * 10).toLocaleString(),
                "change_pct": `+${(Math.random() * 5).toFixed(2)}%`,
                "volume": (Math.floor(Math.random() * 1000000)).toLocaleString(),
                "per": (Math.random() * 50).toFixed(1),
                "pbr": (Math.random() * 5).toFixed(2),
                "yield": (Math.random() * 5).toFixed(2) + "%"
            }))
        ],
        "値下がり率": [
            { "rank": 1, "code": "215A", "name": "タイミー", "price": "950", "change_pct": "-15.8%", "volume": "5,438,200", "per": "35.3", "pbr": "5.44", "yield": "-" },
            { "rank": 2, "code": "4582", "name": "シンバイオ", "price": "180", "change_pct": "-12.5%", "volume": "3,121,800", "per": "-", "pbr": "8.8", "yield": "-" },
            ...Array.from({ length: 98 }, (_, i) => ({
                "rank": i + 3,
                "code": (2000 + i).toString(),
                "name": `銘柄サンプル ${i + 3}`,
                "price": (500 + i * 5).toLocaleString(),
                "change_pct": `-${(Math.random() * 5).toFixed(2)}%`,
                "volume": (Math.floor(Math.random() * 500000)).toLocaleString(),
                "per": (Math.random() * 30).toFixed(1),
                "pbr": (Math.random() * 3).toFixed(2),
                "yield": (Math.random() * 2).toFixed(2) + "%"
            }))
        ],
        "出来高": [
            { "rank": 1, "code": "9432", "name": "ＮＴＴ", "price": "151.3", "change_pct": "-0.66%", "volume": "177,734,400", "per": "12.8", "pbr": "1.30", "yield": "3.50%" },
            { "rank": 2, "code": "6740", "name": "Ｊディスプレ", "price": "23", "change_pct": "0.00%", "volume": "153,975,300", "per": "-", "pbr": "-", "yield": "-" },
            ...Array.from({ length: 98 }, (_, i) => ({
                "rank": i + 3,
                "code": (3000 + i).toString(),
                "name": `出来高銘柄 ${i + 3}`,
                "price": (Math.floor(Math.random() * 5000)).toLocaleString(),
                "change_pct": `${(Math.random() * 4 - 2).toFixed(2)}%`,
                "volume": (100000000 - i * 1000000).toLocaleString(),
                "per": (Math.random() * 40).toFixed(1),
                "pbr": (Math.random() * 4).toFixed(2),
                "yield": (Math.random() * 4).toFixed(2) + "%"
            }))
        ],
        "配当利回り": [
            { "rank": 1, "code": "3758", "name": "アエリア", "price": "240", "change_pct": "-2.04%", "volume": "152,000", "per": "18.5", "pbr": "1.52", "yield": "7.86%" },
            { "rank": 2, "code": "3205", "name": "レーサム", "price": "1,250", "change_pct": "+0.81%", "volume": "85,600", "per": "12.3", "pbr": "2.45", "yield": "7.39%" },
            { "rank": 3, "code": "9286", "name": "エネクスＩＦ", "price": "57,000", "change_pct": "+0.35%", "volume": "588", "per": "14.4", "pbr": "0.73", "yield": "7.14%" },
            ...Array.from({ length: 97 }, (_, i) => ({
                "rank": i + 4,
                "code": (4000 + i).toString(),
                "name": `高利回り銘柄 ${i + 4}`,
                "price": (1000 + i * 50).toLocaleString(),
                "change_pct": `${(Math.random() * 2 - 1).toFixed(2)}%`,
                "volume": (Math.floor(Math.random() * 100000)).toLocaleString(),
                "per": (Math.random() * 15 + 5).toFixed(1),
                "pbr": (Math.random() * 1.5 + 0.5).toFixed(2),
                "yield": (7 - i * 0.05).toFixed(2) + "%"
            }))
        ],
        // Other themes added similarly for a full 100 experience
        "値上がり幅": Array.from({ length: 100 }, (_, i) => ({
            "rank": i + 1,
            "code": (5000 + i).toString(),
            "name": `大幅上昇 ${i + 1}`,
            "price": (5000 + i * 100).toLocaleString(),
            "change_pct": `+${(Math.random() * 1000).toFixed(0)}`,
            "volume": (Math.floor(Math.random() * 200000)).toLocaleString(),
            "per": (Math.random() * 60).toFixed(1),
            "pbr": (Math.random() * 10).toFixed(2),
            "yield": (Math.random() * 3).toFixed(2) + "%"
        })),
        "値下がり幅": Array.from({ length: 100 }, (_, i) => ({
            "rank": i + 1,
            "code": (6000 + i).toString(),
            "name": `大幅下落 ${i + 1}`,
            "price": (10000 - i * 50).toLocaleString(),
            "change_pct": `-${(Math.random() * 1000).toFixed(0)}`,
            "volume": (Math.floor(Math.random() * 100000)).toLocaleString(),
            "per": (Math.random() * 40).toFixed(1),
            "pbr": (Math.random() * 5).toFixed(2),
            "yield": (Math.random() * 2).toFixed(2) + "%"
        })),
        "売買代金": Array.from({ length: 100 }, (_, i) => ({
            "rank": i + 1,
            "code": (7000 + i).toString(),
            "name": `主要銘柄 ${i + 1}`,
            "price": (Math.floor(Math.random() * 20000)).toLocaleString(),
            "change_pct": `${(Math.random() * 6 - 3).toFixed(2)}%`,
            "volume": (100000 - i * 1000).toLocaleString() + "M",
            "per": (Math.random() * 30).toFixed(1),
            "pbr": (Math.random() * 8).toFixed(2),
            "yield": (Math.random() * 4).toFixed(2) + "%"
        })),
        "高PER": Array.from({ length: 100 }, (_, i) => ({
            "rank": i + 1,
            "code": (8000 + i).toString(),
            "name": `成長株 ${i + 1}`,
            "price": (Math.floor(Math.random() * 10000)).toLocaleString(),
            "change_pct": `${(Math.random() * 4 - 2).toFixed(2)}%`,
            "volume": (Math.floor(Math.random() * 300000)).toLocaleString(),
            "per": (1000 - i * 5).toFixed(1),
            "pbr": (Math.random() * 15 + 5).toFixed(2),
            "yield": (Math.random() * 1.5).toFixed(2) + "%"
        })),
        "低PER": Array.from({ length: 100 }, (_, i) => ({
            "rank": i + 1,
            "code": (9000 + i).toString(),
            "name": `割安株 ${i + 1}`,
            "price": (Math.floor(Math.random() * 3000)).toLocaleString(),
            "change_pct": `${(Math.random() * 2 - 1).toFixed(2)}%`,
            "volume": (Math.floor(Math.random() * 100000)).toLocaleString(),
            "per": (1 + i * 0.1).toFixed(1),
            "pbr": (Math.random() * 0.8 + 0.2).toFixed(2),
            "yield": (Math.random() * 5 + 1).toFixed(2) + "%"
        })),
        "高PBR": Array.from({ length: 100 }, (_, i) => ({
            "rank": i + 1,
            "code": (1100 + i).toString(),
            "name": `期待株 ${i + 1}`,
            "price": (Math.floor(Math.random() * 15000)).toLocaleString(),
            "change_pct": `${(Math.random() * 5 - 2).toFixed(2)}%`,
            "volume": (Math.floor(Math.random() * 400000)).toLocaleString(),
            "per": (Math.random() * 100).toFixed(1),
            "pbr": (50 - i * 0.4).toFixed(2),
            "yield": (Math.random() * 1).toFixed(2) + "%"
        })),
        "低PBR": Array.from({ length: 100 }, (_, i) => ({
            "rank": i + 1,
            "code": (1200 + i).toString(),
            "name": `資産株 ${i + 1}`,
            "price": (Math.floor(Math.random() * 2000)).toLocaleString(),
            "change_pct": `${(Math.random() * 2 - 1).toFixed(2)}%`,
            "volume": (Math.floor(Math.random() * 50000)).toLocaleString(),
            "per": (Math.random() * 20 + 5).toFixed(1),
            "pbr": (0.2 + i * 0.005).toFixed(2),
            "yield": (Math.random() * 6).toFixed(2) + "%"
        }))
    }
};
