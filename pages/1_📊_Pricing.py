import streamlit as st

st.set_page_config(page_title="Pricing - Financial Dashboard", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .pricing-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        height: 100%;
    }
    .pricing-header {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
        color: #2d3748;
    }
    .pricing-price {
        font-size: 36px;
        font-weight: bold;
        color: #3b82f6;
        margin: 15px 0;
    }
    .pricing-feature {
        margin: 8px 0;
        color: #4a5568;
    }
    .pricing-cta {
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("Pricing Plans")
st.write("Choose the plan that best fits your needs")

# Pricing Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="pricing-card">
        <div class="pricing-header">Basic</div>
        <div class="pricing-price">$29/mo</div>
        <div class="pricing-feature">✓ Real-time stock data</div>
        <div class="pricing-feature">✓ Basic technical indicators</div>
        <div class="pricing-feature">✓ Daily market updates</div>
        <div class="pricing-feature">✓ Email support</div>
        <div class="pricing-feature">✗ Advanced analytics</div>
        <div class="pricing-feature">✗ API access</div>
    </div>
    """, unsafe_allow_html=True)
    st.button("Get Started with Basic", key="basic")

with col2:
    st.markdown("""
    <div class="pricing-card">
        <div class="pricing-header">Pro</div>
        <div class="pricing-price">$79/mo</div>
        <div class="pricing-feature">✓ All Basic features</div>
        <div class="pricing-feature">✓ Advanced technical analysis</div>
        <div class="pricing-feature">✓ Portfolio optimization</div>
        <div class="pricing-feature">✓ Priority support</div>
        <div class="pricing-feature">✓ Custom alerts</div>
        <div class="pricing-feature">✗ API access</div>
    </div>
    """, unsafe_allow_html=True)
    st.button("Upgrade to Pro", key="pro", type="primary")

with col3:
    st.markdown("""
    <div class="pricing-card">
        <div class="pricing-header">Enterprise</div>
        <div class="pricing-price">$199/mo</div>
        <div class="pricing-feature">✓ All Pro features</div>
        <div class="pricing-feature">✓ API access</div>
        <div class="pricing-feature">✓ Custom integrations</div>
        <div class="pricing-feature">✓ Dedicated support</div>
        <div class="pricing-feature">✓ Team collaboration</div>
        <div class="pricing-feature">✓ Custom reporting</div>
    </div>
    """, unsafe_allow_html=True)
    st.button("Contact Sales", key="enterprise")

# FAQ Section
st.markdown("---")
st.header("Frequently Asked Questions")

faq_data = {
    "Can I change my plan later?": 
        "Yes, you can upgrade or downgrade your plan at any time. Changes will be reflected in your next billing cycle.",
    "Is there a free trial?":
        "Yes, we offer a 14-day free trial for all plans. No credit card required.",
    "What payment methods do you accept?":
        "We accept all major credit cards, PayPal, and bank transfers for enterprise customers.",
    "How secure is my data?":
        "We use industry-standard encryption and security practices to protect your data. All information is stored securely and never shared with third parties."
}

for question, answer in faq_data.items():
    with st.expander(question):
        st.write(answer) 