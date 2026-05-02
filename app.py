import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

st.set_page_config(
    page_title="ChurnIQ",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background: #03040A !important;
    font-family: 'Space Grotesk', sans-serif;
    color: #C8C8D8;
}

/* Animated starfield */
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background:
        radial-gradient(1px 1px at 20% 30%, rgba(139,92,246,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 80% 10%, rgba(99,102,241,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 50% 60%, rgba(167,139,250,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 10% 80%, rgba(99,102,241,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 70%, rgba(139,92,246,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 35% 90%, rgba(99,102,241,0.4) 0%, transparent 100%),
        radial-gradient(600px 600px at 10% 20%, rgba(99,102,241,0.04) 0%, transparent 60%),
        radial-gradient(800px 800px at 90% 80%, rgba(139,92,246,0.03) 0%, transparent 60%);
    pointer-events: none; z-index: 0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07080F 0%, #04050C 100%) !important;
    border-right: 1px solid rgba(139,92,246,0.15) !important;
    width: 310px !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }

.brand-block {
    padding: 28px 22px 22px;
    border-bottom: 1px solid rgba(139,92,246,0.12);
    margin-bottom: 8px;
    position: relative;
    overflow: hidden;
}
.brand-block::before {
    content: '';
    position: absolute; top: -40px; right: -40px;
    width: 160px; height: 160px; border-radius: 50%;
    background: radial-gradient(circle, rgba(139,92,246,0.15), transparent 70%);
}
.brand-logo {
    font-family: 'Space Mono', monospace;
    font-size: 26px; font-weight: 700;
    color: #fff; letter-spacing: -1px;
    margin-bottom: 4px;
}
.brand-logo span { color: #8B5CF6; }
.brand-tag {
    font-size: 10px; letter-spacing: 3px; text-transform: uppercase;
    color: rgba(139,92,246,0.7); font-weight: 500;
}
.brand-dot {
    display: inline-block; width: 6px; height: 6px;
    background: #10b981; border-radius: 50%;
    margin-right: 6px; animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.3); }
}

.nav-section {
    padding: 18px 22px 6px;
    font-size: 9px; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: rgba(139,92,246,0.5);
}

/* Form inputs */
.stSelectbox > div > div {
    background: rgba(139,92,246,0.05) !important;
    border: 1px solid rgba(139,92,246,0.18) !important;
    border-radius: 10px !important;
    color: #C8C8D8 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
}
.stSelectbox > div > div:focus-within {
    border-color: rgba(139,92,246,0.5) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.1) !important;
}
.stSlider [data-baseweb="slider"] { padding: 4px 0 !important; }
.stSlider [data-baseweb="thumb"] {
    background: linear-gradient(135deg, #8B5CF6, #6366f1) !important;
    border: 2px solid #fff !important;
    width: 18px !important; height: 18px !important;
    box-shadow: 0 0 12px rgba(139,92,246,0.5) !important;
}
.stSlider [data-baseweb="track-background"] { background: rgba(139,92,246,0.15) !important; }
.stSlider [data-baseweb="track-fill"] {
    background: linear-gradient(90deg, #8B5CF6, #6366f1) !important;
}
label, .stSlider label, .stSelectbox label, .stNumberInput label {
    color: #7070A0 !important;
    font-size: 11px !important; font-weight: 500 !important;
    letter-spacing: 0.5px !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stNumberInput > div > div > input {
    background: rgba(139,92,246,0.05) !important;
    border: 1px solid rgba(139,92,246,0.18) !important;
    border-radius: 10px !important; color: #C8C8D8 !important;
    font-family: 'Space Mono', monospace !important;
}

/* CTA Button */
.stButton > button {
    background: linear-gradient(135deg, #7C3AED 0%, #6366F1 50%, #4F46E5 100%) !important;
    color: #fff !important; border: none !important;
    border-radius: 14px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 14px !important; font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    padding: 16px 20px !important;
    width: 100% !important; margin-top: 20px !important;
    box-shadow: 0 0 30px rgba(139,92,246,0.35), inset 0 1px 0 rgba(255,255,255,0.15) !important;
    transition: all 0.3s ease !important;
    position: relative !important; overflow: hidden !important;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 0 50px rgba(139,92,246,0.55), inset 0 1px 0 rgba(255,255,255,0.2) !important;
}
.stButton > button:active { transform: translateY(0) scale(0.99) !important; }

/* Download button */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid rgba(139,92,246,0.3) !important;
    color: #A78BFA !important; border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important;
    font-size: 13px !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: rgba(139,92,246,0.1) !important;
    border-color: rgba(139,92,246,0.5) !important;
}

/* Main content */
.block-container { padding: 2.5rem 3rem !important; max-width: 1280px !important; }

/* Page hero */
.hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(139,92,246,0.1); border: 1px solid rgba(139,92,246,0.25);
    border-radius: 50px; padding: 5px 14px;
    font-size: 11px; font-weight: 600; color: #A78BFA;
    letter-spacing: 1.5px; text-transform: uppercase;
    margin-bottom: 16px;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 44px; font-weight: 700; line-height: 1.05;
    letter-spacing: -1.5px; color: #fff; margin-bottom: 12px;
}
.hero-title .accent {
    background: linear-gradient(135deg, #A78BFA 0%, #818CF8 50%, #6EE7B7 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub { font-size: 16px; color: #5A5A7A; line-height: 1.6; max-width: 520px; margin-bottom: 28px; }

/* Pill stats */
.pill-row { display: flex; gap: 10px; margin-bottom: 36px; flex-wrap: wrap; }
.pill {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 50px; padding: 7px 16px;
    font-size: 12px; display: flex; align-items: center; gap: 8px;
}
.pill-label { color: #3A3A5A; font-weight: 500; }
.pill-val { color: #A78BFA; font-weight: 700; font-family: 'Space Mono', monospace; font-size: 11px; }

/* Result cards */
.res-wrap {
    border-radius: 20px; padding: 0; margin-bottom: 28px;
    animation: reveal 0.6s cubic-bezier(0.22, 1, 0.36, 1) both;
    overflow: hidden;
}
@keyframes reveal {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
.res-inner {
    padding: 30px 32px; position: relative; overflow: hidden;
}
.res-inner.churn {
    background: linear-gradient(135deg, rgba(239,68,68,0.08) 0%, rgba(153,27,27,0.04) 100%);
    border: 1px solid rgba(239,68,68,0.25);
}
.res-inner.safe {
    background: linear-gradient(135deg, rgba(16,185,129,0.08) 0%, rgba(5,122,85,0.04) 100%);
    border: 1px solid rgba(16,185,129,0.25);
}
.res-inner::after {
    content: '';
    position: absolute; top: -80px; right: -80px;
    width: 300px; height: 300px; border-radius: 50%; opacity: 0.06;
}
.res-inner.churn::after { background: #ef4444; }
.res-inner.safe::after  { background: #10b981; }

.res-icon   { font-size: 40px; margin-bottom: 10px; }
.res-title  { font-size: 28px; font-weight: 700; letter-spacing: -0.5px; color: #fff; margin-bottom: 6px; }
.res-prob   { font-size: 14px; color: #5A5A7A; margin-bottom: 16px; }
.res-prob b { font-family: 'Space Mono', monospace; font-size: 20px; font-weight: 700; }
.c-red  { color: #F87171; }
.c-grn  { color: #34D399; }
.chip {
    display: inline-block; padding: 5px 14px; border-radius: 6px;
    font-size: 10px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase;
}
.chip-hi  { background: rgba(239,68,68,0.15);  color: #F87171; border: 1px solid rgba(239,68,68,0.3); }
.chip-md  { background: rgba(245,158,11,0.15); color: #FCD34D; border: 1px solid rgba(245,158,11,0.3); }
.chip-lo  { background: rgba(16,185,129,0.15); color: #34D399; border: 1px solid rgba(16,185,129,0.3); }

/* Metric row */
.mrow { display: flex; gap: 12px; margin-bottom: 28px; flex-wrap: wrap; }
.mcard {
    flex: 1; min-width: 88px;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px; padding: 16px 14px; text-align: center;
    transition: all 0.25s;
}
.mcard:hover {
    background: rgba(139,92,246,0.08);
    border-color: rgba(139,92,246,0.25);
    transform: translateY(-3px);
}
.mlabel { font-size: 9px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #3A3A5A; margin-bottom: 8px; }
.mval   { font-family: 'Space Mono', monospace; font-size: 19px; font-weight: 700; color: #E8E8F8; }
.msub   { font-size: 10px; color: #2A2A4A; margin-top: 4px; }

/* Analysis card */
.acard {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px; padding: 20px 22px;
    height: 100%;
}
.atitle {
    font-size: 9px; font-weight: 700; letter-spacing: 2.5px;
    text-transform: uppercase; color: #7C3AED; margin-bottom: 16px;
    padding-bottom: 10px; border-bottom: 1px solid rgba(139,92,246,0.1);
}
.fitem {
    display: flex; gap: 12px; align-items: flex-start;
    padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.04);
}
.fitem:last-child { border: none; padding-bottom: 0; }
.fdot {
    width: 7px; height: 7px; border-radius: 50%; margin-top: 6px; flex-shrink: 0;
}
.fdot-r { background: #ef4444; box-shadow: 0 0 8px rgba(239,68,68,0.6); }
.fdot-y { background: #f59e0b; box-shadow: 0 0 8px rgba(245,158,11,0.6); }
.fdot-g { background: #10b981; box-shadow: 0 0 8px rgba(16,185,129,0.6); }
.fname  { font-size: 13px; font-weight: 600; color: #E8E8F8; line-height: 1.3; }
.fdesc  { font-size: 11px; color: #3A3A5A; margin-top: 3px; }

/* Section divider */
.sec { font-size: 9px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase;
    color: #2A2A4A; margin: 28px 0 16px; display: flex; align-items: center; gap: 12px; }
.sec::after { content: ''; flex: 1; height: 1px; background: rgba(255,255,255,0.04); }

/* Welcome screen */
.welcome { text-align: center; padding: 60px 16px 40px; }
.welcome-icon { font-size: 56px; margin-bottom: 20px; }
.welcome-h { font-size: 24px; font-weight: 700; color: #E8E8F8; letter-spacing: -0.5px; margin-bottom: 10px; }
.welcome-p { font-size: 14px; color: #3A3A5A; line-height: 1.7; max-width: 360px; margin: 0 auto 40px; }
.fgrid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; text-align: left; }
.fbox {
    background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px; padding: 18px 16px; transition: all 0.2s;
}
.fbox:hover { background: rgba(139,92,246,0.07); border-color: rgba(139,92,246,0.2); transform: translateY(-3px); }
.fbox-icon { font-size: 22px; margin-bottom: 8px; }
.fbox-t { font-size: 13px; font-weight: 600; color: #E8E8F8; margin-bottom: 4px; }
.fbox-d { font-size: 11px; color: #3A3A5A; line-height: 1.6; }

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden !important; }
div[data-testid="stDecoration"] { display: none !important; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_artifacts():
    m  = pickle.load(open('model.pkl',       'rb'))
    s  = pickle.load(open('scaler.pkl',      'rb'))
    fc = pickle.load(open('feature_cols.pkl','rb'))
    return m, s, fc

model, scaler, feature_cols = load_artifacts()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand-block">
        <div class="brand-logo">Churn<span>IQ</span></div>
        <div class="brand-tag"><span class="brand-dot"></span>Live · v2.0</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="nav-section">Demographics</div>', unsafe_allow_html=True)
    gender     = st.selectbox("Gender",         ["Male","Female"])
    senior     = st.selectbox("Senior Citizen", ["No","Yes"])
    partner    = st.selectbox("Partner",        ["Yes","No"])
    dependents = st.selectbox("Dependents",     ["No","Yes"])

    st.markdown('<div class="nav-section">Services</div>', unsafe_allow_html=True)
    phone_service    = st.selectbox("Phone Service",     ["Yes","No"])
    multiple_lines   = st.selectbox("Multiple Lines",    ["No","Yes","No phone service"])
    internet_service = st.selectbox("Internet Service",  ["Fiber optic","DSL","No"])
    online_security  = st.selectbox("Online Security",   ["No","Yes","No internet service"])
    online_backup    = st.selectbox("Online Backup",     ["Yes","No","No internet service"])
    device_prot      = st.selectbox("Device Protection", ["No","Yes","No internet service"])
    tech_support     = st.selectbox("Tech Support",      ["No","Yes","No internet service"])
    streaming_tv     = st.selectbox("Streaming TV",      ["No","Yes","No internet service"])
    streaming_movies = st.selectbox("Streaming Movies",  ["No","Yes","No internet service"])

    st.markdown('<div class="nav-section">Account</div>', unsafe_allow_html=True)
    contract       = st.selectbox("Contract",       ["Month-to-month","One year","Two year"])
    paperless      = st.selectbox("Paperless Bill", ["Yes","No"])
    payment_method = st.selectbox("Payment",        ["Electronic check","Mailed check","Bank transfer (automatic)","Credit card (automatic)"])
    tenure          = st.slider("Tenure (months)", 0, 72, 12)
    monthly_charges = st.slider("Monthly Charges ($)", 18.0, 120.0, 65.0, 0.5)
    total_charges   = st.number_input("Total Charges ($)", 0.0, value=float(round(monthly_charges*tenure, 2)), step=10.0)

    st.markdown("<br>", unsafe_allow_html=True)
    go = st.button("⬡  Run Analysis", use_container_width=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def encode():
    services = [phone_service,online_security,online_backup,device_prot,tech_support,streaming_tv,streaming_movies]
    row = dict(
        gender=1 if gender=="Male" else 0, SeniorCitizen=1 if senior=="Yes" else 0,
        Partner=1 if partner=="Yes" else 0, Dependents=1 if dependents=="Yes" else 0,
        tenure=tenure, PhoneService=1 if phone_service=="Yes" else 0,
        MultipleLines={"No":0,"No phone service":1,"Yes":2}[multiple_lines],
        InternetService={"DSL":0,"Fiber optic":1,"No":2}[internet_service],
        OnlineSecurity={"No":0,"No internet service":1,"Yes":2}[online_security],
        OnlineBackup={"No":0,"No internet service":1,"Yes":2}[online_backup],
        DeviceProtection={"No":0,"No internet service":1,"Yes":2}[device_prot],
        TechSupport={"No":0,"No internet service":1,"Yes":2}[tech_support],
        StreamingTV={"No":0,"No internet service":1,"Yes":2}[streaming_tv],
        StreamingMovies={"No":0,"No internet service":1,"Yes":2}[streaming_movies],
        Contract={"Month-to-month":0,"One year":1,"Two year":2}[contract],
        PaperlessBilling=1 if paperless=="Yes" else 0,
        PaymentMethod={"Bank transfer (automatic)":0,"Credit card (automatic)":1,"Electronic check":2,"Mailed check":3}[payment_method],
        MonthlyCharges=monthly_charges, TotalCharges=total_charges,
        ChargesPerMonth=total_charges/(tenure+1),
        IsLongTermContract=1 if contract!="Month-to-month" else 0,
        NumServices=sum(1 for s in services if s=="Yes"),
    )
    return pd.DataFrame([row])[feature_cols]

def risks():
    r = []
    if contract=="Month-to-month":           r.append(("Month-to-month contract","3× higher churn than annual","r"))
    if tenure<12:                            r.append((f"New customer ({tenure} mo)","First-year churn rate ~47%","r"))
    if monthly_charges>65:                   r.append((f"High charges (${monthly_charges:.0f})","Above $65 risk threshold","y"))
    if internet_service=="Fiber optic":      r.append(("Fiber optic internet","High competition segment","y"))
    if online_security=="No":                r.append(("No online security","Unprotected customers churn more","y"))
    if tech_support=="No":                   r.append(("No tech support","Dissatisfaction driver","y"))
    if payment_method=="Electronic check":   r.append(("Electronic check","Highest-churn payment method","y"))
    return r

def tips():
    t = []
    if contract=="Month-to-month":           t.append(("Offer annual upgrade","15% discount to switch to 1-year plan"))
    if tenure<12:                            t.append(("Loyalty onboarding","Enrol in first-year rewards program"))
    if online_security=="No" or tech_support=="No": t.append(("Bundle security+support","Reduced rate package deal"))
    if monthly_charges>70:                   t.append(("Personalised plan review","Cost reduction consultation"))
    ns = sum(1 for s in [online_security,online_backup,device_prot,tech_support,streaming_tv,streaming_movies] if s=="Yes")
    if ns<3:                                 t.append(("Cross-sell services","Increase stickiness with bundles"))
    return t or [("Schedule check-in","Customer satisfied — maintain touchpoints")]

def gauge(prob):
    fig, ax = plt.subplots(figsize=(3, 3), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('none'); ax.set_facecolor('none')
    # Tick marks
    for a in np.linspace(0.15*np.pi, 0.85*np.pi, 9):
        ax.plot([a, a], [0.82, 0.92], color='#1A1A2E', linewidth=2, solid_capstyle='round')
    # Background track
    bg = np.linspace(0.15*np.pi, 0.85*np.pi, 300)
    ax.plot(bg, [1]*300, color='#12122A', linewidth=20, solid_capstyle='round')
    # Color fill
    col = '#EF4444' if prob>0.6 else ('#F59E0B' if prob>0.35 else '#10B981')
    end = 0.15*np.pi + prob*0.7*np.pi
    fill = np.linspace(0.15*np.pi, end, 300)
    if len(fill)>1:
        ax.plot(fill, [1]*len(fill), color=col, linewidth=20, solid_capstyle='round', alpha=0.9)
        ax.plot(fill, [1]*len(fill), color=col, linewidth=28, solid_capstyle='round', alpha=0.1)
    # Center
    ax.text(np.pi/2, 0.3, f"{prob*100:.0f}%", ha='center', va='center',
            fontsize=26, fontweight='bold', color='white',
            fontfamily='monospace', transform=ax.transData)
    ax.text(np.pi/2, 0.02, "risk score", ha='center', va='center',
            fontsize=8, color='#3A3A5A', transform=ax.transData)
    ax.text(0.15*np.pi, 1.28, "0", ha='center', color='#2A2A4A', fontsize=8)
    ax.text(0.85*np.pi, 1.28, "100", ha='center', color='#2A2A4A', fontsize=8)
    ax.set_ylim(0,1.5); ax.set_theta_zero_location('W'); ax.set_theta_direction(-1); ax.axis('off')
    plt.tight_layout(pad=0)
    return fig

def imp_chart():
    fi = pd.Series(model.feature_importances_, index=feature_cols).sort_values().tail(8)
    fig, ax = plt.subplots(figsize=(8, 3.5))
    fig.patch.set_facecolor('#07080F'); ax.set_facecolor('#07080F')
    med = fi.median()
    for i, (feat, val) in enumerate(fi.items()):
        hi = val >= med
        # Background bar
        ax.barh(i, val, color='#12122A', height=0.5, edgecolor='none')
        # Fill bar
        c = '#7C3AED' if hi else '#1E1E3A'
        ax.barh(i, val, color=c, height=0.5, edgecolor='none', alpha=0.9)
        if hi:
            ax.barh(i, val, color=c, height=0.5, edgecolor='none', alpha=0.12, linewidth=0)
        # Value label
        ax.text(val+0.002, i, f'{val:.3f}', va='center', color='#3A3A5A', fontsize=9, fontfamily='monospace')
        # Feature label
        ax.text(-0.002, i, feat, va='center', ha='right', color='#8080A0' if hi else '#3A3A5A',
                fontsize=10, fontweight='600' if hi else '400')
    ax.set_xlim(-0.08, fi.max()*1.25)
    ax.set_ylim(-0.8, len(fi)-0.2)
    ax.axis('off')
    plt.tight_layout(pad=0.3)
    return fig


# ── Page ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-badge">📡 &nbsp; AI-Powered Platform</div>
<div class="hero-title">Predict <span class="accent">Churn.</span><br>Retain More.</div>
<div class="hero-sub">Real-time telecom customer churn analysis with personalised retention intelligence.</div>
<div class="pill-row">
    <div class="pill"><span class="pill-label">Model</span><span class="pill-val">GRADIENT BOOST</span></div>
    <div class="pill"><span class="pill-label">Accuracy</span><span class="pill-val">76%</span></div>
    <div class="pill"><span class="pill-label">AUC-ROC</span><span class="pill-val">0.84</span></div>
    <div class="pill"><span class="pill-label">Dataset</span><span class="pill-val">7,043</span></div>
    <div class="pill"><span class="pill-label">Features</span><span class="pill-val">22</span></div>
</div>
""", unsafe_allow_html=True)


if not go:
    st.markdown("""
    <div class="welcome">
        <div class="welcome-icon">⬡</div>
        <div class="welcome-h">Ready to analyse</div>
        <div class="welcome-p">Configure the customer profile in the sidebar and hit <strong>Run Analysis</strong> to get an instant prediction with retention intelligence.</div>
        <div class="fgrid">
            <div class="fbox"><div class="fbox-icon">◎</div><div class="fbox-t">Churn Score</div><div class="fbox-d">Instant probability with risk classification</div></div>
            <div class="fbox"><div class="fbox-icon">⚑</div><div class="fbox-t">Risk Signals</div><div class="fbox-d">Pinpoints specific churn-driving factors</div></div>
            <div class="fbox"><div class="fbox-icon">↗</div><div class="fbox-t">Retention Actions</div><div class="fbox-d">Personalised recommendations to prevent loss</div></div>
            <div class="fbox"><div class="fbox-icon">⊞</div><div class="fbox-t">Feature Impact</div><div class="fbox-d">Which inputs moved the needle most</div></div>
            <div class="fbox"><div class="fbox-icon">◈</div><div class="fbox-t">Profile Summary</div><div class="fbox-d">Key customer metrics at a glance</div></div>
            <div class="fbox"><div class="fbox-icon">⬇</div><div class="fbox-t">Export Report</div><div class="fbox-d">Full prediction report as a download</div></div>
        </div>
    </div>""", unsafe_allow_html=True)

else:
    inp  = encode()
    prob = model.predict_proba(scaler.transform(inp))[0][1]
    pred = int(prob >= 0.5)
    risk = "HIGH RISK" if prob>=0.70 else ("MEDIUM RISK" if prob>=0.40 else "LOW RISK")
    rc   = "chip-hi"   if prob>=0.70 else ("chip-md"    if prob>=0.40 else "chip-lo")
    ns   = sum(1 for s in [online_security,online_backup,device_prot,tech_support,streaming_tv,streaming_movies] if s=="Yes")

    # Result
    if pred==1:
        st.markdown(f"""<div class="res-wrap"><div class="res-inner churn">
            <div class="res-icon">⚠</div>
            <div class="res-title">Customer will Churn</div>
            <div class="res-prob">Probability: <b class="c-red">{prob*100:.1f}%</b></div>
            <span class="chip {rc}">{risk}</span>
        </div></div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="res-wrap"><div class="res-inner safe">
            <div class="res-icon">✓</div>
            <div class="res-title">Customer will Stay</div>
            <div class="res-prob">Probability: <b class="c-grn">{prob*100:.1f}%</b></div>
            <span class="chip {rc}">{risk}</span>
        </div></div>""", unsafe_allow_html=True)

    # Profile
    st.markdown('<div class="sec">Customer Profile</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="mrow">
        <div class="mcard"><div class="mlabel">Tenure</div><div class="mval">{tenure}</div><div class="msub">months</div></div>
        <div class="mcard"><div class="mlabel">Monthly</div><div class="mval">${monthly_charges:.0f}</div><div class="msub">/ month</div></div>
        <div class="mcard"><div class="mlabel">Lifetime</div><div class="mval">${total_charges:,.0f}</div><div class="msub">total paid</div></div>
        <div class="mcard"><div class="mlabel">Contract</div><div class="mval" style="font-size:13px;">{contract.split()[0]}</div><div class="msub">type</div></div>
        <div class="mcard"><div class="mlabel">Internet</div><div class="mval" style="font-size:13px;">{internet_service.split()[0]}</div><div class="msub">service</div></div>
        <div class="mcard"><div class="mlabel">Services</div><div class="mval">{ns}<span style="font-size:12px;color:#2A2A4A;">/6</span></div><div class="msub">active</div></div>
    </div>""", unsafe_allow_html=True)

    # Analysis row
    st.markdown('<div class="sec">Churn Analysis</div>', unsafe_allow_html=True)
    g, r, t = st.columns([1, 1.3, 1.3])

    with g:
        st.pyplot(gauge(prob), use_container_width=True); plt.close()

    with r:
        rf  = risks()
        dm  = {"r":"fdot-r","y":"fdot-y","g":"fdot-g"}
        fh  = "".join([f'<div class="fitem"><div class="fdot {dm[c]}"></div><div><div class="fname">{n}</div><div class="fdesc">{d}</div></div></div>' for n,d,c in rf]) \
              or '<div class="fitem"><div class="fdot fdot-g"></div><div><div class="fname">No major risk factors</div></div></div>'
        st.markdown(f'<div class="acard"><div class="atitle">Risk Signals</div>{fh}</div>', unsafe_allow_html=True)

    with t:
        tp  = tips()
        th  = "".join([f'<div class="fitem"><div class="fdot fdot-g"></div><div><div class="fname">{n}</div><div class="fdesc">{d}</div></div></div>' for n,d in tp])
        st.markdown(f'<div class="acard"><div class="atitle">Retention Actions</div>{th}</div>', unsafe_allow_html=True)

    # Feature importance
    st.markdown('<div class="sec">Feature Importance</div>', unsafe_allow_html=True)
    st.pyplot(imp_chart(), use_container_width=True); plt.close()

    # Export
    st.markdown('<div class="sec">Export</div>', unsafe_allow_html=True)
    rf2 = risks(); tp2 = tips()
    rep = f"""CHURNIQ ANALYSIS REPORT
=======================
Result      : {'CHURN' if pred else 'RETAIN'}
Probability : {prob*100:.1f}%
Risk Level  : {risk}

CUSTOMER
--------
Tenure      : {tenure} months
Contract    : {contract}
Monthly     : ${monthly_charges:.2f}
Total       : ${total_charges:.2f}
Services    : {ns}/6

RISK FACTORS
------------
{chr(10).join(['• '+n+' — '+d for n,d,_ in rf2]) or '• None'}

ACTIONS
-------
{chr(10).join(['• '+n+' — '+d for n,d in tp2])}

------------------------------
ChurnIQ | Anurag Malik
CSE-AI 2Y | Chitkara University
"""
    st.download_button("⬇  Download Report", rep, "churniq.txt", "text/plain", use_container_width=True)