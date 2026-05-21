import streamlit as st
import math

# ─────────────────────────── Page config ────────────────────────────
st.set_page_config(
    page_title="Loan Calculator",
    page_icon="💰",
    layout="centered",
)

# ─────────────────────────── Custom CSS ─────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* ── gradient background ── */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        min-height: 100vh;
    }

    /* ── hero title ── */
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        color: #f0e6d3;
        letter-spacing: -0.5px;
        margin-bottom: 0;
        line-height: 1.1;
    }
    .hero-sub {
        color: #a89ec9;
        font-size: 1rem;
        font-weight: 300;
        margin-top: 4px;
        margin-bottom: 2rem;
    }

    /* ── glass card ── */
    .glass-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 20px;
        padding: 2rem 2.2rem;
        backdrop-filter: blur(12px);
        margin-bottom: 1.4rem;
    }

    /* ── result metric box ── */
    .metric-box {
        background: linear-gradient(135deg, #6c3de8 0%, #a855f7 100%);
        border-radius: 16px;
        padding: 1.4rem 1.8rem;
        margin-bottom: 1rem;
        color: white;
    }
    .metric-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        opacity: 0.8;
        margin-bottom: 4px;
    }
    .metric-value {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 700;
    }

    /* ── table styling ── */
    .schedule-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85rem;
        color: #e0d6f5;
    }
    .schedule-table th {
        background: rgba(108,61,232,0.4);
        padding: 10px 14px;
        text-align: right;
        font-weight: 500;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .schedule-table th:first-child { text-align: center; }
    .schedule-table td {
        padding: 9px 14px;
        text-align: right;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .schedule-table td:first-child { text-align: center; color: #a89ec9; }
    .schedule-table tr:last-child td { border-bottom: none; }
    .schedule-table tr:hover td { background: rgba(255,255,255,0.04); }

    /* ── divider ── */
    hr { border-color: rgba(255,255,255,0.1); }

    /* ── streamlit overrides ── */
    label, .stSlider label, .stNumberInput label, .stSelectbox label {
        color: #c9bef0 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6c3de8, #a855f7);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        font-size: 1rem;
        width: 100%;
        transition: opacity 0.2s;
    }
    .stButton>button:hover { opacity: 0.88; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────── Header ─────────────────────────────────
st.markdown('<p class="hero-title">💰 Loan Calculator</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Estimate monthly payments, total interest & full amortisation schedule</p>', unsafe_allow_html=True)

# ─────────────────────────── Inputs ─────────────────────────────────
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    loan_amount = st.number_input(
        "Loan Amount (₦)",
        min_value=1_000.0,
        max_value=1_000_000_000.0,
        value=5_000_000.0,
        step=50_000.0,
        format="%.2f",
    )
    loan_term_years = st.number_input(
        "Loan Term (Years)",
        min_value=1,
        max_value=30,
        value=5,
        step=1,
    )

with col2:
    annual_rate = st.number_input(
        "Annual Interest Rate (%)",
        min_value=0.1,
        max_value=50.0,
        value=15.0,
        step=0.1,
        format="%.2f",
    )
    loan_type = st.selectbox(
        "Loan Type",
        ["Reducing Balance (Amortising)", "Flat Rate (Simple Interest)"],
    )

st.markdown("</div>", unsafe_allow_html=True)

calculate = st.button("Calculate")

# ─────────────────────────── Calculation helpers ─────────────────────
def amortising(principal: float, annual_r: float, years: int):
    """Standard reducing-balance (amortising) loan."""
    n = years * 12
    r = annual_r / 100 / 12
    if r == 0:
        monthly = principal / n
    else:
        monthly = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)
    total_payment = monthly * n
    total_interest = total_payment - principal

    schedule = []
    balance = principal
    for i in range(1, n + 1):
        interest = balance * r
        principal_paid = monthly - interest
        balance -= principal_paid
        balance = max(balance, 0)
        schedule.append({
            "Month": i,
            "Payment": monthly,
            "Principal": principal_paid,
            "Interest": interest,
            "Balance": balance,
        })
    return monthly, total_payment, total_interest, schedule


def flat_rate(principal: float, annual_r: float, years: int):
    """Simple / flat-rate loan."""
    n = years * 12
    total_interest = principal * (annual_r / 100) * years
    total_payment = principal + total_interest
    monthly = total_payment / n
    monthly_interest = total_interest / n
    monthly_principal = principal / n

    schedule = []
    balance = principal
    for i in range(1, n + 1):
        balance -= monthly_principal
        balance = max(balance, 0)
        schedule.append({
            "Month": i,
            "Payment": monthly,
            "Principal": monthly_principal,
            "Interest": monthly_interest,
            "Balance": balance,
        })
    return monthly, total_payment, total_interest, schedule


def fmt(n: float) -> str:
    return f"₦{n:,.2f}"


# ─────────────────────────── Results ────────────────────────────────
if calculate:
    if "Flat" in loan_type:
        monthly, total_payment, total_interest, schedule = flat_rate(
            loan_amount, annual_rate, loan_term_years
        )
    else:
        monthly, total_payment, total_interest, schedule = amortising(
            loan_amount, annual_rate, loan_term_years
        )

    # ── Key metrics ──
    c1, c2, c3 = st.columns(3)
    metrics = [
        ("Monthly Payment", fmt(monthly)),
        ("Total Repayment", fmt(total_payment)),
        ("Total Interest", fmt(total_interest)),
    ]
    for col, (label, value) in zip([c1, c2, c3], metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Summary bar ──
    interest_pct = (total_interest / total_payment) * 100
    principal_pct = 100 - interest_pct
    st.markdown(
        f"""
        <div class="glass-card" style="margin-top:0.5rem">
            <div style="color:#a89ec9;font-size:0.8rem;margin-bottom:8px;text-transform:uppercase;letter-spacing:1px">
                Payment Breakdown
            </div>
            <div style="display:flex;height:12px;border-radius:6px;overflow:hidden;margin-bottom:8px">
                <div style="width:{principal_pct:.1f}%;background:linear-gradient(90deg,#6c3de8,#a855f7)"></div>
                <div style="width:{interest_pct:.1f}%;background:linear-gradient(90deg,#ec4899,#f97316)"></div>
            </div>
            <div style="display:flex;gap:1.5rem;font-size:0.82rem;color:#e0d6f5">
                <span>🟣 Principal &nbsp;<strong>{principal_pct:.1f}%</strong></span>
                <span>🟠 Interest &nbsp;<strong>{interest_pct:.1f}%</strong></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Amortisation schedule (collapsible) ──
    with st.expander("📋  View Full Amortisation Schedule"):
        rows = "".join(
            f"""<tr>
                <td>{s['Month']}</td>
                <td>{fmt(s['Payment'])}</td>
                <td>{fmt(s['Principal'])}</td>
                <td>{fmt(s['Interest'])}</td>
                <td>{fmt(s['Balance'])}</td>
            </tr>"""
            for s in schedule
        )
        st.markdown(
            f"""
            <table class="schedule-table">
                <thead>
                    <tr>
                        <th>Month</th>
                        <th>Payment</th>
                        <th>Principal</th>
                        <th>Interest</th>
                        <th>Balance</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
            """,
            unsafe_allow_html=True,
        )

# ─────────────────────────── Footer ─────────────────────────────────

