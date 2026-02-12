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

if papers:
    for paper in papers:
        title = paper.get('title', 'Untitled')
        url = paper.get('url', '#')
        venue = paper.get('venue', 'Journal/Conference')
        year = paper.get('year', '')
        
        # Format Authors
        author_list = [auth.get('name') for auth in paper.get('authors', [])]
        author_str = ", ".join(author_list)
        
        # Display
        st.markdown(f"### [{title}]({url})")
        st.markdown(f"👤 **{author_str}**")
        st.markdown(f"📅 {year} | 🏛️ *{venue}*")
        st.divider()
else:
    st.write("No publications found.")
