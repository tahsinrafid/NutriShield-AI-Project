import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import os

GEMINI_SYSTEM_INSTRUCTION = """
You are an expert Senior Clinical Dietician and Consumer Safety Auditor specializing in the Bangladeshi food market and dietary habits.
Your entire response and medical analysis must be optimized strictly for a Bangladeshi consumer context.
Your response must always be split into exactly two predictable markdown blocks using these literal tokens:
### [VISUAL_DASHBOARD]
### [TECHNICAL_DEEP_DIVE]

Rules for ### [VISUAL_DASHBOARD]:
- Output exactly three bullet points.
- Use high-contrast emojis and extremely simple, jargon-free words that a child or uneducated shopper can understand in 2 seconds.
- The first bullet must be ACTION and use one of these exact formats: 🔴 **ACTION**: STOP - DO NOT EAT, 🟡 **ACTION**: EAT VERY LITTLE, or 🟢 **ACTION**: EAT FREELY.
- The second bullet must be WHY and contain exactly one ultra-simple sentence explaining the core danger.
- Use simplified, direct conversational English common in Bangladesh.
- CRUCIAL LANGUAGE BOUNDARY: Every single sentence generated in the output must be written in standard, grammatically correct English.
- BAN ON BANGLA SCRIPT: You are strictly FORBIDDEN from generating any Bangla alphabet characters (e.g., do NOT write 'এই খাবারে অনেক ময়দা').
- BAN ON PHONETIC BANGLISH: You are strictly FORBIDDEN from writing conversational sentences using English letters to spell out Bangla words (e.g., do NOT write 'eta bhalo na' or 'beshi khaben na').
- ALLOWED LOCAL NOUNS: You must keep the sentences in English but use specific local nouns for food items, additives, and portion estimates.

Follow these strict examples precisely:
🟢 CORRECT (English structure + Localized metrics):
	"WHY: This food contains too much refined maida and salt, which can cause weight gain and impact heart health."
	"HOW MUCH: Max Serving: 35 grams (About half of a 70-gram packet or one-fourth of a bati)."

❌ INCORRECT (Completely Banned):
	"WHY: এই খাবারে অনেক ময়দা এবং লবণ আছে..."
	"WHY: Ei khabare onek maida ar lobon ache..."
- The third bullet must be HOW MUCH and use this exact pattern: Max Serving: X grams (About [local metric]).
- Completely ban generic Western units like biscuits or crackers unless the scanned item is literally a sweet biscuit.
- Map the serving weight directly to the declared food type using local household metrics.
- For noodles, soups, and curries, use fractions of a bati (bowl) or chamoch (tablespoons).
- For dry snacks like Chanachur, chips, muri, and jhalmuri, use muth (handfuls) or chamoch (tablespoons).
- For packaged snacks, relate it to fractions of standard local packet sizes such as one-fourth of a 10-Taka pack.
- For bakery or dessert items, use pice (pieces).

When evaluating the ingredients list from the image, audit for localized risks common in Bangladeshi processed foods, including:
- Cheap Palm Oil and Hydrogenated Vegetable Oils (Dalda) that can raise unsafe trans-fats.
- Refined flour (Maida) that can cause extreme glycemic spikes for diabetics.
- Excessive MSG / Monosodium Glutamate / E621.
- Chemical preservatives commonly used in local packaging, such as Sodium Benzoate and Potassium Sorbate.

Rules for ### [TECHNICAL_DEEP_DIVE]:
- Output the complete, unrestricted, high-fidelity clinical analysis without truncating or shortening anything.
- Include these exact markdown sections in the deep dive:
	### 📊 Nutritional Report Card
	### ⚖️ Consumption Boundaries
	### 🧪 Chemical Additives Explained
- CRUCIAL: Do not include any conversational introductions, summaries, greetings, or filler text at the start of this block.
- The very first character under the ### [TECHNICAL_DEEP_DIVE] token must begin directly with ### 📊 Nutritional Report Card.
- Make the technical section detailed, precise, and exhaustive.
- Never omit tables, lists, or long explanations if they are relevant.
"""

if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
elif "GOOGLE_API_KEY" in os.environ:
    api_key = os.environ["GOOGLE_API_KEY"]
else:
    api_key = None

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3.5-flash", system_instruction=GEMINI_SYSTEM_INSTRUCTION)
else:
    st.error("🔑 API Key not found! Please configure GOOGLE_API_KEY in your Streamlit Advanced Settings Secrets.")


