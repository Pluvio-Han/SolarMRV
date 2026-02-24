"use client";

import { motion } from "framer-motion";
import { ExternalLink, ShieldCheck } from "lucide-react";
import type { SolarRecord } from "@/lib/mock-data";

interface RecordTableProps {
    records: SolarRecord[];
}

export default function RecordTable({ records }: RecordTableProps) {
    const latest = records.slice(-10).reverse();

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="card-glow p-6"
        >
            <div className="flex items-center justify-between mb-5">
                <div>
                    <h3 className="text-base font-semibold" style={{ color: "#f0f4f8" }}>
                        链上数据记录
                    </h3>
                    <p className="text-xs mt-0.5" style={{ color: "#6b7280" }}>
                        最近 10 条上链记录
                    </p>
                </div>
                <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full"
                    style={{ backgroundColor: "rgba(6,214,160,0.1)", border: "1px solid rgba(6,214,160,0.2)" }}
                >
                    <ShieldCheck size={13} style={{ color: "#06d6a0" }} />
                    <span className="text-xs" style={{ color: "#06d6a0" }}>SM2 已签名</span>
                </div>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full text-sm">
                    <thead>
                        <tr style={{ borderBottom: "1px solid rgba(42,48,66,0.6)" }}>
                            <th className="text-left py-2.5 px-3 text-xs font-medium" style={{ color: "#6b7280" }}>ID</th>
                            <th className="text-left py-2.5 px-3 text-xs font-medium" style={{ color: "#6b7280" }}>时间</th>
                            <th className="text-right py-2.5 px-3 text-xs font-medium" style={{ color: "#6b7280" }}>功率 (W)</th>
                            <th className="text-right py-2.5 px-3 text-xs font-medium" style={{ color: "#6b7280" }}>SOC (%)</th>
                            <th className="text-right py-2.5 px-3 text-xs font-medium" style={{ color: "#6b7280" }}>累计 (kWh)</th>
                            <th className="text-left py-2.5 px-3 text-xs font-medium" style={{ color: "#6b7280" }}>TX Hash</th>
                        </tr>
                    </thead>
                    <tbody>
                        {latest.map((r, i) => {
                            const date = new Date(r.timestamp * 1000);
                            return (
                                <motion.tr
                                    key={r.id}
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: 0.5 + i * 0.05 }}
                                    className="transition-colors"
                                    style={{
                                        borderBottom: "1px solid rgba(42,48,66,0.3)",
                                    }}
                                    onMouseEnter={(e) => {
                                        (e.currentTarget as HTMLElement).style.backgroundColor = "rgba(6,214,160,0.04)";
                                    }}
                                    onMouseLeave={(e) => {
                                        (e.currentTarget as HTMLElement).style.backgroundColor = "transparent";
                                    }}
                                >
                                    <td className="py-2.5 px-3" style={{ color: "#8892a4", fontFamily: "var(--font-mono)" }}>
                                        #{r.id}
                                    </td>
                                    <td className="py-2.5 px-3" style={{ color: "#f0f4f8" }}>
                                        {date.getHours().toString().padStart(2, '0')}:{date.getMinutes().toString().padStart(2, '0')}
                                    </td>
                                    <td className="py-2.5 px-3 text-right" style={{ color: r.pvPower > 0 ? "#06d6a0" : "#6b7280", fontFamily: "var(--font-mono)" }}>
                                        {r.pvPower.toFixed(1)}
                                    </td>
                                    <td className="py-2.5 px-3 text-right" style={{ color: "#ffd166", fontFamily: "var(--font-mono)" }}>
                                        {r.battSOC}
                                    </td>
                                    <td className="py-2.5 px-3 text-right" style={{ color: "#118ab2", fontFamily: "var(--font-mono)" }}>
                                        {r.totalEnergy.toFixed(2)}
                                    </td>
                                    <td className="py-2.5 px-3">
                                        <div className="flex items-center gap-1.5">
                                            <span style={{ color: "#8892a4", fontFamily: "var(--font-mono)", fontSize: "12px" }}>
                                                {r.txHash.slice(0, 10)}...{r.txHash.slice(-6)}
                                            </span>
                                            <ExternalLink size={11} style={{ color: "#6b7280" }} />
                                        </div>
                                    </td>
                                </motion.tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </motion.div>
    );
}
