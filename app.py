import streamlit as st
import requests
#업데이트 귀찮... 자동으로 레츠고
# 1. Define the function to fetch and sort papers
@st.cache_data(ttl=43200) # Update cache every 12 hours
def get_papers(author_id):
    url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers"
    
    # We ask for: Title, Year, Citation Count, URL, and Venue (Journal name)
    params = {
        "fields": "title,year,citationCount,url,venue",
        "limit": 100 
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json().get('data', [])
            
            # --- SORTING LOGIC ---
            # Sort by 'year' in descending order (Newest first). 
            # If a paper has no year (None), treat it as 0 so it goes to the bottom.
            sorted_data = sorted(data, key=lambda x: x.get('year') or 0, reverse=True)
            
            return sorted_data
        else:
            return []
    except Exception:
        return []

# 2. 교수님 Author ID
MY_AUTHOR_ID = "6506039"

st.title("Research Publications")
st.caption("Automatically updated via Semantic Scholar")

# 3. Fetch and Display
papers = get_papers(MY_AUTHOR_ID)

if papers:
    for paper in papers:
        title = paper.get('title', 'Untitled')
        year = paper.get('year', 'N/A')
        venue = paper.get('venue', 'Journal/Conference')
        citations = paper.get('citationCount', 0)
        link = paper.get('url', '#')
        
        # Display layout
        st.subheader(f"[{title}]({link})")
        st.markdown(f"**{year}** | *{venue}*")
        st.markdown(f"Cited by: {citations}")
        st.divider()
else:
    st.write("No publications found.")