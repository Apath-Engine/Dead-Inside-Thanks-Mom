import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="Dead Inside, Thanks Mom", page_icon="🌹", layout="centered"
)

st.title("🌹 Dead Inside, Thanks Mom")
st.markdown("親子関係の揺らぎと感情のダイナミクスを非線形カオスモデルでシミュレーションするアプリです。")

# --- スマホでも隠れないように、メイン画面にパラメータ設定を配置 ---
st.markdown("### ⚙️ パラメータ設定")

col1, col2 = st.columns(2)

with col1:
  st.markdown("#### 初期値")
  init_m = st.slider("初期干渉 (M)", 0.0, 5.0, 1.0, 0.1)
  init_s = st.slider("初期ストレス (S)", 0.0, 5.0, 2.0, 0.1)
  init_r = st.slider("初期自立 (R)", 0.0, 5.0, 0.5, 0.1)

with col2:
  st.markdown("#### モデル係数")
  alpha = st.slider("親の干渉減衰 (alpha)", 0.0, 2.0, 0.5, 0.05)
  kappa = st.slider("ストレス影響係数 (kappa)", 0.0, 2.0, 1.0, 0.05)
  gamma = st.slider("自立促進係数 (gamma)", 0.0, 2.0, 0.5, 0.05)

# シミュレーション期間
t_max = st.slider("シミュレーション期間 (Time)", 10, 100, 50, 5)

# --- モデル計算部分 (例) ---
time_pts = np.linspace(0, t_max, 500)
M_curve = init_m * np.exp(alpha * time_pts * 0.05) * (1 + 0.1 * init_s)
S_curve = init_s * np.exp(kappa * time_pts * 0.06)
R_curve = (
    init_r
    * np.ones_like(time_pts)
    * (1 - 0.01 * time_pts * gamma)
)

if init_s > 1.5 and init_m > 0.8:
  diagnosis = "⚠️ 【過剰干渉フェーズ】"
else:
  diagnosis = "✨ 【均衡・安定フェーズ】"

st.markdown(f"### 診断結果: {diagnosis}")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(time_pts, M_curve, label="干渉 (M)", color="#d9534f")
ax.plot(time_pts, S_curve, label="ストレス (S)", color="#f0ad4e")
ax.plot(time_pts, R_curve, label="自立 (R)", color="#5cb85c")
ax.set_title("Emotional Dynamics Over Time")
ax.set_xlabel("Time")
ax.set_ylabel("Level")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.6)

st.pyplot(fig)
