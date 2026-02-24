"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  Sun, Zap, Activity, Database,
  Link2, Shield, Clock,
} from "lucide-react";

import StatCard from "@/components/StatCard";
import BatteryGauge from "@/components/BatteryGauge";
import PowerChart from "@/components/PowerChart";
import NodeStatus from "@/components/NodeStatus";
import RecordTable from "@/components/RecordTable";

import {
  mockCurrentData,
  mockPowerData,
  mockRecords,
  mockChainStatus,
} from "@/lib/mock-data";

export default function Dashboard() {
  const [currentTime, setCurrentTime] = useState("");

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setCurrentTime(
        `${now.getFullYear()}-${(now.getMonth() + 1).toString().padStart(2, '0')}-${now.getDate().toString().padStart(2, '0')} ` +
        `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`
      );
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen grid-bg">
      {/* ====== Header ====== */}
      <header className="sticky top-0 z-50" style={{
        backgroundColor: "rgba(10,14,23,0.85)",
        backdropFilter: "blur(16px)",
        borderBottom: "1px solid rgba(42,48,66,0.5)",
      }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <motion.div
              animate={{ rotate: [0, 360] }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
            >
              <Sun size={28} style={{ color: "#ffd166" }} />
            </motion.div>
            <div>
              <h1 className="text-lg font-bold tracking-tight" style={{ color: "#f0f4f8" }}>
                PluvioHan <span style={{ color: "#06d6a0" }}>Solar RWA</span>
              </h1>
              <p className="text-xs" style={{ color: "#6b7280" }}>
                光伏能源 · 链上存证 · 实时监控
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* Clock */}
            <div className="hidden sm:flex items-center gap-2 text-xs" style={{ color: "#8892a4" }}>
              <Clock size={13} />
              <span style={{ fontFamily: "var(--font-mono)" }}>{currentTime}</span>
            </div>

            {/* Chain status indicator */}
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full"
              style={{
                backgroundColor: mockChainStatus.isConnected ? "rgba(6,214,160,0.1)" : "rgba(239,71,111,0.1)",
                border: `1px solid ${mockChainStatus.isConnected ? "rgba(6,214,160,0.3)" : "rgba(239,71,111,0.3)"}`,
              }}
            >
              <span className="w-2 h-2 rounded-full pulse-dot" style={{
                backgroundColor: mockChainStatus.isConnected ? "#06d6a0" : "#ef476f"
              }} />
              <span className="text-xs font-medium" style={{
                color: mockChainStatus.isConnected ? "#06d6a0" : "#ef476f"
              }}>
                {mockChainStatus.isConnected ? "链上同步" : "链断开"}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* ====== Main Content ====== */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-6 space-y-6">

        {/* Row 1: Stat Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard
            title="实时发电功率"
            value={mockCurrentData.pvPower}
            unit="W"
            icon={Zap}
            color="cyan"
            trend="up"
            subtitle={`电压 ${mockCurrentData.pvVoltage}V`}
          />
          <StatCard
            title="光伏电压"
            value={mockCurrentData.pvVoltage}
            unit="V"
            icon={Activity}
            color="blue"
            trend="stable"
          />
          <StatCard
            title="累计发电量"
            value={mockCurrentData.totalEnergy}
            unit="kWh"
            icon={Sun}
            color="amber"
            trend="up"
            subtitle="今日累计"
          />
          <StatCard
            title="链上记录"
            value={mockChainStatus.recordCount}
            unit="条"
            icon={Database}
            color="green"
            trend="up"
            subtitle={`区块高度 #${mockChainStatus.blockHeight}`}
          />
        </div>

        {/* Row 2: Chart + Battery */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2">
            <PowerChart data={mockPowerData} />
          </div>
          <BatteryGauge
            soc={mockCurrentData.battSOC}
            voltage={mockCurrentData.battVoltage}
            isCharging={mockCurrentData.pvPower > 0}
          />
        </div>

        {/* Row 3: Records Table + Node Status */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2">
            <RecordTable records={mockRecords} />
          </div>
          <NodeStatus
            nodes={mockChainStatus.nodes}
            blockHeight={mockChainStatus.blockHeight}
          />
        </div>

        {/* Footer badges */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="flex flex-wrap items-center justify-center gap-4 pt-4 pb-8"
        >
          {[
            { icon: Shield, label: "国密 SM2 签名", color: "#06d6a0" },
            { icon: Link2, label: "FISCO-BCOS 联盟链", color: "#118ab2" },
            { icon: Database, label: "6 节点 PBFT 共识", color: "#ffd166" },
          ].map(({ icon: Icon, label, color }) => (
            <div key={label} className="flex items-center gap-2 px-3 py-1.5 rounded-full text-xs"
              style={{ backgroundColor: "rgba(26,31,46,0.8)", border: "1px solid rgba(42,48,66,0.5)" }}
            >
              <Icon size={13} style={{ color }} />
              <span style={{ color: "#8892a4" }}>{label}</span>
            </div>
          ))}
        </motion.div>
      </main>

      {/* ====== Footer ====== */}
      <footer style={{ borderTop: "1px solid rgba(42,48,66,0.4)" }}>
        <div className="max-w-7xl mx-auto px-6 py-4 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs" style={{ color: "#6b7280" }}>
          <span>© 2026 PluvioHan · 光伏 RWA 物联网数据存证平台</span>
          <span style={{ fontFamily: "var(--font-mono)" }}>
            Powered by FISCO-BCOS v2.11 · EPEVER Tracer-AN
          </span>
        </div>
      </footer>
    </div>
  );
}
