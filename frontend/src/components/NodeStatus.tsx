"use client";

import { motion } from "framer-motion";
import { Server, Wifi, WifiOff, ArrowUpDown } from "lucide-react";
import type { NodeInfo } from "@/lib/mock-data";

interface NodeStatusProps {
    nodes: NodeInfo[];
    blockHeight: number;
}

export default function NodeStatus({ nodes, blockHeight }: NodeStatusProps) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="card-glow p-6"
        >
            <div className="flex items-center justify-between mb-5">
                <h3 className="text-base font-semibold" style={{ color: "#f0f4f8" }}>
                    联盟链节点状态
                </h3>
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-full"
                    style={{ backgroundColor: "rgba(6,214,160,0.1)", border: "1px solid rgba(6,214,160,0.2)" }}
                >
                    <ArrowUpDown size={13} style={{ color: "#06d6a0" }} />
                    <span className="text-xs font-medium" style={{ color: "#06d6a0", fontFamily: "var(--font-mono)" }}>
                        #{blockHeight}
                    </span>
                </div>
            </div>

            <div className="space-y-3">
                {nodes.map((node, i) => (
                    <motion.div
                        key={node.name}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.4 + i * 0.1 }}
                        className="flex items-center justify-between p-3 rounded-xl transition-colors"
                        style={{ backgroundColor: "rgba(17,24,39,0.5)", border: "1px solid rgba(42,48,66,0.4)" }}
                    >
                        <div className="flex items-center gap-3">
                            <div className="p-2 rounded-lg" style={{
                                backgroundColor: node.status === "online" ? "rgba(6,214,160,0.1)" : "rgba(239,71,111,0.1)"
                            }}>
                                <Server size={16} style={{
                                    color: node.status === "online" ? "#06d6a0" : "#ef476f"
                                }} />
                            </div>

                            <div>
                                <div className="flex items-center gap-2">
                                    <span className="text-sm font-medium" style={{ color: "#f0f4f8" }}>
                                        {node.name}
                                    </span>
                                    <span className={`w-1.5 h-1.5 rounded-full ${node.status === "online" ? "pulse-dot" : ""}`}
                                        style={{ backgroundColor: node.status === "online" ? "#06d6a0" : "#ef476f" }}
                                    />
                                </div>
                                <p className="text-xs" style={{ color: "#6b7280" }}>
                                    {node.location}
                                </p>
                            </div>
                        </div>

                        <div className="text-right">
                            <div className="flex items-center gap-1.5 justify-end">
                                {node.status === "online" ? (
                                    <Wifi size={12} style={{ color: "#06d6a0" }} />
                                ) : (
                                    <WifiOff size={12} style={{ color: "#ef476f" }} />
                                )}
                                <span className="text-xs" style={{
                                    color: node.status === "online" ? "#06d6a0" : "#ef476f"
                                }}>
                                    {node.status === "online" ? "在线" : "离线"}
                                </span>
                            </div>
                            <p className="text-xs mt-0.5" style={{ color: "#6b7280", fontFamily: "var(--font-mono)" }}>
                                #{node.blockHeight}
                            </p>
                        </div>
                    </motion.div>
                ))}
            </div>

            {/* Consensus info */}
            <div className="mt-4 pt-3 flex justify-between text-xs" style={{ borderTop: "1px solid rgba(42,48,66,0.5)" }}>
                <span style={{ color: "#6b7280" }}>共识算法</span>
                <span style={{ color: "#f0f4f8" }}>PBFT</span>
            </div>
            <div className="flex justify-between text-xs mt-1">
                <span style={{ color: "#6b7280" }}>节点总数</span>
                <span style={{ color: "#f0f4f8" }}>{nodes.length * 2} (每机构 2 节点)</span>
            </div>
        </motion.div>
    );
}
