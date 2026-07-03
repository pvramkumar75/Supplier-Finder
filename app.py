import streamlit as st
from google import genai
from google.genai import types

# ====================== CONFIGURATION ======================
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)
# ===========================================================

st.set_page_config(page_title="Supplier Finder", layout="centered")
st.title("🔍 Supplier Finder App")
st.markdown("Find new suppliers with live web search powered by Gemini")

# ==================== INPUT FIELDS =========================
material = st.text_input(
    "Material Description *", 
    placeholder="e.g., Thermal Insulation Material for Cables"
)

specs = st.text_area(
    "Paste Specifications (Optional - helps get better matches)",
    placeholder="Enter detailed specifications here... (e.g., temperature range, thickness, material type, standards like IS/BS/IEC)",
    height=120
)

current_suppliers = st.text_input(
    "Current Suppliers (Optional - to avoid duplicates)",
    placeholder="e.g., ABC Insulation, XYZ Ltd"
)

quantity = st.text_input(
    "Tentative Quantity Required (Optional)",
    placeholder="e.g., 5000 meters per month or 80 MT per month"
)

country = st.selectbox(
    "Search Location",
    ["Anywhere", "India", "China", "USA", "Europe", "UK", "Germany", "Japan"]
)

supplier_name = st.text_input(
    "Check Specific Supplier / Manufacturer (Optional)",
    placeholder="Enter company name if you want full details of one supplier"
)
# ===========================================================

if st.button("🚀 Search Suppliers", type="primary"):
    if not material:
        st.error("Material Description is mandatory!")
    else:
        with st.spinner("Searching live on the web... Please wait"):
            
            # Build prompt dynamically - only include filled fields
            prompt = f"""You are an expert procurement researcher.

**Material:** {material}
"""

            if specs.strip():
                prompt += f"**Specifications:** {specs}\n"

            if quantity.strip():
                prompt += f"**Quantity:** {quantity}\n"

            if current_suppliers.strip():
                prompt += f"**Avoid these existing suppliers:** {current_suppliers}\n"

            prompt += f"""**Priority Location:** {country if country != "Anywhere" else "Worldwide"}

**Task:**
Find 8 to 10 **new and relevant suppliers** (do not repeat any avoided suppliers mentioned above).

For each supplier, give:
- Supplier / Company Name
- How well it matches the requirement (mention which specs or features match)
- Contact Number
- Email ID
- Website
- Address / Location

**Important Rules:**
- Give India-based suppliers first preference if available.
- If the supplier is not from India, clearly mention the country.
- Rank them from most relevant to least relevant.
- Be accurate and only show real suppliers from current web data.
- If specifications are not provided, find suppliers for the general material category.
"""

            if supplier_name.strip():
                prompt += f"\n\n**Also fetch complete details** for this specific supplier/manufacturer: **{supplier_name}** (give full address, contact numbers, email, website, and country of origin)."

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearch())]
                    )
                )
                st.markdown("### Search Results")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error occurred: {str(e)}")

st.caption("Powered by Gemini 2.5 Flash + Google Search | For internal procurement use")