"use client";

import { motion } from "framer-motion";
import { Battery, BatteryCharging } from "lucide-react";

interface BatteryGaugeProps {
    soc: number;
    voltage: number;
    isCharging?: boolean;
}

export default function BatteryGauge({ soc, voltage, isCharging = true }: BatteryGaugeProps) {
    const getColor = (level: number) => {
        if (level >= 80) return "#06d6a0";
        if (level >= 50) return "#ffd166";
        if (level >= 20) return "#f77f00";
        return "#ef476f";
    };

    const color = getColor(soc);
    const circumference = 2 * Math.PI * 58;
    const offset = circumference - (soc / 100) * circumference;

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6 }}
            className="card-glow p-6 flex flex-col items-center"
        >
            <p className="text-sm mb-4" style={{ color: "#8892a4" }}>电池状态</p>

            {/* Circular gauge */}
            <div className="relative w-36 h-36 mb-4">
                <svg className="w-full h-full -rotate-90" viewBox="0 0 128 128">
                    {/* Background circle */}
                    <circle
                        cx="64" cy="64" r="58"
                        fill="none"
                        stroke="rgba(42,48,66,0.6)"
                        strokeWidth="8"
                    />
                    {/* Progress arc */}
                    <motion.circle
                        cx="64" cy="64" r="58"
                        fill="none"
                        stroke={color}
                        strokeWidth="8"
                        strokeLinecap="round"
                        strokeDasharray={circumference}
                        initial={{ strokeDashoffset: circumference }}
                        animate={{ strokeDashoffset: offset }}
                        transition={{ duration: 1.2, ease: "easeOut" }}
                        style={{ filter: `drop-shadow(0 0 6px ${color})` }}
                    />
                </svg>

                {/* Center content */}
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <motion.span
                        key={soc}
                        initial={{ scale: 0.8 }}
                        animate={{ scale: 1 }}
                        className="text-3xl font-bold"
                        style={{ color, fontFamily: "var(--font-mono)" }}
                    >
                        {soc}%
                    </motion.span>
                    <span className="text-xs" style={{ color: "#6b7280" }}>SOC</span>
                </div>
            </div>

            {/* Info row */}
            <div className="flex items-center gap-4 text-sm">
                <div className="flex items-center gap-1.5">
                    {isCharging ? (
                        <BatteryCharging size={16} style={{ color: "#06d6a0" }} />
                    ) : (
                        <Battery size={16} style={{ color: "#8892a4" }} />
                    )}
                    <span style={{ color: isCharging ? "#06d6a0" : "#8892a4" }}>
                        {isCharging ? "充电中" : "待机"}
                    </span>
                </div>
                <div style={{ color: "#8892a4" }}>
                    <span style={{ color: "#f0f4f8", fontFamily: "var(--font-mono)" }}>{voltage}</span> V
                </div>
            </div>
        </motion.div>
    );
}