if "demo_mode" not in st.session_state:
	st.session_state.demo_mode = False


st.set_page_config(
	page_title="NutriShield AI",
	page_icon="🥗",
	layout="wide",
	initial_sidebar_state="expanded",
)


st.markdown(
	"""
	<style>
		:root {
			--ns-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
		}

		html, body, [class*="css"] {
			font-family: "Inter", "Segoe UI", Arial, sans-serif;
		}

		.stApp {
			background: linear-gradient(180deg, #f7fafc 0%, #eef4f8 100%);
		}

		.stApp,
		[data-testid="stAppViewContainer"],
		[data-testid="stMainBlockContainer"] {
			background-color: #0F172A !important;
		}

		[data-testid="stAppViewContainer"] *,
		[data-testid="stMainBlockContainer"] *,
		.stApp main *,
		.stApp section *,
		.stApp article *,
		.stApp div:not([data-testid="stSidebar"]):not(.stButton) p,
		.stApp div:not([data-testid="stSidebar"]):not(.stButton) span,
		.stApp div:not([data-testid="stSidebar"]):not(.stButton) label,
		.stApp div:not([data-testid="stSidebar"]):not(.stButton) h1,
		.stApp div:not([data-testid="stSidebar"]):not(.stButton) h2,
		.stApp div:not([data-testid="stSidebar"]):not(.stButton) h3,
		.stApp div:not([data-testid="stSidebar"]):not(.stButton) h4 {
			color: #F8FAFC !important;
		}

		[data-testid="stAppViewContainer"] .stMarkdown,
		[data-testid="stMainBlockContainer"] .stMarkdown,
		[data-testid="stAppViewContainer"] .stMarkdown p,
		[data-testid="stMainBlockContainer"] .stMarkdown p,
		[data-testid="stAppViewContainer"] .stMarkdown span,
		[data-testid="stMainBlockContainer"] .stMarkdown span {
			color: #F8FAFC !important;
		}

		.block-container {
			padding-top: 2rem;
			padding-bottom: 2rem;
			max-width: 1200px;
		}

		[data-testid="stSidebar"] {
			padding-top: 0.5rem;
			padding-bottom: 0.5rem;
		}

		[data-testid="stSidebar"] .stSlider,
		[data-testid="stSidebar"] .stMultiSelect,
		[data-testid="stSidebar"] .stTextInput,
		[data-testid="stSidebar"] .stNumberInput {
			margin-bottom: 0.35rem;
		}

		[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMin"],
		[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMax"] {
			padding-top: 0.15rem;
			padding-bottom: 0.15rem;
		}

		.nutrishield-hero {
			background-color: #1E293B;
			color: #F8FAFC;
			border: 1px solid #334155;
			border-radius: 12px;
			padding: 24px;
			box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
			margin-bottom: 1.25rem;
		}

		.nutrishield-hero h1,
		.nutrishield-hero h2,
		.nutrishield-hero h3,
		.nutrishield-hero p,
		.nutrishield-card h1,
		.nutrishield-card h2,
		.nutrishield-card h3,
		.nutrishield-card p {
			color: #F8FAFC !important;
			font-family: 'Inter', sans-serif !important;
		}

		.nutrishield-hero h1 {
			margin: 0;
			font-size: 2.1rem;
			line-height: 1.15;
		}

		.nutrishield-hero p {
			margin: 0.75rem 0 0;
			font-size: 1rem;
			line-height: 1.6;
		}

		.nutrishield-card {
			background-color: #1E293B;
			color: #F8FAFC;
			border: 1px solid #334155;
			border-radius: 12px;
			padding: 24px;
			box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
			margin-top: 0.25rem;
		}

		.nutrishield-section-title {
			margin: 0 0 0.55rem;
			color: #F8FAFC;
			font-family: 'Inter', sans-serif;
		}

		.nutrishield-step-divider {
			display: flex;
			align-items: center;
			gap: 0.75rem;
			margin: 1rem 0;
			color: #F8FAFC;
			font-size: 0.9rem;
		}

		.nutrishield-step-divider::before,
		.nutrishield-step-divider::after {
			content: "";
			height: 1px;
			flex: 1;
			background: #334155;
		}

		.nutrishield-step-icon {
			width: 2rem;
			height: 2rem;
			display: inline-flex;
			align-items: center;
			justify-content: center;
			border-radius: 999px;
			background: #0f172a;
			color: #F8FAFC;
			font-size: 1rem;
		}

		.nutrishield-step-text {
			color: #F8FAFC !important;
			font-family: 'Inter', sans-serif;
		}
	</style>
	""",
	unsafe_allow_html=True,
)


