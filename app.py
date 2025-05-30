import pandas as pd
import streamlit as st
from PIL import Image

# Load CSV with grape info
df = pd.read_csv("grape_varieties.csv")

# Titel and subtitle for the page
st.title("CIP 🍇 Grape Variety Encyclopedia")
st.header("Your Gateway To The World Of Wine")

# --- Search Bar ---
search_term = st.text_input("🔍 Search for grape name, flavor, or description:")

# # # Sidebar # # #
# Title
st.sidebar.header("Make Your Choice")

# Region filter
all_regions = sorted({region.strip() for regions in df['regions'] for region in regions.split(';')})
selected_region = st.sidebar.selectbox("Select Region", options=["All"] + all_regions)

# Grape color filter
colors = df['color'].dropna().unique().tolist()
selected_color = st.sidebar.selectbox("Select Grape Color", options=["All"] + colors)

# # # Apply filters # # # 
filtered_df = df.copy()

# Text search
if search_term:
    search_term_lower = search_term.lower()
    filtered_df = filtered_df[
        df['name'].str.lower().str.contains(search_term_lower) |
        df['description'].str.lower().str.contains(search_term_lower) |
        df['flavor_profile'].str.lower().str.contains(search_term_lower)
    ]

# Region filter
if selected_region != "All":
    filtered_df = filtered_df[filtered_df['regions'].str.contains(selected_region)]

# Grape color filter
if selected_color != "All":
    filtered_df = filtered_df[filtered_df['color'] == selected_color]

# # # some statistic add-ons for the sidebar # # #
# Title
st.sidebar.markdown("---")
st.sidebar.header("📊 Grapebase Stats")

# Total entries
total_count = len(df)
st.sidebar.markdown(f"**Total entries:** {total_count}")

# Grape color distribution
color_counts = df['color'].value_counts()
# Display the distribution of grape colors in the sidebar
for color, count in color_counts.items():
    st.sidebar.markdown(f"**{color}:** {count}")

# # # Display results # # # 

if not filtered_df.empty:
    for _, row in filtered_df.iterrows():
        st.subheader(row['name'])
        image = Image.open(row['image_path'])
        st.image(image, caption=row['name'], width=300)
        st.markdown(f"**Description:** {row['description']}")
        st.markdown(f"**Regions:** {row['regions']}")
        st.markdown(f"**Flavors:** {row['flavor_profile']}")
        st.markdown(f"**Pairings:** {row['food_pairings']}")
        st.markdown("---")
else:
    st.warning("No results found. Try adjusting your search or filters.")