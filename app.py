#업데이트 귀찮... 자동으로 레츠고

import streamlit as st
import requests

# 1. Fetch data from Semantic Scholar
@st.cache_data(ttl=43200) # Cache for 12 hours
def get_papers(author_id):
    url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers"
    
    # ASK FOR SPECIFIC FIELDS: title, date, venue, URL, and AUTHORS
    params = {
        "fields": "title,year,publicationDate,venue,authors,url,citationCount",
        "limit": 100
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json().get('data', [])
            
            # --- SORTING LOGIC ---
            # Sort by specific 'publicationDate' (YYYY-MM-DD). 
            # If date is missing, use 'year'. If both missing, use '0000'.
            # reverse=True means Newest First.
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

# 2. Author ID
MY_AUTHOR_ID = "6506039"

st.title("Research Publications")
st.caption("Automatically updated via Semantic Scholar")

# 3. Get Data
papers = get_papers(MY_AUTHOR_ID)

if papers:
    for paper in papers:
        # A. Extract Info
        title = paper.get('title', 'Untitled')
        url = paper.get('url', '#')
        venue = paper.get('venue', 'Journal/Conference')
        year = paper.get('year', '')
        
        # B. Format Authors (List -> String)
        # Example: "Gahyun Baek, J. Smith, A. Doe"
        author_list = [auth.get('name') for auth in paper.get('authors', [])]
        author_str = ", ".join(author_list)
        
        # C. Display nicely
        st.markdown(f"### [{title}]({url})")
        st.markdown(f"👤 **{author_str}**")
        st.markdown(f"📅 {year} | 🏛️ *{venue}*")
        st.divider()
else:
    st.write("No publications found.")
