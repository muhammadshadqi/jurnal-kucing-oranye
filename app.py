import streamlit as st
import io, traceback
import pandas as pd
import numpy as np

LOGO_B64 = "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"

st.set_page_config(page_title="Astro Pricing Tools", page_icon="🚀", layout="wide",
                   initial_sidebar_state="expanded")

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
</style>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:14px 0 6px;">
        <img src="data:image/png;base64,{LOGO_B64}" style="width:64px;height:64px;border-radius:12px;margin-bottom:6px;"/>
        <div style="font-family:'Nunito',sans-serif;font-size:1.1rem;font-weight:800;color:white;letter-spacing:-0.3px;">Pricing Tools</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Nav", ["📊 GP Bridge","📈 PI Analyzer","🧮 Pricing Simulator","🗄️ Query Reference"],
                    label_visibility="collapsed")
    st.markdown("---")
    st.markdown('<div style="font-size:0.75rem;color:rgba(255,255,255,0.6);line-height:1.7;">Output: Excel (.xlsx)<br>Input: CSV atau Excel<br>Engine: Python + openpyxl</div>', unsafe_allow_html=True)

# ── Helper ───────────────────────────────────────────────────────────────────
def color_delta(val):
    if pd.isna(val): return ""
    try:
        v = float(str(val).replace("%","").replace(",",""))
        return "color: #1A7A4A; font-weight:600" if v > 0 else ("color: #C0392B; font-weight:600" if v < 0 else "")
    except: return ""

def style_delta_df(df, cols):
    return df.style.applymap(color_delta, subset=cols)

def fmt_idr(v):
    try: return f"Rp {float(v):,.0f}"
    except: return v

