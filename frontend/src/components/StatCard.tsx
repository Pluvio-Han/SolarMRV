"use client";

import { motion } from "framer-motion";
import { LucideIcon } from "lucide-react";

interface StatCardProps {
    title: string;
    value: string | number;
    unit: string;
    icon: LucideIcon;
    color: "cyan" | "amber" | "blue" | "red" | "green";
    subtitle?: string;
    trend?: "up" | "down" | "stable";
}

const colorMap = {
    cyan: { bg: "rgba(6,214,160,0.1)", text: "#06d6a0", border: "rgba(6,214,160,0.3)" },
    amber: { bg: "rgba(255,209,102,0.1)", text: "#ffd166", border: "rgba(255,209,102,0.3)" },
    blue: { bg: "rgba(17,138,178,0.1)", text: "#118ab2", border: "rgba(17,138,178,0.3)" },
    red: { bg: "rgba(239,71,111,0.1)", text: "#ef476f", border: "rgba(239,71,111,0.3)" },
    green: { bg: "rgba(6,214,160,0.1)", text: "#06d6a0", border: "rgba(6,214,160,0.3)" },
};

export default function StatCard({ title, value, unit, icon: Icon, color, subtitle, trend }: StatCardProps) {
    const c = colorMap[color];

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="card-glow p-5"
            style={{ borderColor: c.border }}
        >
            <div className="flex items-start justify-between mb-3">
                <div
                    className="p-2.5 rounded-xl"
                    style={{ backgroundColor: c.bg }}
                >
                    <Icon size={22} style={{ color: c.text }} />
                </div>
                {trend && (
                    <span className="text-xs px-2 py-1 rounded-full" style={{
                        backgroundColor: trend === "up" ? "rgba(6,214,160,0.15)" : trend === "down" ? "rgba(239,71,111,0.15)" : "rgba(136,146,164,0.15)",
                        color: trend === "up" ? "#06d6a0" : trend === "down" ? "#ef476f" : "#8892a4",
                    }}>
                        {trend === "up" ? "▲" : trend === "down" ? "▼" : "—"}
                    </span>
                )}
            </div>
            <p className="text-sm mb-1" style={{ color: "#8892a4" }}>{title}</p>
            <div className="flex items-baseline gap-1.5">
                <motion.span
                    key={String(value)}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-3xl font-bold tracking-tight"
                    style={{ color: c.text, fontFamily: "var(--font-mono)" }}
                >
                    {value}
                </motion.span>
                <span className="text-sm" style={{ color: "#8892a4" }}>{unit}</span>
            </div>
            {subtitle && (
                <p className="text-xs mt-2" style={{ color: "#6b7280" }}>{subtitle}</p>
            )}
        </motion.div>
    );
}
