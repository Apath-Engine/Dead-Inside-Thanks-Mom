import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="Dead Inside, Thanks Mom", page_icon="🥀", layout="centered"
)

st.title("🥀 Dead Inside, Thanks Mom")
st.markdown(
    "親子関係の揺らぎと感情のダイナミクスを非線形カオスモデルでシミュレーションするアプリです。"
)

# スライダー（スマホでも操作しやすい形）
st.sidebar.header("🎛️ パラメータ設定")

st.sidebar.subheader("初期値")
M_init = st.sidebar.slider(
    "初期干渉 (M)", min_value=0.0, max_value=10.0, value=1.0, step=0.1
)
S_init = st.sidebar.slider(
    "初期ストレス (S)", min_value=0.0, max_value=10.0, value=2.0, step=0.1
)
R_init = st.sidebar.slider(
    "初期自立 (R)", min_value=0.0, max_value=1.0, value=0.5, step=0.05
)

st.sidebar.subheader("モデル係数")
alpha = st.sidebar.slider("親の干渉減衰 (alpha)", 0.0, 2.0, 0.5, 0.05)
kappa = st.sidebar.slider("ストレス影響係数 (kappa)", 0.0, 5.0, 1.0, 0.1)
beta = st.sidebar.slider("ストレス増加係数 (beta)", 0.0, 5.0, 1.0, 0.1)
delta = st.sidebar.slider("ストレス発散係数 (delta)", 0.0, 2.0, 0.5, 0.05)
gamma = st.sidebar.slider("自立回復係数 (gamma)", 0.0, 2.0, 0.3, 0.05)


# 微分方程式モデル
def family_recovery_model(t, y):
  M, S, R = y
  dm_dt = -alpha * M + kappa * S * (1 - R)
  ds_dt = beta * M - delta * S
  dr_dt = gamma * (1 - R) * S - 0.2 * M
  return [dm_dt, ds_dt, dr_dt]


# シミュレーション実行
t_span = (0, 50)
t_eval = np.linspace(0, 50, 500)
y0 = [M_init, S_init, R_init]

sol = solve_ivp(
    family_recovery_model, t_span, y0, t_eval=t_eval, method="RK45"
)

# 状態判定
final_M = sol.y[0][-1]
final_S = sol.y[1][-1]
final_R = sol.y[2][-1]

status_text = "【通常状態】"
if final_S > 5.0 and final_R < 0.3:
  status_text = "💡 【膠着状態】（メンタル限界・要距離感調整）"
elif final_R >= 0.7:
  status_text = "✨ 【完全自立・平和的解放】"
elif final_M > 6.0:
  status_text = "⚠️ 【過剰干渉フェーズ】"

st.markdown(f"### 診断結果: **{status_text}**")

# グラフ描画
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(sol.t, sol.y[0], label="干渉 (M)", color="#ff4b4b", linewidth=2)
ax.plot(sol.t, sol.y[1], label="ストレス (S)", color="#ffa15a", linewidth=2)
ax.plot(sol.t, sol.y[2], label="自立度 (R)", color="#00cc96", linewidth=2)
ax.set_title("Emotional Dynamics Over Time")
ax.set_xlabel("Time")
ax.set_ylabel("Level")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.6)

st.pyplot(fig)
