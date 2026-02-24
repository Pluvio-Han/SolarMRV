// 模拟链上数据 — 后续会替换为真实 JSON-RPC 调用

export interface SolarRecord {
    id: number;
    timestamp: number;
    pvPower: number;      // W (已还原)
    pvVoltage: number;    // V
    battSOC: number;      // %
    battVoltage: number;  // V
    totalEnergy: number;  // kWh
    signature: string;
    txHash: string;
}

export interface ChainStatus {
    blockHeight: number;
    recordCount: number;
    nodes: NodeInfo[];
    isConnected: boolean;
}

export interface NodeInfo {
    name: string;
    location: string;
    ip: string;
    status: "online" | "offline" | "syncing";
    blockHeight: number;
}

// 生成 24h 模拟功率数据 (日照曲线)
function generatePowerData(): { time: string; power: number; voltage: number; soc: number }[] {
    const data = [];
    const now = new Date();
    for (let i = 287; i >= 0; i--) {
        const t = new Date(now.getTime() - i * 5 * 60000);
        const hour = t.getHours() + t.getMinutes() / 60;

        // 模拟日照曲线: 6am-6pm 有光照
        let power = 0;
        if (hour >= 6 && hour <= 18) {
            const peak = Math.sin(((hour - 6) / 12) * Math.PI);
            power = peak * 450 * (0.85 + Math.random() * 0.3);
            // 模拟云层遮挡
            if (Math.random() < 0.1) power *= 0.3;
        }

        const voltage = power > 0 ? 17 + Math.random() * 3 : 0;
        const soc = Math.min(100, Math.max(20, 60 + (hour - 12) * 3 + Math.random() * 5));

        data.push({
            time: `${t.getHours().toString().padStart(2, '0')}:${t.getMinutes().toString().padStart(2, '0')}`,
            power: Math.round(power * 100) / 100,
            voltage: Math.round(voltage * 100) / 100,
            soc: Math.round(soc),
        });
    }
    return data;
}

// 生成链上记录
function generateRecords(count: number): SolarRecord[] {
    const records: SolarRecord[] = [];
    const now = Date.now();
    for (let i = count - 1; i >= 0; i--) {
        const ts = Math.floor((now - i * 300000) / 1000);
        const hour = new Date(ts * 1000).getHours();
        const hasSun = hour >= 6 && hour <= 18;
        const peak = hasSun ? Math.sin(((hour - 6) / 12) * Math.PI) : 0;

        records.push({
            id: count - i,
            timestamp: ts,
            pvPower: hasSun ? Math.round(peak * 400 * (0.9 + Math.random() * 0.2) * 100) / 100 : 0,
            pvVoltage: hasSun ? Math.round((17 + Math.random() * 3) * 100) / 100 : 0,
            battSOC: Math.round(Math.min(100, Math.max(20, 55 + (hour - 12) * 3 + Math.random() * 5))),
            battVoltage: Math.round((12.8 + Math.random() * 1.2) * 100) / 100,
            totalEnergy: Math.round((0.5 + (count - i) * 0.02) * 100) / 100,
            signature: `3045022100${Array.from({ length: 60 }, () => Math.floor(Math.random() * 16).toString(16)).join('')}`,
            txHash: `0x${Array.from({ length: 64 }, () => Math.floor(Math.random() * 16).toString(16)).join('')}`,
        });
    }
    return records;
}

export const mockPowerData = generatePowerData();

export const mockRecords = generateRecords(48);

export const mockChainStatus: ChainStatus = {
    blockHeight: 156,
    recordCount: 48,
    isConnected: true,
    nodes: [
        { name: "Gwen", location: "腾讯云·广州", ip: "1.12.43.152", status: "online", blockHeight: 156 },
        { name: "Miles", location: "腾讯云·上海", ip: "106.53.76.27", status: "online", blockHeight: 156 },
        { name: "Peter", location: "DO·新加坡", ip: "206.189.44.223", status: "online", blockHeight: 155 },
    ],
};

// 当前实时数据 (取最新记录)
export const mockCurrentData = {
    pvPower: 356.78,
    pvVoltage: 18.92,
    battSOC: 87,
    battVoltage: 13.65,
    totalEnergy: 1.46,
    lastUpdate: new Date().toISOString(),
};