with st.sidebar:
	st.title("👤 User Health Profile")
	st.caption("Personalize the analysis experience with relevant health context.")

	age = st.slider("Age", 1, 100, 25)
	weight_kg = st.number_input("Weight (kg)", min_value=1.0, value=65.0, step=0.5)
	chronic_conditions = st.multiselect(
		"Chronic conditions",
		[
			"Hypertension (High BP)",
			"Type 2 Diabetes",
			"Chronic Kidney Disease",
			"High Cholesterol",
		],
	)
	allergens = st.multiselect(
		"Allergens",
		["Gluten", "Lactose/Dairy", "Peanuts", "Soy", "MSG Sensitivity"],
	)
	custom_health_goals = st.text_input("Custom Health Goals")


health_profile_summary = (
	"User Health Profile:\n"
	f"- Age: {age}\n"
	f"- Weight: {weight_kg} kg\n"
	f"- Chronic Conditions: {', '.join(chronic_conditions) if chronic_conditions else 'None declared'}\n"
	f"- Allergies: {', '.join(allergens) if allergens else 'None declared'}\n"
	f"- Custom Health Goals: {custom_health_goals if custom_health_goals else 'None declared'}"
)


def split_gemini_response(text: str) -> tuple[str, str]:
	dashboard_part, token, technical_part = text.partition("### [TECHNICAL_DEEP_DIVE]")
	if token:
		dashboard_part = dashboard_part.replace("### [VISUAL_DASHBOARD]", "", 1).strip()
		return dashboard_part, technical_part.strip()

	return text.strip(), ""


st.markdown(
	"""
	<div class="nutrishield-hero">
		<h1>🥗 NutriShield AI</h1>
		<p>Scan food labels, understand ingredient risks, and track nutrition insights with a consumer safety lens.</p>
	</div>
	""",
	unsafe_allow_html=True,
)


tab_scan, tab_dashboard, tab_dictionary = st.tabs(
	["📸 Scan & Analysis", "📊 Health Dashboard", "📘 Additives Dictionary"]
)