def fmt_pct(v):
    try: return f"{float(v)*100:+.1f}%"
    except: return v

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — GP Bridge
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 GP Bridge":
    st.markdown("""<div class="astro-header"><h1>📊 GP Bridge & PVM Decomposition</h1>
    <p>Price · Volume · Mix · COGS · New & Churned SKU Effect</p></div>""", unsafe_allow_html=True)

    with st.expander("📋 Format kolom yang dibutuhkan", expanded=False):
        st.markdown("**Wajib:** `week_key`, `next_week`, `product_id`, `product_name`, `pricing_bl_25`, `qty`, `qty1`, `selling_price`, `selling_price1`, `cost_price`, `cost_price1`")
        st.markdown("**Opsional:** `comp_price`, `comp_price1`, `pi`, `pi1`, `avg_stock`, `avg_stock1`, `pareto_classification`")
        st.markdown("**Contoh 3 baris data:**")
        st.dataframe(pd.DataFrame({
            "week_key":["20250101","20250101","20250101"],
            "next_week":["20250108","20250108","20250108"],
            "product_id":["SKU001","SKU002","SKU003"],
            "product_name":["Indomie Goreng","Aqua 600ml","Minyakita 1L"],
            "pricing_bl_25":["Dry","Dry","Dry"],
            "qty":[1200,800,500], "qty1":[1350,750,520],
            "selling_price":[3500,2800,15000], "selling_price1":[3500,2800,15500],
            "cost_price":[2800,2100,13000], "cost_price1":[2850,2100,13200],
        }), hide_index=True, use_container_width=True)

    uploaded = st.file_uploader("Upload file CSV atau Excel (Q1 — GP Bridge)", type=["csv","xlsx","xls"], key="pvm_file")

    if uploaded:
        st.success(f"✅ {uploaded.name} ({uploaded.size/1024:.1f} KB)")

        if st.button("▶ Run GP Bridge Analysis", key="run_pvm"):
            with st.spinner("Memproses..."):
                try:
                    import pvm_revised
                    file_bytes = uploaded.read()
                    excel_bytes, out_filename = pvm_revised.run_pvm(file_bytes, uploaded.name)

                    st.success("✅ Selesai!")
                    st.download_button("⬇️ Download Excel (GP Bridge)", data=excel_bytes,
                                       file_name=out_filename,
                                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                       key="dl_pvm")

                    # ── Summary Tables ──────────────────────────────────────
                    st.markdown("---")
                    st.markdown("### 📊 Summary Preview")

                    # Re-run compute for summary
                    import importlib, sys
                    buf2 = io.BytesIO(file_bytes)
                    ext = uploaded.name.rsplit(".",1)[-1].lower()
                    df_raw = pd.read_csv(buf2) if ext=="csv" else pd.read_excel(buf2)

                    import pvm_revised as _pvm
                    df_raw = _pvm.ensure_cols(df_raw)
                    p1c, p2c = _pvm.detect_period(df_raw)
                    if p1c is None: p1c, p2c = "week_key","next_key"
                    df_e = _pvm.enrich(df_raw, p1c, p2c)
                    pvm = _pvm.compute_pvm(df_e)

                    BLS = ["Dry","Fresh","Frozen","PL"]

                    # Tabel 1 — Margin Bridge per BL
                    st.markdown("#### Tabel 1 — Margin Bridge per BL (pp & IDR)")
                    rows_t1 = []
                    for bl in BLS + ["TOTAL"]:
                        p = pvm[bl]
                        rows_t1.append({
                            "BL": bl,
                            "Margin P1 (%)": f"{p['m_base']*100:.2f}%",
                            "Margin P2 (%)": f"{p['m_end']*100:.2f}%",
                            "Δ Total (pp)": f"{p['pp_total']*100:+.2f}pp",
                            "1. Churned SKU (pp)": f"{p['pp_B']*100:+.2f}pp",
                            "2.1 COGS Effect (pp)": f"{p['pp_cogs']*100:+.2f}pp",
                            "2.2 Price Effect (pp)": f"{p['pp_price']*100:+.2f}pp",
                            "2.3 Vol-Mix Effect (pp)": f"{p['pp_volmix']*100:+.2f}pp",
                            "3. New SKU (pp)": f"{p['pp_G']*100:+.2f}pp",
                        })
                    df_t1 = pd.DataFrame(rows_t1)
                    delta_cols_t1 = ["Δ Total (pp)","1. Churned SKU (pp)","2.1 COGS Effect (pp)",
                                     "2.2 Price Effect (pp)","2.3 Vol-Mix Effect (pp)","3. New SKU (pp)"]
                    st.dataframe(style_delta_df(df_t1, delta_cols_t1), hide_index=True, use_container_width=True)

                    # Tabel 1A — GP Bridge IDR
                    st.markdown("#### Tabel 1A — GP Bridge (IDR)")
                    rows_t1a = []
                    for bl in BLS + ["TOTAL"]:
                        p = pvm[bl]
                        rows_t1a.append({
                            "BL": bl,
                            "GP P1": fmt_idr(p['gp_start']),
                            "GP P2": fmt_idr(p['gp_end']),
                            "Δ GP": fmt_idr(p['gp_end']-p['gp_start']),
                            "Δ GP (%)": f"{(p['gp_end']-p['gp_start'])/p['gp_start']*100:+.1f}%" if p['gp_start']!=0 else "N/A",
                            "1. Churned (IDR)": fmt_idr(p['gp_dep'] * -1 if 'gp_dep' in p else 0),
                            "2.1 COGS (IDR)": fmt_idr(p['cogs_rp']),
                            "2.2 Price (IDR)": fmt_idr(p['price_rp']),
                            "2.3 Vol-Mix (IDR)": fmt_idr(p['volmix_rp']),
                            "3. New SKU (IDR)": fmt_idr(p.get('gp_new',0)),
                        })
                    df_t1a = pd.DataFrame(rows_t1a)
                    st.dataframe(style_delta_df(df_t1a, ["Δ GP","Δ GP (%)"]), hide_index=True, use_container_width=True)

                    # Tabel pp Bridge summary
                    st.markdown("#### Tabel pp Bridge Summary")
                    rows_pp = []
                    effects = [
                        ("Margin P1 (baseline)", "m_base"),
                        ("1. Churned SKU Effect", "pp_B"),
                        ("2.1 COGS Effect", "pp_cogs"),
                        ("2.2 Price Effect", "pp_price"),
                        ("2.3 Vol-Mix Effect", "pp_volmix"),
                        ("3. New SKU Effect", "pp_G"),
                        ("Margin P2 (ending)", "m_end"),
                    ]
                    for label, key in effects:
                        row = {"Effect": label}
                        for bl in BLS + ["TOTAL"]:
                            v = pvm[bl][key]
                            row[bl] = f"{v*100:.2f}%" if key in ("m_base","m_end") else f"{v*100:+.2f}pp"
                        rows_pp.append(row)
                    df_pp = pd.DataFrame(rows_pp)
                    delta_cols_pp = [bl for bl in BLS+["TOTAL"]]
                    st.dataframe(df_pp.style.applymap(color_delta, subset=delta_cols_pp),
                                 hide_index=True, use_container_width=True)

                except Exception:
                    st.error("❌ Error:")
                    st.code(traceback.format_exc(), language="python")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PI Analyzer
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈 PI Analyzer":
    st.markdown("""<div class="astro-header"><h1>📈 Price Index Decomposition</h1>
    <p>Shapley Value decomposition — Churned · Price Change · Comp Change · New SKU</p></div>""", unsafe_allow_html=True)

    with st.expander("📋 Format kolom yang dibutuhkan", expanded=False):
        st.markdown("**Kolom:** `week_key`, `next_week`, `product_id`, `product_name`, `pricing_bl_25`, `price`, `next_price`, `cogs`, `next_cogs`, `comp_price`, `next_comp_price`, `pi`, `next_pi`")
        st.markdown("**Contoh 3 baris data:**")
        st.dataframe(pd.DataFrame({
            "week_key":["20250101","20250101","20250101"],
            "next_week":["20250108","20250108","20250108"],
            "product_id":["SKU001","SKU002","SKU003"],
            "product_name":["Indomie Goreng","Aqua 600ml","Minyakita 1L"],
            "pricing_bl_25":["Dry","Dry","Fresh"],
            "price":[3500,2800,15000],"next_price":[3500,2800,15500],
            "cogs":[2800,2100,13000],"next_cogs":[2850,2100,13200],
            "comp_price":[3400,2750,14800],"next_comp_price":[3400,2900,15000],
            "pi":[102.9,101.8,101.4],"next_pi":[102.9,96.6,103.3],
        }), hide_index=True, use_container_width=True)

    uploaded = st.file_uploader("Upload file CSV atau Excel (Q2 — PI Analyzer)", type=["csv","xlsx","xls"], key="pi_file")

    if uploaded:
        st.success(f"✅ {uploaded.name} ({uploaded.size/1024:.1f} KB)")

        if st.button("▶ Run PI Decomposition", key="run_pi"):
            with st.spinner("Memproses..."):
                try:
                    import pi_revised
                    file_bytes = uploaded.read()
                    excel_bytes, out_filename = pi_revised.run_pi(file_bytes, uploaded.name)

                    st.success("✅ Selesai!")
                    st.download_button("⬇️ Download Excel (PI Analyzer)", data=excel_bytes,
                                       file_name=out_filename,
                                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                       key="dl_pi")

                    # ── Summary Table ────────────────────────────────────────
                    st.markdown("---")
                    st.markdown("### 📊 Summary Preview — PI Bridge per BL")

                    buf2 = io.BytesIO(file_bytes)
                    ext = uploaded.name.rsplit(".",1)[-1].lower()
                    df_raw = pd.read_csv(buf2) if ext=="csv" else pd.read_excel(buf2)

                    import pi_revised as _pi
                    d = _pi.enrich(df_raw)
                    ov, sr, contribs = _pi.precompute(d)

                    segs = ["Dry","Fresh","Frozen"]
                    rows_pi = []
                    effects_pi = [
                        ("PI P1 (A)", "A"),
                        ("1. Churned SKU Effect", "eff_dep"),
                        ("2. Existing SKU Effect", None),
                        ("  2.1 Price Change Effect", "eff_price"),
                        ("  2.2 Comp Change Effect", "eff_comp"),
                        ("3. New SKU Effect", "eff_new"),
                        ("PI P2 (E)", "E"),
                    ]
                    for label, key in effects_pi:
                        row = {"Effect": label}
                        for seg in segs + ["Overall"]:
                            src = ov if seg == "Overall" else (contribs[seg] if key in ("eff_dep","eff_price","eff_comp","eff_new") else sr[seg])
                            if key is None:
                                v = (sr[seg]["eff_price"] + sr[seg]["eff_comp"]) if seg != "Overall" else (ov["eff_price"]+ov["eff_comp"])
                                row[seg] = f"{v:+.2f}pp"
                            elif key in ("A","E"):
                                row[seg] = f"{src[key]:.2f}"
                            else:
                                row[seg] = f"{src[key]:+.2f}pp"
                        rows_pi.append(row)

                    df_pi_sum = pd.DataFrame(rows_pi)
                    delta_cols_pi = segs + ["Overall"]
                    st.dataframe(df_pi_sum.style.applymap(color_delta, subset=delta_cols_pi),
                                 hide_index=True, use_container_width=True)

                    st.caption("Warna hijau = positif (PI naik/berkontribusi positif) · Merah = negatif")

                except Exception:
                    st.error("❌ Error:")
                    st.code(traceback.format_exc(), language="python")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Pricing Simulator
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🧮 Pricing Simulator":
    st.markdown("""<div class="astro-header"><h1>🧮 Pricing Simulator</h1>
    <p>Simulasi dampak skema harga baru terhadap Revenue, GP, dan Volume</p></div>""", unsafe_allow_html=True)

    with st.expander("📋 Format kedua file", expanded=False):
        st.markdown("**File 1 — Data Master (dari Q3):** `product_id`, `product_name`, `l1_category_name`, `pricing_bl_25`, `qty`, `selling_price`, `cost_price`")
        st.markdown("**File 2 — Skema Harga (buat manual):** `product_id`, `baseline`, `var_1`, `var_2`, ...")
        col1e, col2e = st.columns(2)
        with col1e:
            st.markdown("Contoh File 1:")
            st.dataframe(pd.DataFrame({
                "product_id":["SKU001","SKU002"],"product_name":["Indomie Goreng","Aqua 600ml"],
                "l1_category_name":["Noodles","Beverages"],"pricing_bl_25":["Dry","Dry"],
                "qty":[1200,800],"selling_price":[3500,2800],"cost_price":[2800,2100]
            }), hide_index=True, use_container_width=True)
        with col2e:
            st.markdown("Contoh File 2:")
            st.dataframe(pd.DataFrame({
                "product_id":["SKU001","SKU002"],
                "baseline":[3500,2800],"var_1":[3300,2600],"var_2":[3200,2500]
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

                    # ── Summary Impact Preview ───────────────────────────────
                    st.markdown("---")
                    st.markdown("### 📊 Summary Impact Preview")

                    wb_out = __import__("openpyxl").load_workbook(io.BytesIO(excel_bytes), data_only=True)
                    ws_sum = wb_out["Summary Impact"]
                    rows_sum = list(ws_sum.values)
                    if rows_sum:
                        headers = [str(h) if h is not None else "" for h in rows_sum[0]]
                        data_sum = [[str(c) if c is not None else "" for c in row] for row in rows_sum[1:]]
                        df_sum = pd.DataFrame(data_sum, columns=headers)

                        # Auto-detect numeric delta columns for coloring
                        delta_candidates = [c for c in df_sum.columns if any(x in c.lower() for x in ["delta","diff","Δ","change","%"])]
                        st.dataframe(style_delta_df(df_sum, delta_candidates) if delta_candidates else df_sum,
                                     hide_index=True, use_container_width=True)

                except Exception:
                    st.error("❌ Error:")
                    st.code(traceback.format_exc(), language="python")
    elif file1 or file2:
        st.warning("⚠️ Upload kedua file untuk menjalankan simulasi.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — Query Reference
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗄️ Query Reference":
    st.markdown("""<div class="astro-header"><h1>🗄️ Query Reference</h1>
    <p>Template BigQuery SQL — copy, isi tanggal, run di BigQuery</p></div>""", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Q1 — GP Bridge","Q2 — PI Analyzer","Q3 — Pricing Simulator"])

    with tab1:
        st.markdown("**Parameter:** 2 minggu yang dibandingkan. `end_date = start_date + 6 hari`")
        c1, c2, c3, c4 = st.columns(4)
        d1s = c1.date_input("Week 1 Start", key="q1_d1s")
        d1e = c2.date_input("Week 1 End", key="q1_d1e")
        d2s = c3.date_input("Week 2 Start", key="q1_d2s")
        d2e = c4.date_input("Week 2 End", key="q1_d2e")
        q1 = f"""-- Q1: GP Bridge
SELECT
    '{d1s}' AS week_key, '{d2s}' AS next_week,
    p.product_id, p.product_name, p.pricing_bl_25,
    SUM(IF(DATE(o.created_at) BETWEEN '{d1s}' AND '{d1e}', o.qty, 0))             AS qty,
    SUM(IF(DATE(o.created_at) BETWEEN '{d2s}' AND '{d2e}', o.qty, 0))             AS qty1,
    AVG(IF(DATE(o.created_at) BETWEEN '{d1s}' AND '{d1e}', o.selling_price, NULL)) AS selling_price,
    AVG(IF(DATE(o.created_at) BETWEEN '{d2s}' AND '{d2e}', o.selling_price, NULL)) AS selling_price1,
    AVG(IF(DATE(o.created_at) BETWEEN '{d1s}' AND '{d1e}', o.cost_price, NULL))    AS cost_price,
    AVG(IF(DATE(o.created_at) BETWEEN '{d2s}' AND '{d2e}', o.cost_price, NULL))    AS cost_price1,
    AVG(IF(DATE(c.date) BETWEEN '{d1s}' AND '{d1e}', c.comp_price, NULL))          AS comp_price,
    AVG(IF(DATE(c.date) BETWEEN '{d2s}' AND '{d2e}', c.comp_price, NULL))          AS comp_price1,
    AVG(IF(DATE(c.date) BETWEEN '{d1s}' AND '{d1e}', c.pi, NULL))                  AS pi,
    AVG(IF(DATE(c.date) BETWEEN '{d2s}' AND '{d2e}', c.pi, NULL))                  AS pi1
FROM `astro-data-prd.astro_datamart.dim_products`        p
LEFT JOIN `astro-data-prd.astro_datamart.fct_orders`     o USING (product_id)
LEFT JOIN `astro-data-prd.astro_datamart.fct_comp_price` c USING (product_id)
WHERE p.pricing_bl_25 IN ('Dry','Fresh','Frozen','PL')
GROUP BY 1,2,3,4,5
ORDER BY p.pricing_bl_25, p.product_name"""
        st.code(q1, language="sql")

    with tab2:
        st.markdown("**Parameter:** Sama dengan Q1")
        c1, c2, c3, c4 = st.columns(4)
        d1s = c1.date_input("Week 1 Start", key="q2_d1s")
        d1e = c2.date_input("Week 1 End", key="q2_d1e")
        d2s = c3.date_input("Week 2 Start", key="q2_d2s")
        d2e = c4.date_input("Week 2 End", key="q2_d2e")
        q2 = f"""-- Q2: PI Analyzer
SELECT
    '{d1s}' AS week_key, '{d2s}' AS next_week,
    p.product_id, p.product_name, p.pricing_bl_25,
    AVG(IF(DATE(o.created_at) BETWEEN '{d1s}' AND '{d1e}', o.selling_price, NULL)) AS price,
    AVG(IF(DATE(o.created_at) BETWEEN '{d2s}' AND '{d2e}', o.selling_price, NULL)) AS next_price,
    AVG(IF(DATE(o.created_at) BETWEEN '{d1s}' AND '{d1e}', o.cost_price, NULL))    AS cogs,
    AVG(IF(DATE(o.created_at) BETWEEN '{d2s}' AND '{d2e}', o.cost_price, NULL))    AS next_cogs,
    AVG(IF(DATE(c.date) BETWEEN '{d1s}' AND '{d1e}', c.comp_price, NULL))          AS comp_price,
    AVG(IF(DATE(c.date) BETWEEN '{d2s}' AND '{d2e}', c.comp_price, NULL))          AS next_comp_price,
    AVG(IF(DATE(c.date) BETWEEN '{d1s}' AND '{d1e}', c.pi, NULL))                  AS pi,
    AVG(IF(DATE(c.date) BETWEEN '{d2s}' AND '{d2e}', c.pi, NULL))                  AS next_pi
FROM `astro-data-prd.astro_datamart.dim_products`        p
LEFT JOIN `astro-data-prd.astro_datamart.fct_orders`     o USING (product_id)
LEFT JOIN `astro-data-prd.astro_datamart.fct_comp_price` c USING (product_id)
WHERE p.pricing_bl_25 IN ('Dry','Fresh','Frozen','PL')
GROUP BY 1,2,3,4,5
ORDER BY p.pricing_bl_25, p.product_name"""
        st.code(q2, language="sql")

    with tab3:
        st.markdown("**Parameter:** Rentang tanggal bebas (tidak harus weekly)")
        c1, c2 = st.columns(2)
        ds = c1.date_input("Start Date", key="q3_ds")
        de = c2.date_input("End Date", key="q3_de")
        q3 = f"""-- Q3: Pricing Simulator
SELECT
    p.product_id, p.product_name,
    p.l1_category_name, p.pricing_bl_25,
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
st.markdown('<div style="text-align:center;color:#8fa5cc;font-size:0.78rem;margin-top:40px;padding-top:14px;border-top:1px solid #e0e9ff;">🚀 Astro Pricing Tools · Pricing Strategy Team</div>', unsafe_allow_html=True)
