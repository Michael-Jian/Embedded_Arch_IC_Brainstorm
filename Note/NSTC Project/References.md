參考文獻（初始階段 · 4 篇）

> [!NOTE]
> 專案仍在雛形階段，這裡只挑 4 篇「能直接對應核心模組」的文獻，先建立概念，不必精讀。
> 對應關係依據 [ATS-FDM Design.md](ATS-FDM%20Design.md)：ATS-FSM v2、TLI-PE v2、ROI Interrupter v2。
> 文獻資訊（作者、年份、期刊）已用網路搜尋核對；細節公式與數據我只看了摘要，閱讀時請以原文為準。

## 總覽

| # | 文獻 | 對應模組 | 你要從中學到什麼 |
|---|------|---------|----------------|
| 1 | Manzanera & Richefeu, Σ-Δ 背景估計 (2007) | ATS-FSM、TLI-PE | 逐像素「比較 + 遞增/遞減」的極低成本時域估計；多時間尺度 |
| 2 | Cassidy et al., 數位 LIF 神經元 (2013) | TLI-PE | 洩漏（leak）、飽和、閾值的數位硬體化與位寬取捨 |
| 3 | Lichtsteiner, Posch & Delbruck, DVS (2008) | TLI-PE、ROI Interrupter | 逐像素閾值觸發的概念源頭；噪聲與事件稀疏性 |
| 4 | Van Droogenbroeck & Paquot, ViBe 改進 (2012) | ATS-FSM（Drift Guard）、ROI | 背景模型被慢速/靜止物體「污染」、ghost 與更新策略 |

建議閱讀順序：**1 → 2 → 3 → 4**。

---

## 1. Σ-Δ 背景估計：ATS-FSM 與 TLI-PE 的演算法祖先

- **文獻：** A. Manzanera, J. C. Richefeu, "A new motion detection algorithm based on Σ-Δ background estimation," *Pattern Recognition Letters*, vol. 28, no. 3, pp. 320–328, 2007.
- **連結：** [HAL 版本](https://hal.archives-ouvertes.fr/hal-01222650)（另有 ICVGIP 2004 前身論文：[PDF](https://perso.ensta-paris.fr/%7Emanzaner/Publis/icvgip04.pdf)）
- **為什麼選它：** 每個像素只用比較與 ±1 更新來估計背景，記憶體與運算量極小，與你的「Zero-DDR、每時脈一像素」精神一致。作者還擴充成**多個 Σ-Δ 估計器處理不同時間尺度**，這與你的多級 stride 階梯是同一類問題。
- **重點看：**
  - 時間常數（更新頻率）如何決定能偵測的速度範圍 → 對應你的 Stride $S_k$ 與 `shift_bit` 選擇。
  - 為何它在複雜場景中仍有取捨 → 對照你的噪聲地板 $N_f$。
- **已知限制（正好是你的機會）：** 後續綜述指出基本 Σ-Δ 背景容易被慢速或暫停的物體「污染」，這恰好是 ATS-FD 想解決的慢速物體問題。

## 2. 數位 LIF 神經元：TLI-PE 的數學與硬體模型

- **文獻：** A. S. Cassidy et al., "Cognitive Computing Building Block: A Versatile and Efficient Digital Neuron Model for Neurosynaptic Cores," *IJCNN*, 2013.
- **連結：** [IBM Research 頁面](https://research.ibm.com/publications/cognitive-computing-building-block-a-versatile-and-efficient-digital-neuron-model-for-neurosynaptic-cores)
- **為什麼選它：** 你的 TLI-PE 公式 $E_{new}=\text{clamp}((E_{old}\gg s)+\Delta P-N_f,0,65535)$ 本質是 leaky integrate-and-fire。這篇是「LIF 如何用極少數位邏輯實現」的經典範例（摘要稱約 1272 個 ASIC gate），含多種 leak 模式與 reset 模式。
- **重點看：**
  - Leak 的硬體實作方式（是否用移位、是否可配置）→ 對照你的桶型移位器。
  - 飽和/下溢處理與狀態位寬 → 對照你 8-bit→16-bit 的決策。
- **提醒：** 它是神經形態晶片核心，不是影像管線；只借「單元設計」，不必看網路層級。

## 3. DVS 事件相機：逐像素閾值與噪聲的概念源頭

- **文獻：** P. Lichtsteiner, C. Posch, T. Delbruck, "A 128×128 120 dB 15 µs Latency Asynchronous Temporal Contrast Vision Sensor," *IEEE JSSC*, vol. 43, no. 2, pp. 566–576, 2008.
- **連結：** [AIT 文獻記錄](https://publications.ait.ac.at/en/publications/a-128x128-120db-15%C2%B5s-latency-asynchronous-temporal-contrast-visio/)
- **為什麼選它：** DVS 是「每個像素各自比較變化量與閾值，超過才輸出」的原型，與 TLI-PE 的 per-pixel $E>T_{pixel}$ 判定概念同構；你的設計可視為**幀式、可累積的 DVS 近似**。
- **重點看：**
  - 閾值（contrast threshold）與像素間失配、背景噪聲事件的關係 → 支持你加入噪聲地板與 Temporal Persistence Filter 的理由。
  - 輸出是稀疏事件而非整幀 → 啟發 ROI Interrupter 只處理「有事發生」的區域。
- **提醒：** 這是類比感測器電路論文，電路細節可略過，抓系統概念即可。

## 4. ViBe 改進：背景污染、更新策略與慢速物體

- **文獻：** M. Van Droogenbroeck, O. Paquot, "Background Subtraction: Experiments and Improvements for ViBe," *CVPR Workshops (Change Detection Workshop)*, pp. 32–37, 2012. DOI: 10.1109/CVPRW.2012.6238924
- **連結：** [作者頁面](https://www.telecom.uliege.be/publi/publications/mvd/VanDroogenbroeck2012Background/index.html)
- **為什麼選它：** ViBe 是低成本、逐像素的背景模型，這篇討論**更新遮罩與分割遮罩分離**、抑制內部邊界傳播等改進。你的「何時更新 BRAM_Ref（WE 閘控）」本質上就是背景更新策略問題，慢速物體被吞進背景是共同痛點。
- **重點看：**
  - 「用於更新的遮罩」與「用於輸出的遮罩」為何要分開 → 啟發 ATS-FSM 的 WE 決策不應只看同一個活動量指標。
  - 後處理（連通元件）如何降低誤報 → 對照 ROI 的持續性濾波與網格分割。

---

## 之後再補（暫不需要）

- Always-on / wake-up 視覺系統的功耗分析（寫論文能效章節時用）
- Zynq PS-PL、AXI-Lite 中斷、DPU 整合的工程參考（進入實作階段時用）
- ROI-based edge AI 的系統級能效比較

*基於 Pro's Article (Achmadiah et al., 2026) Limitation_02 與你的 ATS-FD 加速器雛形設計。*
