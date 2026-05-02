import streamlit as st
import io, traceback, datetime
import pandas as pd
import numpy as np

LOGO_B64 = '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'
Q1_TEMPLATE = "WITH \ndate_dict as (\nselect\ndate('{START_DATE}') start_date,\ndate('{END_DATE}') end_date\n)\n\n  ,label AS (\n  SELECT\n    product_id,\n    grouping_label,\n  FROM\n    `astro-data-prd.astro_google_sheet.temp_grouping_label_by_sku`\n)\n\n,raw_stock AS(\nSELECT\n  DISTINCT \n  DATE_TRUNC(DATE_ADD(main.date_key, INTERVAL 0 DAY), WEEK({DOW})) + 0 week_key,\n  date_key,\n  product_id,\n  main.product_name,\n  start_available_stock,\n  FROM astro-data-prd.astro_datamart_supply_chain.rpt_overall_stock_movement AS main\n  LEFT JOIN label USING (product_id)\n  WHERE date_key BETWEEN (select distinct date(start_date) from date_dict) and (select distinct date(end_date) from date_dict)\n)\n\n,weekly_stock AS(\nSELECT week_key, product_id, \n  AVG(start_available_stock) avg_stock\nFROM (\n    SELECT week_key, date_key, rm.product_id,\n      SUM(IFNULL(start_available_stock,0)) AS start_available_stock,\n    FROM raw_stock rm GROUP BY ALL\n)\nGROUP BY ALL\n)\n\n,raw1_dim_prod AS(\nSELECT product_id, l1_category_name,\n  `astro-data-prd.astro_function.business_lines_2025`(private_label_or_retail, pr.l1_category_name, pr.food_or_non_food, pr.product_type_name) business_lines_2025,\nFROM `astro-data-prd.astro_dataset.dim_products_x_categories_x_attributes` pr\nGROUP BY ALL \n) \n\n,dim_prod AS(SELECT product_id, \nCASE \nWHEN REGEXP_CONTAINS(LOWER(l1_category_name), r'ayam|unggas|seafood|daging beku') THEN 'Frozen'\nWHEN REGEXP_CONTAINS(LOWER(l1_category_name), r'buah|sayur|telur|tahu|tempe') THEN 'Fresh'\nWHEN REGEXP_CONTAINS(LOWER(business_lines_2025), r'ab|ag|ak') THEN 'PL'\nWHEN REGEXP_CONTAINS(LOWER(business_lines_2025), r'dry food|dry non food') THEN 'Dry'\nELSE 'Others'\nEND AS pricing_bl_25,\nFROM raw1_dim_prod GROUP BY ALL)\n\n,pareto AS(\nSELECT product_id, pareto_classification\nFROM astro-data-prd.astro_datamart_commercial.fact_pareto_per_product_x_sku_scoring_astro_level_qcom\nWHERE 1=1 \nAND month_key = DATE_TRUNC((select distinct date(end_date) from date_dict),MONTH)\nGROUP BY ALL \n) \n\n,raw_main AS(\n  SELECT\n  DATE_TRUNC(date_key,MONTH) month_key, \n  DATE_TRUNC(DATE_ADD(date_key, INTERVAL 0 DAY), WEEK({DOW})) + 0 week_key,\n  date_key, product_id, \n  selling_price*100/pi comp_price,\nFROM astro-data-prd.astro_datamart_buyer_exp.rpt_pricing_suggested_price_simulation\nLEFT JOIN dim_prod USING(product_id)\nWHERE date_key between (select distinct date(start_date) from date_dict) and (select distinct date(end_date) from date_dict)\nAND pi <> 0 AND converted_type = 'exact match' AND pi IS NOT NULL AND pricing_bl_25 = 'Dry'\nGROUP BY ALL\n\nUNION ALL \n\n  SELECT\n  DATE_TRUNC(date_key,MONTH) month_key, \n  DATE_TRUNC(DATE_ADD(date_key, INTERVAL 0 DAY), WEEK({DOW})) + 0 week_key,\n  date_key, product_id, \n  selling_price*100/pi comp_price,\nFROM astro-data-prd.astro_datamart_buyer_exp.rpt_pricing_suggested_price_simulation\nLEFT JOIN dim_prod USING(product_id)\nWHERE date_key between (select distinct date(start_date) from date_dict) and (select distinct date(end_date) from date_dict)\nAND pi <> 0 AND converted_type = 'overall' AND pi IS NOT NULL AND pricing_bl_25 IN ('Fresh','Frozen')\nGROUP BY ALL\n)\n\n,main AS(SELECT week_key, product_id, AVG(comp_price) comp_price FROM raw_main GROUP BY ALL)\n\n,raw_rpt as (\n  select distinct\n  DATE_TRUNC(DATE_ADD(a.date_key, INTERVAL 0 DAY), WEEK({DOW})) + 0 week_key,\n    a.product_id, a.product_name, pricing_bl_25, l1_category_name, business_lines_2025,\n    comp_price, \n    SUM(a.goods_value) goods_value, SUM(a.quantity_sold) AS qty, SUM(total_cogs) cogs,\n    SAFE_DIVIDE(SUM(goods_value), SUM(a.quantity_sold)) AS selling_price,\n    SAFE_DIVIDE(SUM(total_cogs), SUM(a.quantity_sold)) AS cost_price,\n  from astro-data-prd.astro_datamart.rpt_gross_margin a\n  LEFT JOIN dim_prod dp ON a.product_id = dp.product_id\n  LEFT JOIN main r ON a.product_id = r.product_id AND DATE_TRUNC(DATE_ADD(a.date_key, INTERVAL 0 DAY), WEEK({DOW})) + 0 = r.week_key\n  where a.date_key between (select distinct date(start_date) from date_dict) and (select distinct date(end_date) from date_dict)\n  and order_id_sales is not null and a.goods_value > 0 and a.location_type = 'overall'\n  and order_type not in ('KITCHEN')\n  GROUP BY ALL\n)\n\n,list_prod AS(\n  SELECT product_id, product_name, pricing_bl_25, l1_category_name, business_lines_2025,\n  FROM raw_rpt \n  WHERE week_key IN(\n    DATE_TRUNC(DATE_ADD((SELECT DATE(start_date) FROM date_dict LIMIT 1),INTERVAL 0 DAY),WEEK({DOW})),\n    DATE_TRUNC(DATE_ADD((SELECT DATE(end_date) FROM date_dict LIMIT 1),INTERVAL 0 DAY),WEEK({DOW}))\n  )\n  GROUP BY ALL\n)\n\nSELECT \nDATE_TRUNC(DATE_ADD((SELECT DATE(start_date) FROM date_dict LIMIT 1),INTERVAL 0 DAY),WEEK({DOW})) AS week_key,\nDATE_TRUNC(DATE_ADD((SELECT DATE(end_date) FROM date_dict LIMIT 1),INTERVAL 0 DAY),WEEK({DOW})) AS next_week,\nl.*, pareto_classification,\na.qty, b.qty AS qty1,\na.selling_price, b.selling_price AS selling_price1,\na.cost_price, b.cost_price AS cost_price1,\nSAFE_DIVIDE(a.selling_price-a.cost_price,a.selling_price) AS margin_pct,\nSAFE_DIVIDE(b.selling_price-b.cost_price,b.selling_price) AS margin1_pct,\na.comp_price, b.comp_price AS comp_price1,\nSAFE_DIVIDE(a.selling_price*100,a.comp_price) AS pi,\nSAFE_DIVIDE(b.selling_price*100,b.comp_price) AS pi1,\nc.avg_stock, d.avg_stock AS avg_stock1,\nFROM list_prod l\nLEFT JOIN (SELECT * FROM raw_rpt WHERE week_key = DATE_TRUNC(DATE_ADD((SELECT DATE(start_date) FROM date_dict LIMIT 1),INTERVAL 0 DAY),WEEK({DOW}))) a USING(product_id) \nLEFT JOIN (SELECT * FROM raw_rpt WHERE week_key = DATE_TRUNC(DATE_ADD((SELECT DATE(end_date) FROM date_dict LIMIT 1),INTERVAL 0 DAY),WEEK({DOW}))) b USING(product_id) \nLEFT JOIN (SELECT * FROM weekly_stock WHERE week_key = DATE_TRUNC(DATE_ADD((SELECT DATE(start_date) FROM date_dict LIMIT 1),INTERVAL 0 DAY),WEEK({DOW}))) c USING(product_id) \nLEFT JOIN (SELECT * FROM weekly_stock WHERE week_key = DATE_TRUNC(DATE_ADD((SELECT DATE(end_date) FROM date_dict LIMIT 1),INTERVAL 0 DAY),WEEK({DOW}))) d USING(product_id) \nLEFT JOIN pareto USING(product_id)"
Q2_TEMPLATE = "WITH\ndate_dict as (\nselect\ndate('{START_DATE}') start_date,\ndate('{END_DATE}') end_date\n)\n\n,cogs_date as (\nselect distinct product_id, cogs, date_key \nfrom astro_dataset.fact_cogs_per_product_per_date \nwhere date_key between (select distinct date(start_date) from date_dict) and (select distinct date(end_date) from date_dict)\n)\n\n,raw_price AS(\nSELECT date_key, product_id, price_full_final AS price\nFROM `astro-data-prd.astro_dataset.fact_mode_price_per_product_daily`\nWHERE date_key between (select distinct date(start_date) from date_dict) and (select distinct date(end_date) from date_dict)\nAND price_full_final <> 0 AND price_full_final IS NOT NULL\nGROUP BY ALL\n)\n\n,raw1_dim_prod AS(\nSELECT product_id, l1_category_name, product_name, source_status,\n  `astro-data-prd.astro_function.business_lines_2025`(private_label_or_retail, pr.l1_category_name, pr.food_or_non_food, pr.product_type_name) business_lines_2025,\nFROM `astro-data-prd.astro_dataset.dim_products_x_categories_x_attributes` pr\nGROUP BY ALL \n) \n\n,dim_prod AS(SELECT product_id, l1_category_name, product_name, source_status,\nCASE \nWHEN REGEXP_CONTAINS(LOWER(l1_category_name), r'ayam|unggas|seafood|daging beku') THEN 'Frozen'\nWHEN REGEXP_CONTAINS(LOWER(l1_category_name), r'buah|sayur|telur|tahu|tempe') THEN 'Fresh'\nWHEN REGEXP_CONTAINS(LOWER(business_lines_2025), r'ab|ag|ak') THEN 'PL'\nWHEN REGEXP_CONTAINS(LOWER(business_lines_2025), r'dry food|dry non food') THEN 'Dry'\nELSE 'Others'\nEND AS pricing_bl_25,\nFROM raw1_dim_prod GROUP BY ALL)\n\n,pareto AS(\nSELECT product_id, pareto_classification\nFROM astro-data-prd.astro_datamart_commercial.fact_pareto_per_product_x_sku_scoring_astro_level_qcom\nWHERE 1=1 AND month_key = DATE_TRUNC((select distinct date(end_date) from date_dict),MONTH)\nGROUP BY ALL \n) \n\n,raw_main AS(\n  SELECT DATE_TRUNC(date_key,MONTH) month_key, date_key,\n  DATE_TRUNC(DATE_ADD(date_key, INTERVAL 0 DAY), WEEK({DOW})) + 0 week_key,\n  product_id, dp.product_name, dp.l1_category_name, dp.source_status, pricing_bl_25,\n  selling_price AS price, c.cogs, selling_price*100/pi comp_price,\nFROM astro-data-prd.astro_datamart_buyer_exp.rpt_pricing_suggested_price_simulation\n  LEFT JOIN dim_prod dp USING(product_id)\n  LEFT JOIN cogs_date c USING(product_id,date_key)\nWHERE date_key between (select distinct date(start_date) from date_dict) and (select distinct date(end_date) from date_dict)\nAND pi <> 0 AND pi IS NOT NULL AND converted_type = 'overall'\nAND dp.source_status = 'SOURCE' AND pricing_bl_25 NOT IN ('PL','Dry')\nGROUP BY ALL\n\nUNION ALL \n\n  SELECT DATE_TRUNC(date_key,MONTH) month_key, date_key,\n  DATE_TRUNC(DATE_ADD(date_key, INTERVAL 0 DAY), WEEK({DOW})) + 0 week_key,\n  product_id, dp.product_name, dp.l1_category_name, dp.source_status, pricing_bl_25,\n  selling_price AS price, c.cogs, selling_price*100/pi comp_price,\nFROM astro-data-prd.astro_datamart_buyer_exp.rpt_pricing_suggested_price_simulation\n  LEFT JOIN dim_prod dp USING(product_id)\n  LEFT JOIN cogs_date c USING(product_id,date_key)\nWHERE date_key between (select distinct date(start_date) from date_dict) and (select distinct date(end_date) from date_dict)\nAND pi <> 0 AND pi IS NOT NULL AND converted_type = 'exact match'\nAND dp.source_status = 'SOURCE' AND pricing_bl_25 IN ('Dry')\nGROUP BY ALL\n)\n\n,main1 AS(SELECT week_key, product_id, product_name, l1_category_name, source_status, pricing_bl_25,\n  AVG(price) price, AVG(cogs) cogs, AVG(comp_price) comp_price FROM raw_main GROUP BY ALL)\n\n,main AS(SELECT week_key, product_id, product_name, l1_category_name, source_status, pricing_bl_25,\n  price, cogs, SAFE_DIVIDE(price-cogs,price) gp_pct, comp_price,\n  SAFE_DIVIDE(price*100,comp_price) pi, SAFE_DIVIDE(cogs*100,comp_price) cogs_index FROM main1)\n\n,dict AS(SELECT product_id, product_name, l1_category_name, source_status, pricing_bl_25 FROM main GROUP BY ALL)\n\nSELECT\nDATE_TRUNC(DATE_ADD((SELECT DATE(start_date) FROM date_dict LIMIT 1),INTERVAL 0 DAY),WEEK({DOW})) week_key,\nDATE_TRUNC(DATE_ADD((SELECT DATE(end_date) FROM date_dict LIMIT 1),INTERVAL 0 DAY),WEEK({DOW})) next_week,\nd.product_id, d.product_name, d.l1_category_name, d.source_status, d.pricing_bl_25,\npareto_classification,\nm1.price, m2.price AS next_price,\nm1.cogs, m2.cogs AS next_cogs,\nm1.comp_price, m2.comp_price AS next_comp_price,\nm1.pi, m2.pi AS next_pi,\nFROM dict d\nLEFT JOIN (SELECT * FROM main m2 WHERE week_key = DATE_TRUNC(DATE_ADD((SELECT DATE(start_date) FROM date_dict LIMIT 1),INTERVAL 0 DAY),WEEK({DOW}))) m1 ON m1.product_id = d.product_id\nLEFT JOIN (SELECT * FROM main m2 WHERE week_key = DATE_TRUNC(DATE_ADD((SELECT DATE(end_date) FROM date_dict LIMIT 1),INTERVAL 0 DAY),WEEK({DOW}))) m2 ON d.product_id = m2.product_id \nLEFT JOIN pareto p ON d.product_id = p.product_id"
Q3_TEMPLATE = "WITH \ndate_dict as (\nselect\ndate('{START_DATE}') start_date,\ndate('{END_DATE}') end_date\n)\n\n,raw1_dim_prod AS(\nSELECT product_id, product_name, l1_category_name, l2_category_name,\n  `astro-data-prd.astro_function.business_lines_2025`(private_label_or_retail, pr.l1_category_name, pr.food_or_non_food, pr.product_type_name) business_lines_2025,\nFROM `astro-data-prd.astro_dataset.dim_products_x_categories_x_attributes` pr\nGROUP BY ALL \n) \n\n,dim_prod AS(SELECT product_id,\nCASE \nWHEN REGEXP_CONTAINS(LOWER(l1_category_name), r'ayam|unggas|seafood|daging beku') THEN 'Frozen'\nWHEN REGEXP_CONTAINS(LOWER(l1_category_name), r'buah|sayur|telur|tahu|tempe') THEN 'Fresh'\nWHEN REGEXP_CONTAINS(LOWER(business_lines_2025), r'ab|ag|ak') THEN 'PL'\nWHEN REGEXP_CONTAINS(LOWER(business_lines_2025), r'dry food|dry non food') THEN 'Dry'\nELSE 'Others'\nEND AS pricing_bl_25,\nproduct_name, l1_category_name, l2_category_name,\nFROM raw1_dim_prod GROUP BY ALL)\n\nSELECT DISTINCT\n    a.product_id, dp.product_name, dp.l1_category_name, dp.l2_category_name,\n    pricing_bl_25,\n    SUM(a.quantity_sold) AS qty,\n    SAFE_DIVIDE(SUM(goods_value), SUM(a.quantity_sold)) AS selling_price,\n    SAFE_DIVIDE(SUM(total_cogs), SUM(a.quantity_sold)) AS cost_price,\nFROM astro-data-prd.astro_datamart.rpt_gross_margin a\nLEFT JOIN dim_prod dp ON a.product_id = dp.product_id\nWHERE a.date_key BETWEEN (SELECT DATE(start_date) FROM date_dict) AND (SELECT DATE(end_date) FROM date_dict)\nAND order_id_sales is not null AND a.goods_value > 0\nAND a.location_type = 'overall' AND order_type not in ('KITCHEN')\nGROUP BY ALL"


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
.stButton>button { background:linear-gradient(135deg,#0083FF,#003DA6); color:white !important; font-family:'Nunito',sans-serif; font-weight:700; border:none; border-radius:10px; padding:10px 28px; width:100%; }
[data-testid="stDownloadButton"] button { background:#00a651 !important; color:white !important; font-family:'Nunito',sans-serif !important; font-weight:700 !important; border-radius:10px !important; width:100%; }
[data-testid="stFileUploader"] { background:#f0f6ff; border:2px dashed #0083FF; border-radius:10px; padding:6px; }
.hint-box { background:#E6F2FF; border-left:4px solid #0083FF; border-radius:0 8px 8px 0; padding:12px 16px; margin-bottom:16px; font-size:0.88rem; }
.q-card { background:#f8faff; border:1px solid #dce8ff; border-radius:12px; padding:16px 20px; margin-bottom:16px; }
.q-badge { display:inline-block; background:#0083FF; color:white; font-weight:700; font-size:0.8rem; border-radius:6px; padding:2px 10px; margin-right:8px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:16px 0 8px;">
        <img src="data:image/png;base64,{LOGO_B64}"
             style="width:80px;height:80px;object-fit:contain;display:block;margin:0 auto 8px;"/>
        <div style="font-family:'Nunito',sans-serif;font-size:1.05rem;font-weight:800;color:white;">Astro Pricing Tools</div>
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
    try: return df.style.map(color_delta, subset=cols)
    except AttributeError: return df.style.applymap(color_delta, subset=cols)

def fmt_idr(v):
    try: return f"Rp {float(v):,.0f}"
    except: return str(v)

DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
DOW_MAP = {d: i for i, d in enumerate(DAYS)}

def get_valid_dates(dow_name):
    dow_num = DOW_MAP[dow_name]
    result = []
    for yr in [2024, 2025, 2026, 2027]:
        d = datetime.date(yr, 1, 1)
        while d.year == yr:
            if d.weekday() == dow_num:
                result.append(d)
            d += datetime.timedelta(days=1)
    return result

# ── Session state keys for persisting results ────────────────────────────────
for _k in ["pvm_result","pi_result","sim_result"]:
    if _k not in st.session_state:
        st.session_state[_k] = None


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — GP Bridge
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 GP Bridge":
    st.markdown("""<div class="astro-header">
    <h1>📊 GP Bridge & PVM Decomposition</h1>
    <p>Price · Volume · Mix · COGS · New & Churned SKU Effect</p></div>""", unsafe_allow_html=True)

    st.markdown("""<div class="hint-box">
    <b>Kolom wajib:</b> <code>week_key</code>, <code>next_week</code>, <code>product_id</code>,
    <code>product_name</code>, <code>pricing_bl_25</code>, <code>qty</code>, <code>qty1</code>,
    <code>selling_price</code>, <code>selling_price1</code>, <code>cost_price</code>, <code>cost_price1</code><br>
    <b>Opsional:</b> <code>comp_price</code>, <code>comp_price1</code>, <code>pi</code>, <code>pi1</code>,
    <code>avg_stock</code>, <code>pareto_classification</code>
    </div>""", unsafe_allow_html=True)

    st.dataframe(pd.DataFrame({
        "week_key":  ["2026-04-07"]*3, "next_week": ["2026-04-14"]*3,
        "product_id":["1001","1002","1003"], "product_name":["Indomie Goreng","Ayam Fillet 500g","Tomat 500g"],
        "pricing_bl_25":["Dry","Frozen","Fresh"],
        "qty":[500,120,300], "qty1":[480,135,290],
        "selling_price":[3500,42000,8500], "selling_price1":[3500,43000,8500],
        "cost_price":[2800,35000,6200], "cost_price1":[2850,36000,6400],
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

                    # Build summary dataframes
                    buf2 = io.BytesIO(file_bytes)
                    ext  = uploaded.name.rsplit(".",1)[-1].lower()
                    df_raw = pd.read_csv(buf2) if ext=="csv" else pd.read_excel(buf2)
                    df_raw = _pvm.ensure_cols(df_raw)
                    p1c, p2c = _pvm.detect_period(df_raw)
                    if p1c is None: p1c, p2c = "week_key","next_week"
                    df_e  = _pvm.enrich(df_raw, p1c, p2c)
                    pvm   = _pvm.compute_pvm(df_e)
                    BLS   = ["Dry","Fresh","Frozen","PL"]

                    rows1 = []
                    for bl in BLS + ["TOTAL"]:
                        p = pvm[bl]
                        rows1.append({"BL":bl,
                            "Margin P1":f"{p['m_base']*100:.2f}%","Margin P2":f"{p['m_end']*100:.2f}%",
                            "Δ Total":f"{p['pp_total']*100:+.2f}pp","1.Churned":f"{p['pp_B']*100:+.2f}pp",
                            "2.1 COGS":f"{p['pp_cogs']*100:+.2f}pp","2.2 Price":f"{p['pp_price']*100:+.2f}pp",
                            "2.3 VolMix":f"{p['pp_volmix']*100:+.2f}pp","3.New SKU":f"{p['pp_G']*100:+.2f}pp"})
                    rows2 = []
                    for bl in BLS + ["TOTAL"]:
                        p = pvm[bl]; delta = p['gp_end']-p['gp_start']
                        rows2.append({"BL":bl,"GP P1":fmt_idr(p['gp_start']),"GP P2":fmt_idr(p['gp_end']),
                            "Δ GP":fmt_idr(delta),"Δ GP%":f"{delta/p['gp_start']*100:+.1f}%" if p['gp_start']!=0 else "N/A",
                            "1.Churned":fmt_idr(-p.get('gp_dep',0)),"2.1 COGS":fmt_idr(p['cogs_rp']),
                            "2.2 Price":fmt_idr(p['price_rp']),"2.3 VolMix":fmt_idr(p['volmix_rp']),
                            "3.New SKU":fmt_idr(p.get('gp_new',0))})
                    effects = [("Margin P1","m_base",False),("1. Churned SKU","pp_B",True),
                               ("2.1 COGS Effect","pp_cogs",True),("2.2 Price Effect","pp_price",True),
                               ("2.3 Vol-Mix Effect","pp_volmix",True),("3. New SKU","pp_G",True),
                               ("Margin P2","m_end",False)]
                    rows3 = []
                    for label, key, is_delta in effects:
                        row = {"Effect": label}
                        for bl in BLS+["TOTAL"]:
                            v = pvm[bl][key]
                            row[bl] = f"{v*100:.2f}%" if not is_delta else f"{v*100:+.2f}pp"
                        rows3.append(row)

                    # Save to session state
                    st.session_state["pvm_result"] = {
                        "excel_bytes": excel_bytes, "out_filename": out_filename,
                        "df1": pd.DataFrame(rows1), "df2": pd.DataFrame(rows2), "df3": pd.DataFrame(rows3),
                        "BLS": BLS
                    }
                except Exception:
                    st.error("❌ Error:"); st.code(traceback.format_exc(), language="python")

    # Show results (persists after download)
    if st.session_state["pvm_result"]:
        r = st.session_state["pvm_result"]
        st.success("✅ Selesai!")
        st.download_button("⬇️ Download Excel (GP Bridge)", data=r["excel_bytes"],
            file_name=r["out_filename"],
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="dl_pvm")
        st.markdown("---")
        st.markdown("### 📊 Summary Preview")
        st.markdown("#### Tabel 1 — Margin Bridge per BL (pp)")
        st.dataframe(style_df(r["df1"],["Δ Total","1.Churned","2.1 COGS","2.2 Price","2.3 VolMix","3.New SKU"]),
                     hide_index=True, use_container_width=True)
        st.markdown("#### Tabel 1A — GP Bridge (IDR)")
        st.dataframe(style_df(r["df2"],["Δ GP","Δ GP%"]), hide_index=True, use_container_width=True)
        st.markdown("#### Tabel pp Bridge Summary")
        BLS = r["BLS"]
        st.dataframe(style_df(r["df3"], BLS+["TOTAL"]), hide_index=True, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PI Analyzer
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈 PI Analyzer":
    st.markdown("""<div class="astro-header">
    <h1>📈 Price Index Decomposition</h1>
    <p>Shapley Value — Churned · Price Change · Comp Change · New SKU</p></div>""", unsafe_allow_html=True)

    st.markdown("""<div class="hint-box">
    <b>Kolom:</b> <code>week_key</code>, <code>next_week</code>, <code>product_id</code>,
    <code>product_name</code>, <code>pricing_bl_25</code>, <code>price</code>, <code>next_price</code>,
    <code>cogs</code>, <code>next_cogs</code>, <code>comp_price</code>, <code>next_comp_price</code>,
    <code>pi</code>, <code>next_pi</code>
    </div>""", unsafe_allow_html=True)

    st.dataframe(pd.DataFrame({
        "week_key":["2026-04-07"]*3,"next_week":["2026-04-14"]*3,
        "product_id":["1001","1002","1003"],"pricing_bl_25":["Dry","Frozen","Fresh"],
        "price":[3500,42000,8500],"next_price":[3500,43000,8500],
        "comp_price":[3400,41000,8200],"next_comp_price":[3300,41500,8800],
        "pi":[102.94,102.44,103.66],"next_pi":[106.06,103.61,96.59],
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

                    buf2 = io.BytesIO(file_bytes)
                    ext  = uploaded.name.rsplit(".",1)[-1].lower()
                    df_raw = pd.read_csv(buf2) if ext=="csv" else pd.read_excel(buf2)
                    d = _pi.enrich(df_raw)
                    ov, sr, contribs = _pi.precompute(d)
                    segs = ["Dry","Fresh","Frozen"]
                    effects_pi = [
                        ("PI P1",                     "A",         False),
                        ("1. Churned SKU Effect",      "eff_dep",   True),
                        ("2. Existing SKU (2.1+2.2)",  None,        True),
                        ("  2.1 Price Change",         "eff_price", True),
                        ("  2.2 Comp Change",          "eff_comp",  True),
                        ("3. New SKU Effect",          "eff_new",   True),
                        ("PI P2",                     "E",         False),
                    ]
                    rows_pi = []
                    for label, key, is_delta in effects_pi:
                        row = {"Effect": label}
                        for seg in segs + ["Overall"]:
                            src_ov = ov; src_sr = sr.get(seg,{}); src_ct = contribs.get(seg,{})
                            if key is None:
                                ep = src_ct.get("eff_price",0) if seg!="Overall" else ov.get("eff_price",0)
                                ec = src_ct.get("eff_comp",0)  if seg!="Overall" else ov.get("eff_comp",0)
                                v = ep + ec
                            elif seg == "Overall":
                                v = src_ov.get(key, 0)
                            elif key in ("A","E"):
                                v = src_sr.get(key, 0)
                            else:
                                v = src_ct.get(key, src_sr.get(key, 0))
                            row[seg] = f"{v:.2f}" if not is_delta else f"{v:+.2f}pp"
                        rows_pi.append(row)

                    st.session_state["pi_result"] = {
                        "excel_bytes": excel_bytes, "out_filename": out_filename,
                        "df_pi": pd.DataFrame(rows_pi)
                    }
                except Exception:
                    st.error("❌ Error:"); st.code(traceback.format_exc(), language="python")

    if st.session_state["pi_result"]:
        r = st.session_state["pi_result"]
        st.success("✅ Selesai!")
        st.download_button("⬇️ Download Excel (PI Analyzer)", data=r["excel_bytes"],
            file_name=r["out_filename"],
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="dl_pi")
        st.markdown("---")
        st.markdown("### 📊 Summary Preview — PI Bridge per BL")
        st.dataframe(style_df(r["df_pi"], ["Dry","Fresh","Frozen","Overall"]),
                     hide_index=True, use_container_width=True)
        st.caption("Hijau = berkontribusi positif pada PI · Merah = negatif")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Pricing Simulator
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🧮 Pricing Simulator":
    st.markdown("""<div class="astro-header">
    <h1>🧮 Pricing Simulator</h1>
    <p>Simulasi dampak skema harga baru terhadap Revenue, GP, dan Volume</p></div>""", unsafe_allow_html=True)

    col_h1, col_h2 = st.columns(2)
    with col_h1:
        st.markdown("""<div class="hint-box"><b>File 1 — Data Master (Q3):</b><br>
        <code>product_id</code>, <code>product_name</code>, <code>l1_category_name</code>,
        <code>pricing_bl_25</code>, <code>qty</code>, <code>selling_price</code>, <code>cost_price</code></div>""",
        unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            "product_id":["1001","1002","1003"],
            "product_name":["Indomie Goreng","Ayam Fillet","Tomat"],
            "l1_category_name":["Mie Instan","Daging Beku","Sayuran"],
            "pricing_bl_25":["Dry","Frozen","Fresh"],
            "qty":[12500,3200,7800],"selling_price":[3500,42000,8500],"cost_price":[2800,35000,6200],
        }), hide_index=True, use_container_width=True)
    with col_h2:
        st.markdown("""<div class="hint-box"><b>File 2 — Skema Harga (buat manual):</b><br>
        Kolom 1: <code>product_id</code> · Kolom 2: <code>baseline</code> ·
        Kolom 3+: variant harga (nama & jumlah kolom bebas)</div>""", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            "product_id":["1001","1002","1003"],
            "baseline":[3500,42000,8500],"var_1":[3300,40000,8000],"var_2":[3000,38000,7500],
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

                    # Parse summary from excel
                    import openpyxl as _xl
                    df_sum_parsed = None
                    try:
                        wb_out = _xl.load_workbook(io.BytesIO(excel_bytes), data_only=True)
                        ws_sum = wb_out["Summary Impact"]
                        all_rows = list(ws_sum.values)
                        header_idx = None
                        for i, row in enumerate(all_rows):
                            non_empty = [c for c in row if c is not None and str(c).strip() != ""]
                            if len(non_empty) >= 3:
                                header_idx = i; break
                        if header_idx is not None:
                            raw_headers = list(all_rows[header_idx])
                            seen = {}; headers = []
                            for h in raw_headers:
                                h_str = str(h) if h is not None else ""
                                if h_str in seen: seen[h_str]+=1; headers.append(f"{h_str}_{seen[h_str]}")
                                else: seen[h_str]=0; headers.append(h_str)
                            data_rows_sum = []
                            for row in all_rows[header_idx+1:]:
                                if any(c is not None and str(c).strip()!="" for c in row):
                                    data_rows_sum.append([str(c) if c is not None else "" for c in row])
                            if data_rows_sum:
                                df_sum_parsed = pd.DataFrame(data_rows_sum, columns=headers)
                    except Exception as e_parse:
                        pass

                    st.session_state["sim_result"] = {
                        "excel_bytes": excel_bytes, "out_filename": out_filename,
                        "df_sum": df_sum_parsed
                    }
                except Exception:
                    st.error("❌ Error:"); st.code(traceback.format_exc(), language="python")
    elif file1 or file2:
        st.warning("⚠️ Upload kedua file untuk menjalankan simulasi.")

    if st.session_state["sim_result"]:
        r = st.session_state["sim_result"]
        st.success("✅ Simulasi selesai!")
        st.download_button("⬇️ Download Hasil Simulasi", data=r["excel_bytes"],
            file_name=r["out_filename"],
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="dl_sim")
        if r["df_sum"] is not None:
            st.markdown("---")
            st.markdown("### 📊 Summary Impact Preview")
            df_sum = r["df_sum"]
            delta_cols = [c for c in df_sum.columns if any(x in str(c) for x in ["Δ","delta","%","diff"])]
            st.dataframe(style_df(df_sum, delta_cols) if delta_cols else df_sum,
                         hide_index=True, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — Query Reference
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗄️ Query Reference":
    st.markdown("""<div class="astro-header">
    <h1>🗄️ Query Reference</h1>
    <p>Template BigQuery SQL — pilih DOW & minggu, query otomatis ter-update</p></div>""",
    unsafe_allow_html=True)

    def dow_week_picker(prefix):
        dow_choice = st.selectbox(
            "Pilih Day of Week (start periode)", DAYS, index=1,
            key=f"{prefix}_dow"
        )
        valid_dates = get_valid_dates(dow_choice)
        today = datetime.date.today()
        past_dates = [d for d in valid_dates if d <= today]
        def_w1 = past_dates[-2] if len(past_dates) >= 2 else valid_dates[0]
        def_w2 = past_dates[-1] if len(past_dates) >= 1 else valid_dates[1]

        st.markdown(f"Pilih 2 minggu yang mau dibandingkan (hari **{dow_choice}**).")

        # Year + Month + Date picker for W1
        st.markdown("**Week 1**")
        c1, c2, c3 = st.columns([1,1,2])
        years = sorted(set(d.year for d in valid_dates))
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        yr1 = c1.selectbox("Tahun", years, index=years.index(def_w1.year), key=f"{prefix}_yr1")
        mo1 = c2.selectbox("Bulan", list(range(1,13)), index=def_w1.month-1,
                           format_func=lambda m: months[m-1], key=f"{prefix}_mo1")
        dates_w1 = [d for d in valid_dates if d.year==yr1 and d.month==mo1]
        if not dates_w1:
            dates_w1 = [d for d in valid_dates if d.year==yr1][:1] or [valid_dates[0]]
        def_idx1 = 0
        if def_w1 in dates_w1: def_idx1 = dates_w1.index(def_w1)
        w1 = c3.selectbox("Tanggal", dates_w1, index=def_idx1,
                          format_func=lambda d: d.strftime("%d %b %Y"), key=f"{prefix}_w1")

        # Year + Month + Date picker for W2
        st.markdown("**Week 2**")
        c4, c5, c6 = st.columns([1,1,2])
        yr2 = c4.selectbox("Tahun", years, index=years.index(def_w2.year), key=f"{prefix}_yr2")
        mo2 = c5.selectbox("Bulan", list(range(1,13)), index=def_w2.month-1,
                           format_func=lambda m: months[m-1], key=f"{prefix}_mo2")
        dates_w2 = [d for d in valid_dates if d.year==yr2 and d.month==mo2]
        if not dates_w2:
            dates_w2 = [d for d in valid_dates if d.year==yr2][:1] or [valid_dates[0]]
        def_idx2 = min(len(dates_w2)-1, 0)
        if def_w2 in dates_w2: def_idx2 = dates_w2.index(def_w2)
        w2 = c6.selectbox("Tanggal", dates_w2, index=def_idx2,
                          format_func=lambda d: d.strftime("%d %b %Y"), key=f"{prefix}_w2")

        w1e = w1 + datetime.timedelta(days=6)
        w2e = w2 + datetime.timedelta(days=6)
        st.markdown(f"**Week 1:** {w1.strftime('%d %b %Y')} → {w1e.strftime('%d %b %Y')} &nbsp;|&nbsp; "
                    f"**Week 2:** {w2.strftime('%d %b %Y')} → {w2e.strftime('%d %b %Y')}")

        tmpl = Q1_TEMPLATE if prefix=="q1" else Q2_TEMPLATE
        query = tmpl\
            .replace("{START_DATE}", str(w1))\
            .replace("{END_DATE}", str(w2e))\
            .replace("{DOW}", dow_choice.upper())
        return query

    tab1, tab2, tab3 = st.tabs(["Q1 — GP Bridge","Q2 — PI Analyzer","Q3 — Pricing Simulator"])

    with tab1:
        st.markdown('<div class="q-card"><span class="q-badge">Q1</span><b>GP Bridge</b> — Weekly comparison</div>', unsafe_allow_html=True)
        q1_filled = dow_week_picker("q1")
        st.code(q1_filled, language="sql")
        st.caption("💡 Klik ikon copy (📋) di pojok kanan atas code block untuk copy query ke clipboard.")

    with tab2:
        st.markdown('<div class="q-card"><span class="q-badge">Q2</span><b>PI Analyzer</b> — Weekly comparison</div>', unsafe_allow_html=True)
        q2_filled = dow_week_picker("q2")
        st.code(q2_filled, language="sql")
        st.caption("💡 Klik ikon copy (📋) di pojok kanan atas code block untuk copy query ke clipboard.")

    with tab3:
        st.markdown('<div class="q-card"><span class="q-badge">Q3</span><b>Pricing Simulator</b> — Flexible date range</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        today = datetime.date.today()

        # Start date picker
        st.markdown("**Start Date**")
        cs1, cs2, cs3 = st.columns([1,1,2])
        s_yr = cs1.selectbox("Tahun", [2024,2025,2026,2027], index=1, key="q3_s_yr")
        s_mo = cs2.selectbox("Bulan", list(range(1,13)), index=today.month-2 if today.month>1 else 0,
                             format_func=lambda m: months[m-1], key="q3_s_mo")
        import calendar
        s_days = list(range(1, calendar.monthrange(s_yr, s_mo)[1]+1))
        s_day = cs3.selectbox("Tanggal", s_days, index=0, key="q3_s_day")
        ds = datetime.date(s_yr, s_mo, s_day)

        # End date picker
        st.markdown("**End Date**")
        ce1, ce2, ce3 = st.columns([1,1,2])
        e_yr = ce1.selectbox("Tahun", [2024,2025,2026,2027], index=2, key="q3_e_yr")
        e_mo = ce2.selectbox("Bulan", list(range(1,13)), index=today.month-1,
                             format_func=lambda m: months[m-1], key="q3_e_mo")
        e_days = list(range(1, calendar.monthrange(e_yr, e_mo)[1]+1))
        e_day = ce3.selectbox("Tanggal", e_days, index=today.day-1, key="q3_e_day")
        de = datetime.date(e_yr, e_mo, e_day)

        st.markdown(f"**Periode:** {ds.strftime('%d %b %Y')} → {de.strftime('%d %b %Y')}")
        q3_filled = Q3_TEMPLATE.replace("{START_DATE}", str(ds)).replace("{END_DATE}", str(de))
        st.code(q3_filled, language="sql")
        st.caption("💡 Klik ikon copy (📋) di pojok kanan atas code block untuk copy query ke clipboard.")

    st.info("⚠️ Sesuaikan nama tabel dengan schema BigQuery Astro yang sebenarnya sebelum run.", icon="⚠️")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="text-align:center;color:#8fa5cc;font-size:0.78rem;margin-top:40px;'
    'padding-top:14px;border-top:1px solid #e0e9ff;">'
    '🚀 Astro Pricing Tools · Pricing Strategy Team</div>',
    unsafe_allow_html=True
)