with tab_scan:
	st.markdown('<div class="nutrishield-card">', unsafe_allow_html=True)
	st.markdown('<h3 class="nutrishield-section-title">Food Label Scan</h3>', unsafe_allow_html=True)
	if "use_sample" not in st.session_state:
		st.session_state.use_sample = False
	food_name = st.text_input(
		"📝 What food is this? (Optional but recommended)",
		placeholder="e.g., Instant Noodles, Chanachur, Potato Chips, Soft Drink",
	)
	uploaded_file = st.file_uploader(
		"Upload a food label photo",
		type=["jpg", "jpeg", "png"],
		help="Accepted file types: JPG, JPEG, PNG.",
	)
	if uploaded_file is not None:
		st.session_state.use_sample = False
	if st.session_state.use_sample:
		st.info("💡 **Sample Mode Active:** Ready to analyze default Instant Noodles label data.")
		if st.button("❌ Clear Sample Selection"):
			st.session_state.use_sample = False
			st.rerun()
	else:
		if st.button("💡 Try with a Sample Product (Instant Test Run)"):
			st.session_state.use_sample = True
			st.rerun()
	# st.markdown(
	# 	'<div class="nutrishield-step-divider"><span class="nutrishield-step-icon">⬇</span><span class="nutrishield-step-text">Review and Analyze</span></div>',
	# 	unsafe_allow_html=True,
	# )

	analyze_clicked = st.button(
		"🚀 Analyze Food Safety",
		use_container_width=True,
	)

	if analyze_clicked:
		if uploaded_file is None and not st.session_state.use_sample:
			st.warning("Please upload a food label photo before running analysis.")
		else:
			try:
				if st.session_state.use_sample:
					with open("sample_noodles.png", "rb") as sample_image_file:
						sample_image_bytes = sample_image_file.read()
					uploaded_image = Image.open(io.BytesIO(sample_image_bytes)).convert("RGB")
					declared_food_type = "Instant Noodles"
				else:
					uploaded_image_bytes = uploaded_file.getvalue()
					uploaded_image = Image.open(io.BytesIO(uploaded_image_bytes)).convert("RGB")
					declared_food_type = food_name.strip() if food_name.strip() else "Unspecified packaged food"
				regional_payload_summary = (
					health_profile_summary + f"\n- Declared Food Type: {declared_food_type}"
				)
				analysis_prompt = (
					"Analyze the text, ingredient declarations, and nutrition facts panel per 100g visible in the uploaded image. "
					"Strictly cross-reference them against the user's explicit Health Profile metrics.\n\n"
					f"{regional_payload_summary}\n\n"
					"Return your evaluation using the exact tokenized structure mandated by the system instruction. "
					"The visual dashboard must be extremely simple and the technical deep dive must be complete and untruncated."
				)

				with st.spinner("Analyzing food label and cross-referencing health profile..."):
					response = model.generate_content([analysis_prompt, uploaded_image])

				if "### [TECHNICAL_DEEP_DIVE]" in response.text:
					parts = response.text.split("### [TECHNICAL_DEEP_DIVE]")
					visual_part = parts[0].replace("### [VISUAL_DASHBOARD]", "").strip()
					deep_part = parts[1].strip()
				else:
					if "### [VISUAL_DASHBOARD]" in response.text:
						visual_part = response.text.replace("### [VISUAL_DASHBOARD]", "").strip()
						deep_part = ""
					else:
						visual_part = response.text
						deep_part = ""

				# 1. High-Contrast Global Alert Banner
				if any(marker in visual_part for marker in ["🔴", "STOP", "DO NOT EAT"]):
					st.error("🚨 CRITICAL HEALTH RISK DETECTED")
				elif any(marker in visual_part for marker in ["🟡", "CAUTION", "VERY LITTLE"]):
					st.warning("⚠️ CONSUMPTION WARNING")
				else:
					st.success("🟢 VERDICT: RISK ASSESSMENT CLEAR")

				# 2. Render Accessible Summary
				st.markdown(visual_part)

				# 3. Safe Technical Deep Dive Rendering (Prevents table parsing crashes)
				if deep_part:
					with st.expander("🔍 View Technical Clinical Breakdowns & Additives Science"):
						# Explicitly padding the markdown text with newlines forces Streamlit to parse matrix tables correctly
						sanitized_deep_part = "\n\n" + deep_part + "\n\n"
						st.markdown(sanitized_deep_part)
			except Exception as error:
				st.error(f"Analysis failed. Please check your API key or connection and try again. Details: {error}")
	st.markdown("</div>", unsafe_allow_html=True)


with tab_dashboard:
	st.success("Historical nutritional stats, exposure trends, and health insights will appear here once tracking is connected.")


with tab_dictionary:
	additive_query = st.text_input("Enter Additive Name or E-Number (e.g., E621, MSG, Aspartame):")
	additive_dictionary = {
		"E621": "Monosodium Glutamate. A flavor enhancer. Safe for most, but can trigger headaches or flushing in individuals with MSG Sensitivity.",
		"MSG": "Monosodium Glutamate. A flavor enhancer. Safe for most, but can trigger headaches or flushing in individuals with MSG Sensitivity.",
		"HIGH FRUCTOSE CORN SYRUP": "A highly refined sweetener. Highly dangerous for Diabetics as it spikes blood sugar instantly and contributes to fatty liver.",
		"SODIUM BENZOATE": "A common chemical preservative used in sodas and juices. Can stress kidney filtration over time if consumed in large quantities.",
		"E211": "A common chemical preservative used in sodas and juices. Can stress kidney filtration over time if consumed in large quantities.",
		"ASPARTAME": "An artificial intense sweetener used in 'Diet' products. Safe for weight management, but completely forbidden for people with PKU disease.",
		"POTASSIUM SORBATE": "An anti-mold preservative used in baked goods and cheeses. Generally recognized as safe in standard small quantities.",
	}

	lookup_key = additive_query.strip().upper()
	if lookup_key:
		matched_description = additive_dictionary.get(lookup_key)
		if matched_description:
			st.markdown("<div class='nutrishield-card'>", unsafe_allow_html=True)
			st.markdown(f"**{additive_query.strip()}**")
			st.markdown(matched_description)
			st.markdown("</div>", unsafe_allow_html=True)
		else:
			st.info("No direct match found. Try E621, MSG, High Fructose Corn Syrup, Sodium Benzoate, E211, Aspartame, or Potassium Sorbate.")