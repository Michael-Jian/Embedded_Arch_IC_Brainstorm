參考文獻（初始階段 · 4 篇 · 近 10 年 IEEE）

> [!NOTE]
> 專案仍在雛形階段，這裡只挑 4 篇「能直接對應核心模組」的文獻，先建立概念，不必精讀。
> 對應關係依據 [Experiment Design.md](Experiment%20Design.md)：ATS-FSM v2、TLI-PE v2、ROI Interrupter v2。
> 4 篇皆為 IEEE 期刊／會議論文，發表於 2019–2021。作者、年份、卷期頁碼、DOI 已用網路搜尋核對；內容只看過摘要與書目頁，閱讀時請以原文為準。
> 舊版（Σ-Δ 2007、數位 LIF 2013、DVS 2008、ViBe 2012）因年代較舊已移除；它們仍是概念源頭，需要時可在論文的 Background 一節補引。

## 總覽

| # | 文獻 | 對應模組 | 你要從中學到什麼 |
|---|------|---------|----------------|
| 1 | Dorudian et al., Adaptive Blind Update (IEEE Sensors J., 2019) | ATS-FSM（Stride 階梯、Drift Guard） | 依物體速度調整背景更新頻率；靜止／慢速物體被吞進背景與 ghost 的取捨 |
| 2 | Frenkel et al., ODIN 數位脈衝神經形態處理器 (IEEE TBCAS, 2019) | TLI-PE | 數位 LIF 神經元的硬體化：洩漏、閾值、位寬與面積／能耗取捨 |
| 3 | Linares-Barranco et al., DVS 事件濾波 FPGA 函式庫 (IEEE Access, 2019) | TLI-PE（噪聲地板、持續性濾波）、ROI | 背景活動（噪聲）濾波、像素遮罩、運動偵測的 FPGA 實作與延遲 |
| 4 | Scherer et al., Always-on 事件式相機 (IEEE I2MTC, 2021) | ROI Interrupter、系統層級 | 以運動偵測觸發下游處理的 always-on 節點；偵測模式 vs 全幀模式的功耗 |

建議閱讀順序：**1 → 2 → 3 → 4**。

---

## 1. Adaptive Blind Update：ATS-FSM 的更新策略對照

