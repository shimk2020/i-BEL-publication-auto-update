#업데이트 귀찮... 자동으로 레츠고

import streamlit as st
import requests
import datetime

# 1. Fetch data (Same as before)
@st.cache_data(ttl=43200) 
def get_papers(author_id):
    url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers"
    params = {
        "fields": "title,year,publicationDate,venue,authors,url,citationCount",
        "limit": 100
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json().get('data', [])
            # Sort by Date (Newest first)
            sorted_data = sorted(
                data, 
                key=lambda x: x.get('publicationDate') or str(x.get('year')) or '0000-00-00', 
                reverse=True
            )
            return sorted_data
        else:
            return []
    except Exception:
        return []

# 2. 교수님 Author ID
MY_AUTHOR_ID = "6506039"
papers = get_papers(MY_AUTHOR_ID)

# --- NEW HEADER SECTION ---
# We use Markdown to create a clickable Title
google_scholar_link = "https://scholar.google.com/citations?hl=en&user=_d7FrPoAAAAJ&view_op=list_works&sortby=pubdate"

st.markdown(f"## Published International Journal Papers ([Google Scholar]({google_scholar_link}))")

# Get today's date for the "Last updated" text
today = datetime.date.today().strftime("%Y-%m-%d")
st.caption(f"Last updated: {today}")
# --------------------------

# 3. Get Data
papers = get_papers(MY_AUTHOR_ID)

# Header
google_scholar_link = "https://scholar.google.com/citations?hl=en&user=_d7FrPoAAAAJ&view_op=list_works&sortby=pubdate"
st.markdown(f"### Published International Journal Papers ([Google Scholar]({google_scholar_link}))")
st.caption(f"Last updated: {datetime.date.today().strftime('%Y-%m-%d')}")

if papers:
    for paper in papers:
        title = paper.get('title', 'Untitled')
        url = paper.get('url', '#')
        venue = paper.get('venue', 'Journal')
        year = paper.get('year', '')
        
        # Format Authors
        author_list = [auth.get('name') for auth in paper.get('authors', [])]
        author_str = ", ".join(author_list)
        
        # --- COMPACT HTML DESIGN ---
        # We use HTML to force tighter spacing and specific font sizes
        st.markdown(f"""
        <div style="margin-bottom: 15px;">
            <a href="{url}" target="_blank" style="font-size: 18px; font-weight: bold; color: #0068c9; text-decoration: none;">
                {title}
            </a>
            <br>
            <span style="font-size: 16px; color: #333;">{author_str}</span>
            <br>
            <span style="font-size: 14px; color: #666; font-style: italic;">
                {venue} • {year}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Optional: Add a very faint line between items (or remove for maximum compactness)
        st.markdown("""<hr style="margin: 5px 0; border: none; border-top: 1px solid #f0f0f0;">""", unsafe_allow_html=True)

else:
    st.write("No publications found.")
    

