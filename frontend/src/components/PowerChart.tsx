"use client";

import { motion } from "framer-motion";
import {
    AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip,
    ResponsiveContainer, ReferenceLine,
} from "recharts";

interface PowerChartProps {
    data: { time: string; power: number; voltage: number; soc: number }[];
}

function CustomTooltip({ active, payload, label }: { active?: boolean; payload?: Array<{ value: number; dataKey: string }>; label?: string }) {
    if (!active || !payload) return null;
    return (
        <div style={{
            background: "rgba(26,31,46,0.95)",
            border: "1px solid rgba(6,214,160,0.3)",
            borderRadius: "12px",
            padding: "12px 16px",
            backdropFilter: "blur(8px)",
        }}>
            <p style={{ color: "#8892a4", fontSize: "12px", marginBottom: "8px" }}>{label}</p>
            {payload.map((entry, i) => (
                <p key={i} style={{ color: entry.dataKey === "power" ? "#06d6a0" : "#118ab2", fontSize: "13px", fontFamily: "var(--font-mono)" }}>
                    {entry.dataKey === "power" ? "⚡ " : "🔋 "}
                    {entry.value.toFixed(1)} {entry.dataKey === "power" ? "W" : "%"}
                </p>
            ))}
        </div>
    );
}

export default function PowerChart({ data }: PowerChartProps) {
    // 每 6 个点取一个显示 X 轴标签
    const tickData = data.filter((_, i) => i % 36 === 0);

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="card-glow p-6"
        >
            <div className="flex items-center justify-between mb-4">
                <div>
                    <h3 className="text-base font-semibold" style={{ color: "#f0f4f8" }}>
                        24h 发电功率趋势
                    </h3>
                    <p className="text-xs mt-0.5" style={{ color: "#6b7280" }}>
                        每 5 分钟采样 · 实时更新
                    </p>
                </div>
                <div className="flex gap-3">
                    <span className="flex items-center gap-1.5 text-xs" style={{ color: "#06d6a0" }}>
                        <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: "#06d6a0" }} /> 功率 (W)
                    </span>
                    <span className="flex items-center gap-1.5 text-xs" style={{ color: "#118ab2" }}>
                        <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: "#118ab2" }} /> SOC (%)
                    </span>
                </div>
            </div>

            <ResponsiveContainer width="100%" height={280}>
                <AreaChart data={data} margin={{ top: 5, right: 5, left: -10, bottom: 0 }}>
                    <defs>
                        <linearGradient id="powerGrad" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stopColor="#06d6a0" stopOpacity={0.4} />
                            <stop offset="100%" stopColor="#06d6a0" stopOpacity={0.02} />
                        </linearGradient>
                        <linearGradient id="socGrad" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stopColor="#118ab2" stopOpacity={0.3} />
                            <stop offset="100%" stopColor="#118ab2" stopOpacity={0.02} />
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(42,48,66,0.5)" />
                    <XAxis
                        dataKey="time"
                        stroke="#6b7280"
                        fontSize={11}
                        tickLine={false}
                        ticks={tickData.map(d => d.time)}
                    />
                    <YAxis
                        yAxisId="power"
                        stroke="#6b7280"
                        fontSize={11}
                        tickLine={false}
                        axisLine={false}
                        domain={[0, 500]}
                    />
                    <YAxis
                        yAxisId="soc"
                        orientation="right"
                        stroke="#6b7280"
                        fontSize={11}
                        tickLine={false}
                        axisLine={false}
                        domain={[0, 100]}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <ReferenceLine yAxisId="power" y={0} stroke="rgba(42,48,66,0.8)" />
                    <Area
                        yAxisId="power"
                        type="monotone"
                        dataKey="power"
                        stroke="#06d6a0"
                        strokeWidth={2}
                        fill="url(#powerGrad)"
                        dot={false}
                        activeDot={{ r: 4, stroke: "#06d6a0", fill: "#0a0e17", strokeWidth: 2 }}
                    />
                    <Area
                        yAxisId="soc"
                        type="monotone"
                        dataKey="soc"
                        stroke="#118ab2"
                        strokeWidth={1.5}
                        fill="url(#socGrad)"
                        dot={false}
                        activeDot={{ r: 3, stroke: "#118ab2", fill: "#0a0e17", strokeWidth: 2 }}
                    />
                </AreaChart>
            </ResponsiveContainer>
        </motion.div>
    );
}