- **文獻：** N. Dorudian, S. Lauria, S. Swift, "Moving Object Detection Using Adaptive Blind Update and RGB-D Camera," *IEEE Sensors Journal*, vol. 19, no. 18, pp. 8191–8201, 2019. DOI: [10.1109/JSEN.2019.2920515](https://doi.org/10.1109/JSEN.2019.2920515)
- **連結：** [Brunel 典藏全文](https://bura.brunel.ac.uk/handle/2438/18641)
- **為什麼選它：** 它的核心是**依背景變化與物體速度，動態調整背景模型的更新頻率**，讓靜止物體能被吸收、同時減少 ghost。這與你的 ATS-FSM（多級 Stride 階梯 + 何時拉起 BRAM_Ref 的 WE）是同一個問題：更新太勤會把慢速物體吞掉，太慢則被光照漂移淹沒。
- **重點看：**
  - 更新頻率如何隨速度／背景變化調整 → 對應你的 Stride $S_k$ 切換條件與遲滯（hysteresis）設計。
  - 靜止物體何時該被納入背景 → 對照 Drift Guard 的觸發條件。
- **提醒：** 它用 RGB-D 相機與軟體實作，不是低功耗硬體；只借「自適應更新」的概念，深度資訊與影像處理細節可略過。

## 2. ODIN：數位 LIF 神經元的硬體實作

- **文獻：** C. Frenkel, M. Lefebvre, J.-D. Legat, D. Bol, "A 0.086-mm² 12.7-pJ/SOP 64k-Synapse 256-Neuron Online-Learning Digital Spiking Neuromorphic Processor in 28-nm CMOS," *IEEE Transactions on Biomedical Circuits and Systems*, vol. 13, no. 1, pp. 145–158, 2019.
- **連結：** [arXiv 預印本](https://arxiv.org/abs/1804.07858)（Verilog 原始碼公開：[tinyODIN](https://github.com/ChFrenkel/tinyODIN)）
- **為什麼選它：** 你的 TLI-PE 公式 $E_{new}=\text{clamp}((E_{old}\gg s)+\Delta P-N_f,0,65535)$ 本質是 leaky integrate-and-fire。ODIN 是「極小面積、純數位 LIF 神經元」的代表，神經元可配置為標準 LIF，且 RTL 公開，可直接對照你的桶型移位器與狀態位寬。
- **重點看：**
  - 膜電位的洩漏與閾值比較如何用最少的數位邏輯實現 → 對照你的 shift-leak 與 clamp。
  - 神經元狀態位寬、面積與能耗的取捨 → 對照你 8-bit → 16-bit 的決策。
- **提醒：** 它是神經形態晶片，重點在突觸與線上學習；只借「單一神經元單元」的設計，不必看網路與學習規則。

## 3. DVS 事件濾波的 FPGA 函式庫：噪聲地板與持續性濾波

- **文獻：** A. Linares-Barranco, F. Perez-Pena, D. P. Moeys, F. Gomez-Rodriguez, G. Jimenez-Moreno, S.-C. Liu, T. Delbruck, "Low Latency Event-Based Filtering and Feature Extraction for Dynamic Vision Sensors in Real-Time FPGA Applications," *IEEE Access*, vol. 7, pp. 134926–134942, 2019. DOI: [10.1109/ACCESS.2019.2941282](https://doi.org/10.1109/ACCESS.2019.2941282)
- **連結：** [Universidad de Cádiz 典藏](https://rodin.uca.es/handle/10498/22164)
- **為什麼選它：** DVS 的「逐像素閾值觸發」是 TLI-PE 判定 $E>T_{pixel}$ 的概念原型，而這篇把**背景活動（噪聲）濾波、像素遮罩、物體運動偵測、追蹤**做成 FPGA 函式庫（摘要稱延遲低於 300 ns）。它直接回答你的設計會遇到的工程問題：噪聲事件怎麼壓、熱像素怎麼遮、怎麼在 FPGA 上低延遲實作。
- **重點看：**
  - 背景活動濾波的時空判準與所需記憶體 → 支持你的噪聲地板 $N_f$ 與 Temporal Persistence Filter。
  - 像素遮罩（masking）的作法 → 可借鏡處理壞點／熱像素。
  - 事件稀疏輸出如何接到後續偵測 → 啟發 ROI Interrupter 只處理「有事發生」的區域。
- **提醒：** 輸入是 DVS 事件流，你的是幀式灰階；請抓濾波判準與硬體架構，不必看事件相機本身的電路。

## 4. Always-on 事件式相機節點：ROI Interrupter 的系統層級對照

- **文獻：** M. Scherer, P. Mayer, A. Di Mauro, M. Magno, L. Benini, "Towards Always-on Event-based Cameras for Long-lasting Battery-operated Smart Sensor Nodes," *IEEE International Instrumentation and Measurement Technology Conference (I2MTC)*, 2021. DOI: [10.1109/I2MTC50364.2021.9460037](https://doi.org/10.1109/I2MTC50364.2021.9460037)
- **連結：** [Bologna 典藏記錄](https://cris.unibo.it/handle/11585/870372)
- **為什麼選它：** 它的主題是「用低功耗運動偵測模式來**觸發**後續處理，而不是持續全幀運算」，摘要報告運動偵測模式約 1.8 mW、全幀 15 FPS 約 5.5 mW。這與你的架構目標一致：PL 端先做 Zero-DDR 偵測，有事才用中斷喚醒 PS 端的 MobileNet 分類器。
- **重點看：**
  - 偵測模式與全幀模式的功耗比 → 可作為你能效章節的比較基準與敘述框架。
  - 以背景相減做運動偵測、並可設定更新（refresh）率來換取靈敏度 → 對照你的 Stride 與偵測靈敏度取捨。
- **提醒：** 這是會議論文、平台層級的工作；摘要中的單晶片估計值（"400W"）疑為排版錯誤（應為 µW），引用數字前請對照原文。

---

## 之後再補（暫不需要）

- Always-on / wake-up 視覺系統的功耗分析（寫論文能效章節時用）
- Zynq PS-PL、AXI-Lite 中斷、DPU 整合的工程參考（進入實作階段時用）
- ROI-based edge AI 的系統級能效比較
- 概念源頭（Background 一節可引）：Σ-Δ 背景估計（Manzanera & Richefeu, 2007）、DVS（Lichtsteiner et al., 2008）、ViBe（Barnich & Van Droogenbroeck, 2011；Van Droogenbroeck & Paquot, 2012）

*基於 Pro's Article (Achmadiah et al., 2026) Limitation_02 與你的 ATS-FD 加速器雛形設計。*
