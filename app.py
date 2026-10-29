import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(
    page_title="AI Travel Itinerary Planner",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ Personalized Travel Itinerary Planner")
st.markdown("Plan your perfect AI-powered getaway with personalized day-wise schedules, dining spots, and budget breakdowns.")

st.sidebar.header("🔑 Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

st.sidebar.header("🌍 Trip Preferences")
destination = st.sidebar.text_input("Destination", placeholder="e.g., Goa, Manali, Paris")
duration = st.sidebar.slider("Duration (Days)", min_value=1, max_value=14, value=3)
budget = st.sidebar.selectbox("Budget Level", ["Budget-Friendly", "Moderate", "Luxury"])
travel_style = st.sidebar.multiselect(
    "Travel Style / Interests",
    ["Sightseeing", "Adventure & Trekking", "Food & Dining", "Relaxation & Spa", "Culture & History", "Nightlife"],
    default=["Sightseeing", "Food & Dining"]
)
companions = st.sidebar.selectbox("Traveling With", ["Solo", "Couple", "Friends", "Family"])

st.subheader("📸 Optional: Upload Destination / Inspiration Photo")
uploaded_file = st.file_uploader("Upload an image (hotel, landmark, ticket, or landscape)", type=["jpg", "jpeg", "png"])

image_preview = None
if uploaded_file:
    image_preview = Image.open(uploaded_file)
    st.image(image_preview, caption="Inspiration Image Uploaded", width=350)

if st.button("🚀 Generate My Itinerary", type="primary"):
    if not api_key:
        st.error("Please provide a valid Gemini API Key in the sidebar.")
    elif not destination:
        st.warning("Please enter a travel destination.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""
            You are an expert travel planner. Create a highly detailed, realistic, and personalized travel itinerary with the following details:
            - Destination: {destination}
            - Duration: {duration} Days
            - Budget: {budget}
            - Style/Interests: {', '.join(travel_style)}
            - Traveling With: {companions}

            Please provide the output structured clearly into:
            1. **Trip Overview & Highlights**
            2. **Day-wise Breakdown** (Morning, Afternoon, Evening, Recommended Dining with estimated costs)
            3. **Budget Estimation & Expenses Table** (Stay, Food, Activities, Local Transport)
            4. **Logistics & Safety Advisory** (Best local commute apps, weather tips, local customs)
            """

            with st.spinner("Synthesizing destination data and generating personalized itinerary..."):
                if image_preview:
                    response = model.generate_content([prompt, image_preview])
                else:
                    response = model.generate_content(prompt)

            st.success("Your itinerary is ready!")
            st.markdown(response.text)

            st.download_button(
                label="📥 Download Itinerary (TXT)",
                data=response.text,
                file_name=f"{destination.lower().replace(' ', '_')}_itinerary.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error generating itinerary: {str(e)}")
