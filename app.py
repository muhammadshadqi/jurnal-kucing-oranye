import streamlit as st
import io
import traceback

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="Astro Pricing Tools",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS — Astro brand ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;600;700;800&family=Nunito:wght@600;700;800&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Nunito Sans', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #003DA6 0%, #0055CC 60%, #0083FF 100%);
}
[data-testid="stSidebar"] * {
    color: white !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-weight: 600;
    font-size: 0.95rem;
    padding: 6px 0;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.25) !important;
}

/* Main header */
.astro-header {
    background: linear-gradient(135deg, #003DA6 0%, #0083FF 100%);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 20px;
}
.astro-header h1 {
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 2rem;
    color: white;
    margin: 0;
    line-height: 1.2;
}
.astro-header p {
    color: rgba(255,255,255,0.82);
    margin: 6px 0 0 0;
    font-size: 0.95rem;
}

/* Section card */
.section-card {
    background: #f8faff;
    border: 1.5px solid #dce8ff;
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 20px;
}
.section-card h3 {
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    color: #003DA6;
    margin-top: 0;
}

/* Upload area */
[data-testid="stFileUploader"] {
    background: #f0f6ff;
    border: 2px dashed #0083FF;
    border-radius: 10px;
    padding: 8px;
}

/* Primary button */
.stButton > button {
    background: linear-gradient(135deg, #0083FF, #003DA6);
    color: white !important;
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    border: none;
    border-radius: 10px;
    padding: 12px 32px;
    width: 100%;
    transition: opacity 0.2s, transform 0.1s;
}
.stButton > button:hover {
    opacity: 0.88;
    transform: translateY(-1px);
}

/* Download button */
[data-testid="stDownloadButton"] button {
    background: #00a651 !important;
    color: white !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    width: 100%;
    font-size: 1rem !important;
    padding: 12px 32px !important;
}

/* Info / success / error banners */
.stAlert {
    border-radius: 10px !important;
}

/* Code block */
.stCodeBlock {
    border-radius: 10px;
}

/* Query tabs */
.stTabs [data-baseweb="tab"] {
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    color: #003DA6;
}
.stTabs [aria-selected="true"] {
    color: #0083FF !important;
    border-bottom-color: #0083FF !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #8fa5cc;
    font-size: 0.8rem;
    margin-top: 48px;
    padding-top: 16px;
    border-top: 1px solid #e0e9ff;
}
</style>
""", unsafe_allow_html=True)


# ── Sidebar navigation ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 16px 0 8px 0;">
        <div style="font-family:'Nunito',sans-serif; font-size:1.6rem; font-weight:800; color:white; letter-spacing:-0.5px;">
            🚀 Astro
        </div>
        <div style="font-size:0.8rem; color:rgba(255,255,255,0.7); margin-top:2px;">Pricing Tools</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio(
        "Navigation",
        options=["📊 GP Bridge", "📈 PI Analyzer", "🧮 Pricing Simulator", "🗄️ Query Reference"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.78rem; color:rgba(255,255,255,0.6); line-height:1.6;">
        <b>Output:</b> Excel (.xlsx)<br>
        <b>Input:</b> CSV atau Excel<br>
        <b>Engine:</b> Python + openpyxl
    </div>
    """, unsafe_allow_html=True)


# ── Helper: safe import ──────────────────────────────────────────────────────
def _import_module(module_name):
    """Try to import a module; return (module, error_string)."""
    try:
        import importlib
        mod = importlib.import_module(module_name)
        return mod, None
    except Exception as e:
        return None, str(e)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — GP Bridge / PVM Decomposition
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 GP Bridge":
    st.markdown("""
    <div class="astro-header">
        <div>
            <h1>📊 GP Bridge & PVM Decomposition</h1>
            <p>Dekomposisi Gross Profit — Price, Volume, Mix, COGS, New & Churned SKU Effect</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📁 Upload Data")
    st.info("Upload **1 file** CSV atau Excel hasil query BigQuery (Q1 — GP Bridge).", icon="ℹ️")

    col_req, col_opt = st.columns(2)
    with col_req:
        st.markdown("**Kolom wajib:**")
        st.markdown("""
        `week_key`, `next_week`, `product_id`, `product_name`, `pricing_bl_25`,
        `qty`, `qty1`, `selling_price`, `selling_price1`, `cost_price`, `cost_price1`
        """)
    with col_opt:
        st.markdown("**Kolom opsional:**")
        st.markdown("""
        `comp_price`, `comp_price1`, `pi`, `pi1`,
        `avg_stock`, `avg_stock1`, `pareto_classification`
        """)

    uploaded = st.file_uploader(
        "Drop file di sini atau klik Browse",
        type=["csv", "xlsx", "xls"],
        key="pvm_file",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded:
        st.success(f"✅ File diterima: **{uploaded.name}** ({uploaded.size / 1024:.1f} KB)", icon="✅")

        if st.button("▶ Run GP Bridge Analysis", key="run_pvm"):
            with st.spinner("Memproses data dan generate Excel…"):
                try:
                    pvm_mod, err = _import_module("pvm_revised")
                    if err:
                        st.error(f"❌ Gagal import `pvm_revised.py`: {err}")
                    else:
                        file_bytes = uploaded.read()
                        excel_bytes, out_filename = pvm_mod.run_pvm(file_bytes, uploaded.name)
                        st.balloons()
                        st.success("✅ Analisis selesai! Klik tombol di bawah untuk download.", icon="🎉")
                        st.download_button(
                            label="⬇️ Download Hasil Excel (GP Bridge)",
                            data=excel_bytes,
                            file_name=out_filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key="dl_pvm",
                        )
                        with st.expander("📋 Sheet yang di-generate (12 sheets)"):
                            sheets = [
                                "0. Formula Reference", "1. Raw Data", "Executive Overview",
                                "1b. Aggregates", "2. Margin Bridge", "2b. Margin Bridge (±)",
                                "3. GV Tier", "4. L1 Category", "5. New & Dep",
                                "6. COGS vs Comp", "6b. SKU Bermasalah", "7. SKU Watch List",
                            ]
                            for s in sheets:
                                st.markdown(f"- {s}")
                except Exception:
                    st.error("❌ Terjadi error saat proses. Lihat detail di bawah.")
                    st.code(traceback.format_exc(), language="python")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PI Analyzer
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈 PI Analyzer":
    st.markdown("""
    <div class="astro-header">
        <div>
            <h1>📈 Price Index Decomposition</h1>
            <p>Analisis perubahan Pricing Index vs kompetitor — Shapley Value decomposition</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📁 Upload Data")
    st.info("Upload **1 file** CSV atau Excel hasil query BigQuery (Q2 — PI Analyzer).", icon="ℹ️")

    st.markdown("**Kolom yang dibutuhkan:**")
    st.markdown("""
    `week_key`, `next_week`, `product_id`, `product_name`, `pricing_bl_25`,
    `price`, `next_price`, `cogs`, `next_cogs`, `comp_price`, `next_comp_price`, `pi`, `next_pi`
    """)

    uploaded = st.file_uploader(
        "Drop file di sini atau klik Browse",
        type=["csv", "xlsx", "xls"],
        key="pi_file",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded:
        st.success(f"✅ File diterima: **{uploaded.name}** ({uploaded.size / 1024:.1f} KB)", icon="✅")

        if st.button("▶ Run PI Decomposition", key="run_pi"):
            with st.spinner("Memproses data dan generate Excel…"):
                try:
                    pi_mod, err = _import_module("pi_revised")
                    if err:
                        st.error(f"❌ Gagal import `pi_revised.py`: {err}")
                    else:
                        file_bytes = uploaded.read()
                        excel_bytes, out_filename = pi_mod.run_pi(file_bytes, uploaded.name)
                        st.balloons()
                        st.success("✅ Analisis selesai! Klik tombol di bawah untuk download.", icon="🎉")
                        st.download_button(
                            label="⬇️ Download Hasil Excel (PI Analyzer)",
                            data=excel_bytes,
                            file_name=out_filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key="dl_pi",
                        )
                        with st.expander("📋 Sheet yang di-generate (13 sheets)"):
                            sheets = [
                                "0. Formula Reference", "1. Raw Data", "Executive Overview",
                                "1b. Aggregates", "2. PI Bridge", "2b. PI Bridge (±)",
                                "3. GV Tier", "4. L1 Category",
                                "5. Astro Price Distribution", "6. Comp Change",
                                "6b. SKU Bermasalah", "7. SKU Watch List", "8. Shapley Detail",
                            ]
                            for s in sheets:
                                st.markdown(f"- {s}")
                except Exception:
                    st.error("❌ Terjadi error saat proses. Lihat detail di bawah.")
                    st.code(traceback.format_exc(), language="python")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Pricing Simulator
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🧮 Pricing Simulator":
    st.markdown("""
    <div class="astro-header">
        <div>
            <h1>🧮 Pricing Simulator</h1>
            <p>Simulasi dampak skema harga baru terhadap Revenue, GP, dan Volume</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 📁 File 1 — Data Master")
        st.markdown("""
        **Kolom yang dibutuhkan:**
        `product_id`, `product_name`, `l1_category_name`, `pricing_bl_25`,
        `qty`, `selling_price`, `cost_price`
        """)
        file1 = st.file_uploader(
            "Upload Data Master",
            type=["csv", "xlsx", "xls"],
            key="sim_file1",
        )
        if file1:
            st.success(f"✅ {file1.name} ({file1.size / 1024:.1f} KB)")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 📁 File 2 — Skema Harga")
        st.markdown("""
        **Format (dibuat manual):**
        `product_id`, `baseline`, `var_1`, `var_2`, … (kolom variant tidak terbatas)
        """)
        file2 = st.file_uploader(
            "Upload Skema Harga",
            type=["csv", "xlsx", "xls"],
            key="sim_file2",
        )
        if file2:
            st.success(f"✅ {file2.name} ({file2.size / 1024:.1f} KB)")
        st.markdown('</div>', unsafe_allow_html=True)

    if file1 and file2:
        if st.button("▶ Run Pricing Simulation", key="run_sim"):
            with st.spinner("Menjalankan simulasi…"):
                try:
                    sim_mod, err = _import_module("sim_final")
                    if err:
                        st.error(f"❌ Gagal import `sim_final.py`: {err}")
                    else:
                        f1_bytes = file1.read()
                        f2_bytes = file2.read()
                        excel_bytes, out_filename = sim_mod.run_sim(
                            f1_bytes, file1.name, f2_bytes, file2.name
                        )
                        st.balloons()
                        st.success("✅ Simulasi selesai! Klik tombol di bawah untuk download.", icon="🎉")
                        st.download_button(
                            label="⬇️ Download Hasil Simulasi",
                            data=excel_bytes,
                            file_name=out_filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key="dl_sim",
                        )
                        with st.expander("📋 Sheet yang di-generate (3 sheets)"):
                            for s in ["Raw Data", "SKU Detail", "Summary Impact"]:
                                st.markdown(f"- {s}")
                except Exception:
                    st.error("❌ Terjadi error saat proses. Lihat detail di bawah.")
                    st.code(traceback.format_exc(), language="python")
    elif file1 or file2:
        st.warning("⚠️ Upload kedua file untuk menjalankan simulasi.", icon="⚠️")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — Query Reference
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗄️ Query Reference":
    st.markdown("""
    <div class="astro-header">
        <div>
            <h1>🗄️ Query Reference</h1>
            <p>Template BigQuery SQL untuk generate input data ke setiap tool</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Q1 — GP Bridge", "Q2 — PI Analyzer", "Q3 — Pricing Simulator"])

    with tab1:
        st.markdown("#### Query 1 — GP Bridge (Weekly Comparison)")
        st.markdown("""
        - **Tujuan:** Ambil data perbandingan 2 minggu untuk analisis GP Bridge & PVM
        - **Parameter:** Pilih DOW + 2 tanggal; `end_date = start_date + 6 hari`
        - **Output:** 1 row per SKU per minggu (current week & next week)
        """)
        st.code("""
-- Q1: GP Bridge — Weekly Data
-- Ganti: @start_date_1, @end_date_1 (minggu 1), @start_date_2, @end_date_2 (minggu 2)

SELECT
    FORMAT_DATE('%Y%m%d', DATE(@start_date_1))                AS week_key,
    FORMAT_DATE('%Y%m%d', DATE(@start_date_2))                AS next_week,
    p.product_id,
    p.product_name,
    p.pricing_bl_25,

    -- Week 1
    SUM(IF(DATE(o.created_at) BETWEEN @start_date_1 AND @end_date_1, o.qty, 0))            AS qty,
    AVG(IF(DATE(o.created_at) BETWEEN @start_date_1 AND @end_date_1, o.selling_price, NULL)) AS selling_price,
    AVG(IF(DATE(o.created_at) BETWEEN @start_date_1 AND @end_date_1, o.cost_price, NULL))   AS cost_price,

    -- Week 2
    SUM(IF(DATE(o.created_at) BETWEEN @start_date_2 AND @end_date_2, o.qty, 0))            AS qty1,
    AVG(IF(DATE(o.created_at) BETWEEN @start_date_2 AND @end_date_2, o.selling_price, NULL)) AS selling_price1,
    AVG(IF(DATE(o.created_at) BETWEEN @start_date_2 AND @end_date_2, o.cost_price, NULL))   AS cost_price1,

    -- Optional: competitor price & PI
    AVG(IF(DATE(c.date) BETWEEN @start_date_1 AND @end_date_1, c.comp_price, NULL))         AS comp_price,
    AVG(IF(DATE(c.date) BETWEEN @start_date_2 AND @end_date_2, c.comp_price, NULL))         AS comp_price1,
    AVG(IF(DATE(c.date) BETWEEN @start_date_1 AND @end_date_1, c.pi, NULL))                 AS pi,
    AVG(IF(DATE(c.date) BETWEEN @start_date_2 AND @end_date_2, c.pi, NULL))                 AS pi1,

    -- Optional: stock
    AVG(IF(DATE(s.date) BETWEEN @start_date_1 AND @end_date_1, s.avg_stock, NULL))          AS avg_stock,
    AVG(IF(DATE(s.date) BETWEEN @start_date_2 AND @end_date_2, s.avg_stock, NULL))          AS avg_stock1,

    p.pareto_classification

FROM `astro-data-prd.astro_datamart.dim_products`        p
LEFT JOIN `astro-data-prd.astro_datamart.fct_orders`     o  USING (product_id)
LEFT JOIN `astro-data-prd.astro_datamart.fct_comp_price` c  USING (product_id)
LEFT JOIN `astro-data-prd.astro_datamart.fct_stock`      s  USING (product_id)

WHERE p.pricing_bl_25 IN ('Dry', 'Fresh', 'Frozen', 'PL')

GROUP BY 1,2,3,4,5,18
ORDER BY p.pricing_bl_25, p.product_name
        """, language="sql")

    with tab2:
        st.markdown("#### Query 2 — PI Analyzer (Weekly Comparison)")
        st.markdown("""
        - **Tujuan:** Analisis perubahan Pricing Index vs kompetitor
        - **Parameter:** Sama dengan Q1 (DOW + 2 tanggal)
        - **Output:** 1 row per SKU dengan harga Astro, COGS, kompetitor, dan PI per 2 minggu
        """)
        st.code("""
-- Q2: PI Analyzer — Weekly Data
-- Ganti: @start_date_1, @end_date_1, @start_date_2, @end_date_2

SELECT
    FORMAT_DATE('%Y%m%d', DATE(@start_date_1))                AS week_key,
    FORMAT_DATE('%Y%m%d', DATE(@start_date_2))                AS next_week,
    p.product_id,
    p.product_name,
    p.pricing_bl_25,

    -- Week 1
    AVG(IF(DATE(o.created_at) BETWEEN @start_date_1 AND @end_date_1, o.selling_price, NULL)) AS price,
    AVG(IF(DATE(o.created_at) BETWEEN @start_date_1 AND @end_date_1, o.cost_price, NULL))   AS cogs,
    AVG(IF(DATE(c.date) BETWEEN @start_date_1 AND @end_date_1, c.comp_price, NULL))         AS comp_price,
    AVG(IF(DATE(c.date) BETWEEN @start_date_1 AND @end_date_1, c.pi, NULL))                 AS pi,

    -- Week 2
    AVG(IF(DATE(o.created_at) BETWEEN @start_date_2 AND @end_date_2, o.selling_price, NULL)) AS next_price,
    AVG(IF(DATE(o.created_at) BETWEEN @start_date_2 AND @end_date_2, o.cost_price, NULL))   AS next_cogs,
    AVG(IF(DATE(c.date) BETWEEN @start_date_2 AND @end_date_2, c.comp_price, NULL))         AS next_comp_price,
    AVG(IF(DATE(c.date) BETWEEN @start_date_2 AND @end_date_2, c.pi, NULL))                 AS next_pi

FROM `astro-data-prd.astro_datamart.dim_products`        p
LEFT JOIN `astro-data-prd.astro_datamart.fct_orders`     o  USING (product_id)
LEFT JOIN `astro-data-prd.astro_datamart.fct_comp_price` c  USING (product_id)

WHERE p.pricing_bl_25 IN ('Dry', 'Fresh', 'Frozen', 'PL')

GROUP BY 1,2,3,4,5
ORDER BY p.pricing_bl_25, p.product_name
        """, language="sql")

    with tab3:
        st.markdown("#### Query 3 — Pricing Simulator (Flexible Date Range)")
        st.markdown("""
        - **Tujuan:** Ambil data master untuk simulasi dampak perubahan harga
        - **Parameter:** `@start_date` + `@end_date` bebas (tidak harus weekly)
        - **Output:** 1 row per SKU dengan aggregated qty, avg price, avg COGS
        """)
        st.code("""
-- Q3: Pricing Simulator — Master Data
-- Ganti: @start_date, @end_date (bebas)

SELECT
    p.product_id,
    p.product_name,
    p.l1_category_name,
    p.pricing_bl_25,
    SUM(o.qty)              AS qty,
    AVG(o.selling_price)    AS selling_price,
    AVG(o.cost_price)       AS cost_price

FROM `astro-data-prd.astro_datamart.dim_products`    p
LEFT JOIN `astro-data-prd.astro_datamart.fct_orders` o  USING (product_id)

WHERE
    p.pricing_bl_25 IN ('Dry', 'Fresh', 'Frozen', 'PL')
    AND DATE(o.created_at) BETWEEN @start_date AND @end_date

GROUP BY 1,2,3,4
ORDER BY p.pricing_bl_25, p.product_name
        """, language="sql")

    st.markdown("---")
    st.markdown("""
    <div class="section-card">
    <h3>📌 Catatan Penting</h3>

    - Query di atas adalah **template** — sesuaikan nama kolom dan tabel dengan schema BigQuery Astro yang sebenarnya
    - Table prefix: <code>astro-data-prd.astro_datamart.*</code>
    - <code>pricing_bl_25</code> berisi: <b>Dry, Fresh, Frozen, PL</b>
    - Untuk Q1 & Q2: <code>end_date = start_date + 6 hari</code> (1 minggu penuh)
    - Export dari BigQuery ke CSV/Excel sebelum upload ke tool ini
    </div>
    """, unsafe_allow_html=True)


# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🚀 Astro Pricing Tools &nbsp;·&nbsp; Built with Streamlit &nbsp;·&nbsp; Pricing Strategy Team
</div>
""", unsafe_allow_html=True)
