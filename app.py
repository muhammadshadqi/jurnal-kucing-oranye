import streamlit as st
import io, traceback, datetime
import pandas as pd
import numpy as np

# ── Logo (base64 embedded) ───────────────────────────────────────────────────
LOGO_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAASwAAAEsCAMAAABOo35HAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJ"
    "bWFnZVJlYWR5ccllPAAAAyBpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdp"
    "bj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6"
    "eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEz"
    "NDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJo"
    "dHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlw"
    "dGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAv"
    "IiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RS"
    "ZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpD"
    "cmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBXaW5kb3dzIiB4bXBNTTpJbnN0YW5jZUlE"
    "PSJ4bXAuaWlkOjgzNzk3NTY5NkY0MTExRUFCNDg2ODU0RkQwMjkzMzMwIiB4bXBNTTpEb2N1bWVu"
    "dElEPSJ4bXAuZGlkOjgzNzk3NTZBNkY0MTExRUFCNDg2ODU0RkQwMjkzMzMwIj4gPHhtcE1NOkRl"
    "cml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6ODM3OTc1Njc2RjQxMTFFQUI0ODY4"
    "NTRGRDI5MzMzMCIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDo4Mzc5NzU2ODZGNDExMUVBQjQ4"
    "Njg1NEZEMDI5MzMzMCIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0"
    "YT4gPD94cGFja2V0IGVuZD0iciI/PgH//v38+/r5+Pf29fTz8vHw7+7t7Ovq6ejn5uXk4+Lh4N/e"
    "3dzb2tnY19bV1NPS0dDPzs3My8rJyMfGxcTDwsHAv769vLu6ubi3trW0s7KxsK+urayrqqmop6al"
    "pKOioaCfnp2cm5qZmJeWlZSTkpGQj46NjIuKiYiHhoWEg4KBgH9+fXx7enl4d3Z1dHNycXBvbm1s"
    "a2ppaGdmZWRjYmFgX15dXFtaWVhXVlVUU1JRUE9OTUxLSklIR0ZFRENCQUA/Pj08Ozo5ODc2NTQz"
    "MjEwLy4tLCsqKSgnJiUkIyIhIB8eHRwbGhkYFxYVFBMSERAPDg0MCwoJCAcGBQQDAgEAACH5BAAA"
    "AAAALAAAAAASwBLAAAf/gACCg4SFhoeIiYqLjI2Oj4IBkZKTlJWWl5iZmpucnZ6foKGio6SlpqeD"
    "qKmqq6ytrq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g"
    "4eLj5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+/wABChxIsKDBgwgTKlzIsKHDhxAjSpxIsaLF"
    "ixgzatzIsaPHjyBDihxJsqTJkyhTqlzJsqXLlzBjypxJs6bNmzhz6tzJs6fPn0CDCh1KtKjRo0iT"
    "Kl3KtKnTp1CjSp1KtarVq1izat3KtavXr2DDih1LtqzZs2jTql3Ltq3bt3Djyp1Lt67du3jz6t3L"
    "t6/fv4ADCx5MuLDhw4gTK17MuLHjx5AjS55MubLly5gza97MubPnz6BDix5NurTp06hTq17NurXr"
    "17Bjy55Nu7bt27hz697Nu7fv38CDCx9OvLjx48iTK1/OvLnz59CjS59Ovbr169iza9/Ovbv37+DD"
    "ix9Pvrz58+jTq1/Pvr379/Djy59Pv779+/jz69/Pv7///wAGKOCABBZo4IEIJqjgggw26OCDEEYo"
    "4YQUVmjhhRhmqOGGHHbo4YcghijiiCSWaOKJKKao4oostujiizDGKOOMNNZo44045qjjjjz26OOP"
    "QAYp5JBEFmnkkUgmqeSSTDbp5JNQRinllFRWaeWVWGap5ZZcdunll2CGKeaYZJZp5plopqnmmmy2"
    "6eabcMYp55x01mnnnXjmqeeefPbp559ABinkkIQWauihiCaq6KKMNuroo5BGKumklFZq6aWYZqrp"
    "ppx26umnoIYq6qiklmrqqaimquqqrLbq6quwxirrrLTWauutuOaq66689urrr8AGK+ywxBZr7LHI"
    "Jqvsssw26+yz0EYr7bTUVmvttdhmq+223Hbr7bfghivuuOSWa+656Kar7rrstuvuu/DGK++89NZr"
    "77345qvvvvz26++/AAco8MAEF2zwwQgnrPDCDDfs8MMQRyzxxBRXbPHFGGes8cYcd+zxxyCHLPLI"
    "JJds8skop6zyyiy37PLLMMcs88w012zzzTjnrPPOPPfs889ABy300EQXbfTRSCet9NJMN+3001BH"
    "LfXUVFdt9dVYZ6311lx37fXXYIct9thkl2322WinrfbabLft9ttwxy333HTXbffdeOet99589+33"
    "34AHLvjghBdu+OGIJ6744ow37vjjkEcu+eSUV2755ZhnrvnmnHfu+eeghy766KSXbvrpqKeu+uqs"
    "t+7667DHLvvstNdu++2456777rz37vvvwAcv/PDEF2/88cgnr/zyzDfv/PPQRy/99NRXb/312Gev"
    "/fbcd+/99+CHIAAh+QQAAAAALAASABIAAAAS/4BjAJi5IM1Ao9lkyolnap0IADs="
)

