import os

filepath = "/Users/michaeljian/Documents/Github/Embedded_Arch_IC_Brainstorm/Note/Special Project/Experiment Design.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Section 0
content = content.replace(
    "| 輕量模型 | MobileNetV2 | **MobileNetV2**（保留） | 運算子集合與 ResNet 重疊（都有殘差相加），硬體成本低 |",
    "| 輕量模型 | MobileNetV2 | **MobileNetV1** | 直接維持教授版本，使用 Transfer Learning (Feature Extraction) |"
)
content = content.replace(
    "| 投稿 | 三個會議並列 | **三擇一（建議 AICAS）** | 三個截稿日都早於 GLSVLSI 放榜 → 同一篇不能一稿多投，見 §6 |",
    "| 投稿 | 三個會議並列 | **GLSVLSI (首選目標)** | 三個截稿日相近，同一篇不能一稿多投，見 §6 |"
)

# 2. Section 3.2
content = content.replace(
    "我們直接向教授拿他的預訓練權重，凍結（Freeze）前面的卷積層",
    "我們直接向教授拿他的預訓練權重與 4K 測試影片（預計 2026/10/15 取得），並凍結（Freeze）前面的卷積層（Transfer Learning Feature Extraction）"
)

# 3. Replace all Jetson Nano with Jetson Orin Nano
content = content.replace("NVIDIA Jetson Nano", "NVIDIA Jetson Orin Nano")
content = content.replace("| Jetson Nano |", "| Jetson Orin Nano |")
content = content.replace("Jetson / Hailo", "Jetson Orin Nano / Hailo")

# 4. Section 6.2 and 6.3 MobileNetV2 -> MobileNetV1
content = content.replace("MobileNetV2，Spatial", "MobileNetV1，Spatial")
content = content.replace("跑 MobileNetV2", "跑 MobileNetV1")
content = content.replace("Temporal 模式（MobileNetV2）", "Temporal 模式（MobileNetV1）")
content = content.replace("微調 5 類 MobileNetV2 / ResNet18", "微調 5 類 MobileNetV1 / ResNet18")
content = content.replace("整合 MobileNetV2", "整合 MobileNetV1")

# 5. Risk A7
content = content.replace(
    "| A7 Jetson Nano 不支援 INT8 | ⚠️ 未解決 | 標註 FP16；或改用教授實驗室的 Orin Nano（見 §8） |",
    "| A7 Jetson Orin Nano 支援 INT8 | ✅ 已解決 | 確認教授實驗室有 Jetson Orin Nano，原生支援 INT8，且與教授論文同平台 |"
)

# 6. Remove Section 8
idx = content.find("## 8. 待確認")
if idx != -1:
    content = content[:idx].strip() + "\n"

# 7. Also update the title version if needed? I'll just leave it as v0.2 but maybe we can update it in the UI text. 
# It says v0.2 in line 1. I'll leave the title as is.

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Modification done.")
