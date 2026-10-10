# ATS-FDM 參考文獻與搜尋指南

## 參、Google Scholar 論文搜尋指南

> [!TIP]
> 以下每個方向我給你 **精準的搜尋關鍵字** + **你應該在那類論文中學到什麼**。建議先掃摘要篩選，選出 6-8 篇精讀。

---

### 方向 1：FPGA 背景建模加速器（你的 TLI-PE 的思想源頭）

**搜尋關鍵字：**
```
"background subtraction" "FPGA" "accelerator"
"Gaussian Mixture Model" "FPGA" "real-time"
"ViBe" "FPGA" "implementation"
```

**你會找到什麼：** GMM（高斯混合模型）和 ViBe 演算法的 FPGA 硬體實現。這些論文解決的問題跟你一模一樣——如何在硬體中做「比簡單幀差更強」的運動偵測。重點關注它們的**記憶體管理策略**（如何在片上存儲背景模型）和**per-pixel 管線化設計**（跟你的 TLI-PE 直接對標）。

**代表性搜索入口：**
- `"ViBe background subtraction FPGA"` → ViBe 的 FPGA 實現，極低記憶體開銷
- `"GMM background model Zynq"` → 在 Zynq 平台上的完整實現

---

### 方向 2：低功耗 Always-On 運動偵測硬體（你的系統級能效定位）

**搜尋關鍵字：**
```
"always-on" "motion detection" "low power" "image sensor"
"wake-up" "vision" "accelerator" "edge"
"ultra-low power" "frame difference" "hardware"
```

**你會找到什麼：** ISSCC / VLSI Symposium 等頂會上，有一類「always-on wake-up vision sensor」的論文。它們的目標跟你完全一致：用極低功耗的硬體做粗略的運動偵測，偵測到了再喚醒後端的重量級 AI 推論。重點學習它們的**功耗預算分析方法**和**系統級 duty-cycling 策略**。

**代表性搜索入口：**
- `"always-on motion detection CMOS image sensor ISSCC"` → sensor-in-pixel 級運動偵測
- `"wake-up accelerator object detection edge AI"` → 系統級 wake-up 架構

---

### 方向 3：Leaky Integrate-and-Fire 硬體實現（你的 TLI-PE 的數學模型）

**搜尋關鍵字：**
```
"leaky integrate and fire" "FPGA" "digital implementation"
"LIF neuron" "hardware" "spiking neural network"
"temporal integration" "motion detection" "neuromorphic"
```

**你會找到什麼：** 你的 TLI-PE 本質上就是一個 LIF（Leaky Integrate-and-Fire）神經元。神經形態計算（Neuromorphic Computing）領域有大量論文討論如何在 FPGA 上高效實現 LIF 神經元陣列。重點學習它們的**衰減因子精度與硬體成本的 trade-off**，以及**大規模 LIF 陣列的記憶體存取策略**（因為你的 TLI-PE 實際上是一個 1920×1080 = 200 萬個 LIF 神經元的陣列）。

**代表性搜索入口：**
- `"digital LIF neuron FPGA resource efficient"` → 資源高效的 LIF 硬體
- `"spiking neural network accelerator FPGA on-chip memory"` → 片上記憶體策略

---

### 方向 4：事件驅動視覺處理硬體（DVS — 你的設計理念的極致版本）

**搜尋關鍵字：**
```
"dynamic vision sensor" "FPGA" "processing pipeline"
"event-driven" "vision" "FPGA" "object detection"
"DVS" "event camera" "hardware accelerator"
```

**你會找到什麼：** Dynamic Vision Sensor（DVS / Event Camera）在每個像素位置獨立偵測亮度變化，只有變化超過閾值時才輸出「事件」。這跟你的 TLI-PE 的 per-pixel 閾值比較在概念上是同構的。DVS 的 FPGA 處理管線論文會教你如何處理**稀疏的、非同步的像素級事件流**，以及如何從事件流中提取 ROI——跟你的 ROI Interrupter 的功能直接對標。

**代表性搜索入口：**
- `"event camera FPGA real-time object detection"` → 事件相機的 FPGA 處理
- `"DVS event-driven ROI extraction hardware"` → 從事件流中提取 ROI

---

### 方向 5：自適應閾值 / 多幀累積的運動偵測（你的 ATS-FSM 的演算法基礎）

**搜尋關鍵字：**
```
"adaptive threshold" "motion detection" "temporal accumulation"
"multi-frame difference" "slow moving object detection"
"sigma-delta background estimation" "hardware"
```

**你會找到什麼：** 這一類論文專門討論如何偵測「用傳統幀差法偵測不到的慢速物體」。Sigma-Delta 背景估計是一種經典的逐像素自適應方法，其硬體實現的論文會告訴你**如何用極少的記憶體和邏輯實現比固定閾值更強的偵測能力**。重點關注其時間常數（time constant）的選擇策略——這跟你的 stride 選擇問題完全等價。

**代表性搜索入口：**
- `"sigma-delta background subtraction FPGA"` → 逐像素自適應背景估計
- `"temporal accumulation slow object detection video surveillance"` → 慢速物體偵測演算法


## 肆、論文閱讀優先順序建議

> [!NOTE]
> 基於你目前的設計階段（微架構雛形已有，需要深化），建議按以下順序攻讀：

| 優先序 | 方向 | 理由 |
|-------|------|------|
| ★★★ | 方向 1（FPGA 背景建模） | 直接對標你的 TLI-PE，學習別人怎麼做 per-pixel 狀態管理 |
| ★★★ | 方向 3（LIF 硬體） | 你的 TLI-PE 就是 LIF，學習衰減精度的工程實作 |
| ★★☆ | 方向 5（自適應閾值） | 你的 ATS-FSM 的演算法理論基礎 |
| ★★☆ | 方向 2（Always-On 運動偵測） | 系統級能效分析方法，論文撰寫時的 comparison baseline |
| ★★☆ | 方向 4（DVS 處理） | 概念同構，能啟發更多設計靈感 |


---

*基於 Pro's Article (Achmadiah et al., 2026) Limitation_02 與你的 ATS-FD 加速器雛形設計。*