st.set_page_config(
    page_title="Astro Pricing Tools", page_icon="🚀",
    layout="wide", initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;600;700;800&family=Nunito:wght@600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Nunito Sans', sans-serif; }
[data-testid="stSidebar"] { background: linear-gradient(180deg,#003DA6 0%,#0055CC 60%,#0083FF 100%); }
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.25) !important; }
.astro-header { background: linear-gradient(135deg,#003DA6 0%,#0083FF 100%); border-radius:14px; padding:24px 32px; margin-bottom:24px; }
.astro-header h1 { font-family:'Nunito',sans-serif; font-weight:800; font-size:1.8rem; color:white; margin:0; }
.astro-header p { color:rgba(255,255,255,0.82); margin:4px 0 0 0; font-size:0.9rem; }
.stButton>button { background:linear-gradient(135deg,#0083FF,#003DA6); color:white !important; font-family:'Nunito',sans-serif; font-weight:700; font-size:1rem; border:none; border-radius:10px; padding:10px 28px; width:100%; }
[data-testid="stDownloadButton"] button { background:#00a651 !important; color:white !important; font-family:'Nunito',sans-serif !important; font-weight:700 !important; border-radius:10px !important; width:100%; font-size:1rem !important; }
[data-testid="stFileUploader"] { background:#f0f6ff; border:2px dashed #0083FF; border-radius:10px; padding:6px; }
.stAlert { border-radius:10px !important; }
.stTabs [data-baseweb="tab"] { font-family:'Nunito',sans-serif; font-weight:700; }
.hint-box { background:#E6F2FF; border-left:4px solid #0083FF; border-radius:0 8px 8px 0; padding:12px 16px; margin-bottom:16px; font-size:0.88rem; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:16px 0 8px;">
        <img src="data:image/png;base64,{LOGO_B64}"
             style="width:72px;height:72px;object-fit:contain;margin-bottom:8px;display:block;margin-left:auto;margin-right:auto;"/>
        <div style="font-family:'Nunito',sans-serif;font-size:1.1rem;font-weight:800;color:white;">Astro Pricing Tools</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Nav",
        ["📊 GP Bridge","📈 PI Analyzer","🧮 Pricing Simulator","🗄️ Query Reference"],
        label_visibility="collapsed")
    st.markdown("---")
    st.markdown('<div style="font-size:0.75rem;color:rgba(255,255,255,0.6);line-height:1.8;">Output: Excel (.xlsx)<br>Input: CSV atau Excel<br>Engine: Python + openpyxl</div>',
                unsafe_allow_html=True)

# ── Helpers ──────────────────────────────────────────────────────────────────
def color_delta(val):
    if pd.isna(val): return ""
    try:
        v = float(str(val).replace("%","").replace(",","").replace("pp","").replace("+",""))
        return "color:#1A7A4A;font-weight:600;background:#eafaf1" if v > 0 \
          else ("color:#C0392B;font-weight:600;background:#fdf0ee" if v < 0 else "")
    except: return ""

def style_df(df, cols):
    """pandas ≥ 2.1 uses .map() instead of deprecated .applymap()"""
    try:
        return df.style.map(color_delta, subset=cols)
    except AttributeError:
        return df.style.applymap(color_delta, subset=cols)

def fmt_idr(v):
    try: return f"Rp {float(v):,.0f}"
    except: return str(v)

# ── DOW helpers for Query Reference ─────────────────────────────────────────
DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
DOW_MAP = {d: i for i, d in enumerate(DAYS)}  # Monday=0 ... Sunday=6

def next_dow(ref_date: datetime.date, dow: int) -> datetime.date:
    """Return the next (or same) date that falls on dow (0=Mon)"""
    days_ahead = (dow - ref_date.weekday()) % 7
    return ref_date + datetime.timedelta(days=days_ahead)

def find_allowed_dates(dow: int, months_back: int = 6) -> list:
    today = datetime.date.today()
    start = today - datetime.timedelta(weeks=months_back*4)
    result = []
    d = next_dow(start, dow)
    while d <= today + datetime.timedelta(weeks=52):
        result.append(d)
        d += datetime.timedelta(weeks=1)
    return result


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — GP Bridge
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 GP Bridge":
    st.markdown("""<div class="astro-header">
    <h1>📊 GP Bridge & PVM Decomposition</h1>
    <p>Price · Volume · Mix · COGS · New & Churned SKU Effect</p></div>""",
    unsafe_allow_html=True)

    # Format hint — always visible
    st.markdown("""<div class="hint-box">
    <b>Kolom wajib:</b> <code>week_key</code>, <code>next_week</code>, <code>product_id</code>,
    <code>product_name</code>, <code>pricing_bl_25</code>, <code>qty</code>, <code>qty1</code>,
    <code>selling_price</code>, <code>selling_price1</code>, <code>cost_price</code>, <code>cost_price1</code><br>
    <b>Opsional:</b> <code>comp_price</code>, <code>comp_price1</code>, <code>pi</code>, <code>pi1</code>,
    <code>avg_stock</code>, <code>pareto_classification</code>
    </div>""", unsafe_allow_html=True)

    st.dataframe(pd.DataFrame({
        "week_key":  ["2026-04-07","2026-04-07","2026-04-07"],
        "next_week": ["2026-04-14","2026-04-14","2026-04-14"],
        "product_id":["1001","1002","1003"],
        "product_name":["Indomie Goreng","Ayam Fillet 500g","Tomat 500g"],
        "pricing_bl_25":["Dry","Frozen","Fresh"],
        "qty":[500,120,300], "qty1":[480,135,290],
        "selling_price":[3500,42000,8500], "selling_price1":[3500,43000,8500],
        "cost_price":[2800,35000,6200],    "cost_price1":[2850,36000,6400],
    }), hide_index=True, use_container_width=True)

    uploaded = st.file_uploader("Upload file CSV atau Excel (Q1 — GP Bridge)",
                                 type=["csv","xlsx","xls"], key="pvm_file")
    if uploaded:
        st.success(f"✅ {uploaded.name} ({uploaded.size/1024:.1f} KB)")
        if st.button("▶ Run GP Bridge Analysis", key="run_pvm"):
            with st.spinner("Memproses..."):
                try:
                    import pvm_revised as _pvm
                    file_bytes = uploaded.read()
                    excel_bytes, out_filename = _pvm.run_pvm(file_bytes, uploaded.name)

                    st.success("✅ Selesai!")
                    st.download_button("⬇️ Download Excel (GP Bridge)", data=excel_bytes,
                        file_name=out_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="dl_pvm")

                    st.markdown("---")
                    st.markdown("### 📊 Summary Preview")

                    buf2 = io.BytesIO(file_bytes)
                    ext  = uploaded.name.rsplit(".",1)[-1].lower()
                    df_raw = pd.read_csv(buf2) if ext=="csv" else pd.read_excel(buf2)
                    df_raw = _pvm.ensure_cols(df_raw)
                    p1c, p2c = _pvm.detect_period(df_raw)
                    if p1c is None: p1c, p2c = "week_key","next_week"
                    df_e  = _pvm.enrich(df_raw, p1c, p2c)
                    pvm   = _pvm.compute_pvm(df_e)
                    BLS   = ["Dry","Fresh","Frozen","PL"]

                    # Tabel 1 — Margin Bridge pp
                    st.markdown("#### Tabel 1 — Margin Bridge per BL (pp)")
                    rows1 = []
                    for bl in BLS + ["TOTAL"]:
                        p = pvm[bl]
                        rows1.append({
                            "BL": bl,
                            "Margin P1": f"{p['m_base']*100:.2f}%",
                            "Margin P2": f"{p['m_end']*100:.2f}%",
                            "Δ Total":   f"{p['pp_total']*100:+.2f}pp",
                            "1.Churned": f"{p['pp_B']*100:+.2f}pp",
                            "2.1 COGS":  f"{p['pp_cogs']*100:+.2f}pp",
                            "2.2 Price": f"{p['pp_price']*100:+.2f}pp",
                            "2.3 VolMix":f"{p['pp_volmix']*100:+.2f}pp",
                            "3.New SKU": f"{p['pp_G']*100:+.2f}pp",
                        })
                    df1 = pd.DataFrame(rows1)
                    st.dataframe(style_df(df1, ["Δ Total","1.Churned","2.1 COGS",
                                                "2.2 Price","2.3 VolMix","3.New SKU"]),
                                 hide_index=True, use_container_width=True)

                    # Tabel 1A — GP IDR
                    st.markdown("#### Tabel 1A — GP Bridge (IDR)")
                    rows2 = []
                    for bl in BLS + ["TOTAL"]:
                        p = pvm[bl]
                        delta = p['gp_end'] - p['gp_start']
                        rows2.append({
                            "BL": bl,
                            "GP P1": fmt_idr(p['gp_start']),
                            "GP P2": fmt_idr(p['gp_end']),
                            "Δ GP":  fmt_idr(delta),
                            "Δ GP%": f"{delta/p['gp_start']*100:+.1f}%" if p['gp_start']!=0 else "N/A",
                            "1.Churned": fmt_idr(-p.get('gp_dep',0)),
                            "2.1 COGS":  fmt_idr(p['cogs_rp']),
                            "2.2 Price": fmt_idr(p['price_rp']),
                            "2.3 VolMix":fmt_idr(p['volmix_rp']),
                            "3.New SKU": fmt_idr(p.get('gp_new',0)),
                        })
                    df2 = pd.DataFrame(rows2)
                    st.dataframe(style_df(df2, ["Δ GP","Δ GP%"]),
                                 hide_index=True, use_container_width=True)

                    # Tabel pp Bridge
                    st.markdown("#### Tabel pp Bridge Summary")
                    effects = [
                        ("Margin P1 (baseline)", "m_base", False),
                        ("1. Churned SKU",       "pp_B",   True),
                        ("2.1 COGS Effect",      "pp_cogs",True),
                        ("2.2 Price Effect",     "pp_price",True),
                        ("2.3 Vol-Mix Effect",   "pp_volmix",True),
                        ("3. New SKU",           "pp_G",   True),
                        ("Margin P2 (ending)",   "m_end",  False),
                    ]
                    rows3 = []
                    for label, key, is_delta in effects:
                        row = {"Effect": label}
                        for bl in BLS + ["TOTAL"]:
                            v = pvm[bl][key]
                            row[bl] = f"{v*100:.2f}%" if not is_delta else f"{v*100:+.2f}pp"
                        rows3.append(row)
                    df3 = pd.DataFrame(rows3)
                    st.dataframe(style_df(df3, BLS+["TOTAL"]),
                                 hide_index=True, use_container_width=True)

                except Exception:
                    st.error("❌ Error:")
                    st.code(traceback.format_exc(), language="python")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PI Analyzer
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈 PI Analyzer":
    st.markdown("""<div class="astro-header">
    <h1>📈 Price Index Decomposition</h1>
    <p>Shapley Value — Churned · Price Change · Comp Change · New SKU</p></div>""",
    unsafe_allow_html=True)

    st.markdown("""<div class="hint-box">
    <b>Kolom yang dibutuhkan:</b> <code>week_key</code>, <code>next_week</code>,
    <code>product_id</code>, <code>product_name</code>, <code>pricing_bl_25</code>,
    <code>price</code>, <code>next_price</code>, <code>cogs</code>, <code>next_cogs</code>,
    <code>comp_price</code>, <code>next_comp_price</code>, <code>pi</code>, <code>next_pi</code>
    </div>""", unsafe_allow_html=True)

    st.dataframe(pd.DataFrame({
        "week_key":       ["2026-04-07","2026-04-07","2026-04-07"],
        "next_week":      ["2026-04-14","2026-04-14","2026-04-14"],
        "product_id":     ["1001","1002","1003"],
        "pricing_bl_25":  ["Dry","Frozen","Fresh"],
        "price":          [3500,42000,8500],
        "next_price":     [3500,43000,8500],
        "comp_price":     [3400,41000,8200],
        "next_comp_price":[3300,41500,8800],
        "pi":             [102.94,102.44,103.66],
        "next_pi":        [106.06,103.61,96.59],
    }), hide_index=True, use_container_width=True)

    uploaded = st.file_uploader("Upload file CSV atau Excel (Q2 — PI Analyzer)",
                                 type=["csv","xlsx","xls"], key="pi_file")
    if uploaded:
        st.success(f"✅ {uploaded.name} ({uploaded.size/1024:.1f} KB)")
        if st.button("▶ Run PI Decomposition", key="run_pi"):
            with st.spinner("Memproses..."):
                try:
                    import pi_revised as _pi
                    file_bytes = uploaded.read()
                    excel_bytes, out_filename = _pi.run_pi(file_bytes, uploaded.name)

                    st.success("✅ Selesai!")
                    st.download_button("⬇️ Download Excel (PI Analyzer)", data=excel_bytes,
                        file_name=out_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="dl_pi")

                    st.markdown("---")
                    st.markdown("### 📊 Summary Preview — PI Bridge per BL")

                    buf2 = io.BytesIO(file_bytes)
                    ext  = uploaded.name.rsplit(".",1)[-1].lower()
                    df_raw = pd.read_csv(buf2) if ext=="csv" else pd.read_excel(buf2)
                    d = _pi.enrich(df_raw)
                    ov, sr, contribs = _pi.precompute(d)

                    segs = ["Dry","Fresh","Frozen"]
                    effects_pi = [
                        ("PI P1",                 "A",        False),
                        ("1. Churned SKU Effect", "eff_dep",  True),
                        ("2.1 Price Change",      "eff_price",True),
                        ("2.2 Comp Change",       "eff_comp", True),
                        ("2. Existing SKU (2.1+2.2)", None,  True),
                        ("3. New SKU Effect",     "eff_new",  True),
                        ("PI P2",                 "E",        False),
                    ]
                    rows_pi = []
                    for label, key, is_delta in effects_pi:
                        row = {"Effect": label}
                        for seg in segs + ["Overall"]:
                            src_ov = ov
                            src_sr = sr.get(seg, {})
                            src_ct = contribs.get(seg, {})
                            if key is None:
                                ep = src_ct.get("eff_price",0) if seg!="Overall" else ov.get("eff_price",0)
                                ec = src_ct.get("eff_comp",0)  if seg!="Overall" else ov.get("eff_comp",0)
                                v  = ep + ec
                            elif seg == "Overall":
                                v = src_ov.get(key, 0)
                            elif key in ("A","E","eff_dep","eff_price","eff_comp","eff_new"):
                                v = src_ct.get(key, src_sr.get(key, 0)) if key not in ("A","E") else src_sr.get(key, 0)
                            else:
                                v = src_sr.get(key, 0)
                            row[seg] = f"{v:.2f}" if not is_delta else f"{v:+.2f}pp"
                        rows_pi.append(row)

                    df_pi = pd.DataFrame(rows_pi)
                    delta_rows_mask = df_pi["Effect"].apply(
                        lambda x: any(k in x for k in ["Churned","Price","Comp","Existing","New"]))
                    st.dataframe(style_df(df_pi, segs+["Overall"]),
                                 hide_index=True, use_container_width=True)
                    st.caption("Hijau = berkontribusi positif pada PI · Merah = negatif")

                except Exception:
                    st.error("❌ Error:")
                    st.code(traceback.format_exc(), language="python")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Pricing Simulator
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🧮 Pricing Simulator":
    st.markdown("""<div class="astro-header">
    <h1>🧮 Pricing Simulator</h1>
    <p>Simulasi dampak skema harga baru terhadap Revenue, GP, dan Volume</p></div>""",
    unsafe_allow_html=True)

    # Format hints — always visible
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        st.markdown("""<div class="hint-box"><b>File 1 — Data Master (Q3):</b><br>
        <code>product_id</code>, <code>product_name</code>, <code>l1_category_name</code>,
        <code>pricing_bl_25</code>, <code>qty</code>, <code>selling_price</code>,
        <code>cost_price</code></div>""", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            "product_id":["1001","1002","1003"],
            "product_name":["Indomie Goreng","Ayam Fillet 500g","Tomat 500g"],
            "l1_category_name":["Mie Instan","Daging Beku","Sayuran"],
            "pricing_bl_25":["Dry","Frozen","Fresh"],
            "qty":[12500,3200,7800],
            "selling_price":[3500,42000,8500],
            "cost_price":[2800,35000,6200],
        }), hide_index=True, use_container_width=True)

    with col_h2:
        st.markdown("""<div class="hint-box"><b>File 2 — Skema Harga (buat manual):</b><br>
        <code>product_id</code>, <code>baseline</code>, <code>var_1</code>, <code>var_2</code>, …
        (kolom variant tidak terbatas)</div>""", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            "product_id":["1001","1002","1003"],
            "baseline":[3500,42000,8500],
            "var_1":[3300,40000,8000],
            "var_2":[3000,38000,7500],
        }), hide_index=True, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📁 File 1 — Data Master**")
        file1 = st.file_uploader("Upload Data Master", type=["csv","xlsx","xls"], key="sim_f1")
        if file1: st.success(f"✅ {file1.name}")
    with col2:
        st.markdown("**📁 File 2 — Skema Harga**")
        file2 = st.file_uploader("Upload Skema Harga", type=["csv","xlsx","xls"], key="sim_f2")
        if file2: st.success(f"✅ {file2.name}")

    if file1 and file2:
        if st.button("▶ Run Pricing Simulation", key="run_sim"):
            with st.spinner("Menjalankan simulasi..."):
                try:
                    import sim_final
                    f1b = file1.read(); f2b = file2.read()
                    excel_bytes, out_filename = sim_final.run_sim(f1b, file1.name, f2b, file2.name)

                    st.success("✅ Simulasi selesai!")
                    st.download_button("⬇️ Download Hasil Simulasi", data=excel_bytes,
                        file_name=out_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="dl_sim")

                    # ── Summary Impact Preview ────────────────────────────────
                    st.markdown("---")
                    st.markdown("### 📊 Summary Impact Preview")
                    try:
                        import openpyxl as _xl
                        wb_out = _xl.load_workbook(io.BytesIO(excel_bytes), data_only=True)
                        ws_sum = wb_out["Summary Impact"]

                        # Collect all rows as raw values
                        all_rows = list(ws_sum.values)

                        # Find the first row that has no empty cells (skip title/merged rows)
                        header_idx = None
                        for i, row in enumerate(all_rows):
                            non_empty = [c for c in row if c is not None and str(c).strip() != ""]
                            if len(non_empty) >= 3:
                                header_idx = i
                                break

                        if header_idx is not None:
                            raw_headers = list(all_rows[header_idx])
                            # Deduplicate headers
                            seen = {}
                            headers = []
                            for h in raw_headers:
                                h_str = str(h) if h is not None else ""
                                if h_str in seen:
                                    seen[h_str] += 1
                                    headers.append(f"{h_str}_{seen[h_str]}")
                                else:
                                    seen[h_str] = 0
                                    headers.append(h_str)

                            data_rows_sum = []
                            for row in all_rows[header_idx+1:]:
                                if any(c is not None and str(c).strip() != "" for c in row):
                                    data_rows_sum.append([
                                        str(c) if c is not None else "" for c in row
                                    ])

                            if data_rows_sum:
                                df_sum = pd.DataFrame(data_rows_sum, columns=headers)
                                # detect delta cols
                                delta_cols = [c for c in df_sum.columns
                                              if any(x in str(c) for x in ["Δ","delta","Delta","%","diff"])]
                                st.dataframe(
                                    style_df(df_sum, delta_cols) if delta_cols else df_sum,
                                    hide_index=True, use_container_width=True
                                )
                            else:
                                st.info("Summary Impact kosong.")
                        else:
                            st.warning("Tidak bisa membaca sheet Summary Impact.")
                    except Exception as e_sum:
                        st.warning(f"Preview Summary Impact gagal: {e_sum}")

                except Exception:
                    st.error("❌ Error:")
                    st.code(traceback.format_exc(), language="python")
    elif file1 or file2:
        st.warning("⚠️ Upload kedua file untuk menjalankan simulasi.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — Query Reference
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗄️ Query Reference":
    st.markdown("""<div class="astro-header">
    <h1>🗄️ Query Reference</h1>
    <p>Template BigQuery SQL — pilih DOW & minggu, query otomatis ter-update</p></div>""",
    unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Q1 — GP Bridge","Q2 — PI Analyzer","Q3 — Pricing Simulator"])

    def dow_week_picker(prefix):
        """DOW picker + 2 date pickers that only allow the chosen DOW"""
        dow_choice = st.selectbox(
            "Pilih Day of Week (start periode)",
            DAYS, index=0, key=f"{prefix}_dow"
        )
        dow_int = DOW_MAP[dow_choice]
        allowed = find_allowed_dates(dow_int, months_back=12)

        st.markdown(f"ℹ️ Kalender hanya menampilkan hari **{dow_choice}** — pilih 2 tanggal untuk dibandingkan.")
        col1, col2 = st.columns(2)

        # default: last two occurrences of the chosen DOW
        defaults = [d for d in allowed if d <= datetime.date.today()]
        def_w2 = defaults[-1] if len(defaults) >= 1 else allowed[0]
        def_w1 = defaults[-2] if len(defaults) >= 2 else allowed[0]

        with col1:
            w1 = st.selectbox(
                f"Week 1 — {dow_choice}",
                options=allowed,
                index=allowed.index(def_w1) if def_w1 in allowed else 0,
                format_func=lambda d: d.strftime("%d %b %Y"),
                key=f"{prefix}_w1"
            )
        with col2:
            w2 = st.selectbox(
                f"Week 2 — {dow_choice}",
                options=allowed,
                index=allowed.index(def_w2) if def_w2 in allowed else min(1, len(allowed)-1),
                format_func=lambda d: d.strftime("%d %b %Y"),
                key=f"{prefix}_w2"
            )

        w1_start = w1
        w1_end   = w1 + datetime.timedelta(days=6)
        w2_start = w2
        w2_end   = w2 + datetime.timedelta(days=6)

        st.markdown(
            f"**Week 1:** {w1_start.strftime('%d %b %Y')} → {w1_end.strftime('%d %b %Y')} &nbsp;|&nbsp; "
            f"**Week 2:** {w2_start.strftime('%d %b %Y')} → {w2_end.strftime('%d %b %Y')}"
        )
        return w1_start, w1_end, w2_start, w2_end

    with tab1:
        w1s, w1e, w2s, w2e = dow_week_picker("q1")
        q1 = f"""-- Q1: GP Bridge
-- Week 1: {w1s} → {w1e}  |  Week 2: {w2s} → {w2e}
SELECT
    '{w1s}' AS week_key,
    '{w2s}' AS next_week,
    p.product_id,
    p.product_name,
    p.pricing_bl_25,
    SUM(IF(DATE(o.created_at) BETWEEN '{w1s}' AND '{w1e}', o.qty, 0))              AS qty,
    SUM(IF(DATE(o.created_at) BETWEEN '{w2s}' AND '{w2e}', o.qty, 0))              AS qty1,
    AVG(IF(DATE(o.created_at) BETWEEN '{w1s}' AND '{w1e}', o.selling_price, NULL)) AS selling_price,
    AVG(IF(DATE(o.created_at) BETWEEN '{w2s}' AND '{w2e}', o.selling_price, NULL)) AS selling_price1,
    AVG(IF(DATE(o.created_at) BETWEEN '{w1s}' AND '{w1e}', o.cost_price, NULL))    AS cost_price,
    AVG(IF(DATE(o.created_at) BETWEEN '{w2s}' AND '{w2e}', o.cost_price, NULL))    AS cost_price1,
    AVG(IF(DATE(c.date) BETWEEN '{w1s}' AND '{w1e}', c.comp_price, NULL))          AS comp_price,
    AVG(IF(DATE(c.date) BETWEEN '{w2s}' AND '{w2e}', c.comp_price, NULL))          AS comp_price1,
    AVG(IF(DATE(c.date) BETWEEN '{w1s}' AND '{w1e}', c.pi, NULL))                  AS pi,
    AVG(IF(DATE(c.date) BETWEEN '{w2s}' AND '{w2e}', c.pi, NULL))                  AS pi1
FROM `astro-data-prd.astro_datamart.dim_products`        p
LEFT JOIN `astro-data-prd.astro_datamart.fct_orders`     o USING (product_id)
LEFT JOIN `astro-data-prd.astro_datamart.fct_comp_price` c USING (product_id)
WHERE p.pricing_bl_25 IN ('Dry','Fresh','Frozen','PL')
GROUP BY 1,2,3,4,5
ORDER BY p.pricing_bl_25, p.product_name"""
        st.code(q1, language="sql")

    with tab2:
        w1s, w1e, w2s, w2e = dow_week_picker("q2")
        q2 = f"""-- Q2: PI Analyzer
-- Week 1: {w1s} → {w1e}  |  Week 2: {w2s} → {w2e}
SELECT
    '{w1s}' AS week_key,
    '{w2s}' AS next_week,
    p.product_id,
    p.product_name,
    p.pricing_bl_25,
    AVG(IF(DATE(o.created_at) BETWEEN '{w1s}' AND '{w1e}', o.selling_price, NULL)) AS price,
    AVG(IF(DATE(o.created_at) BETWEEN '{w2s}' AND '{w2e}', o.selling_price, NULL)) AS next_price,
    AVG(IF(DATE(o.created_at) BETWEEN '{w1s}' AND '{w1e}', o.cost_price, NULL))    AS cogs,
    AVG(IF(DATE(o.created_at) BETWEEN '{w2s}' AND '{w2e}', o.cost_price, NULL))    AS next_cogs,
    AVG(IF(DATE(c.date) BETWEEN '{w1s}' AND '{w1e}', c.comp_price, NULL))          AS comp_price,
    AVG(IF(DATE(c.date) BETWEEN '{w2s}' AND '{w2e}', c.comp_price, NULL))          AS next_comp_price,
    AVG(IF(DATE(c.date) BETWEEN '{w1s}' AND '{w1e}', c.pi, NULL))                  AS pi,
    AVG(IF(DATE(c.date) BETWEEN '{w2s}' AND '{w2e}', c.pi, NULL))                  AS next_pi
FROM `astro-data-prd.astro_datamart.dim_products`        p
LEFT JOIN `astro-data-prd.astro_datamart.fct_orders`     o USING (product_id)
LEFT JOIN `astro-data-prd.astro_datamart.fct_comp_price` c USING (product_id)
WHERE p.pricing_bl_25 IN ('Dry','Fresh','Frozen','PL')
GROUP BY 1,2,3,4,5
ORDER BY p.pricing_bl_25, p.product_name"""
        st.code(q2, language="sql")

    with tab3:
        st.markdown("""<div class="hint-box">Parameter: rentang tanggal bebas (tidak harus weekly)</div>""",
                    unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        ds = c1.date_input("Start Date", key="q3_ds",
                           value=datetime.date.today() - datetime.timedelta(days=30))
        de = c2.date_input("End Date",   key="q3_de", value=datetime.date.today())
        q3 = f"""-- Q3: Pricing Simulator
-- Periode: {ds} → {de}
SELECT
    p.product_id,
    p.product_name,
    p.l1_category_name,
    p.pricing_bl_25,
    SUM(o.qty)           AS qty,
    AVG(o.selling_price) AS selling_price,
    AVG(o.cost_price)    AS cost_price
FROM `astro-data-prd.astro_datamart.dim_products`    p
LEFT JOIN `astro-data-prd.astro_datamart.fct_orders` o USING (product_id)
WHERE p.pricing_bl_25 IN ('Dry','Fresh','Frozen','PL')
  AND DATE(o.created_at) BETWEEN '{ds}' AND '{de}'
GROUP BY 1,2,3,4
ORDER BY p.pricing_bl_25, p.product_name"""
        st.code(q3, language="sql")

    st.info("💡 Query di atas adalah template — sesuaikan nama kolom/tabel dengan schema BigQuery Astro yang sebenarnya.", icon="💡")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="text-align:center;color:#8fa5cc;font-size:0.78rem;margin-top:40px;'
    'padding-top:14px;border-top:1px solid #e0e9ff;">'
    '🚀 Astro Pricing Tools · Pricing Strategy Team</div>',
    unsafe_allow_html=True
)
