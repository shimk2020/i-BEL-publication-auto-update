# 업데이트 귀찮... 자동으로 레츠고

import streamlit as st
import requests
import datetime

# 1. Fetch data
@st.cache_data(ttl=43200) 
def get_papers(author_id):
    url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers"
    
    # Request 'externalIds' to get the DOI
    params = {
        "fields": "title,year,publicationDate,venue,authors,url,citationCount,externalIds",
        "limit": 100
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json().get('data', [])
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

# --- HEADER SECTION ---
google_scholar_link = "https://scholar.google.com/citations?hl=en&user=_d7FrPoAAAAJ&view_op=list_works&sortby=pubdate"
today_date = datetime.date.today().strftime('%Y-%m-%d')

st.markdown(f"""
<div style="font-size: 40px; font-weight: bold; margin-bottom: 10px; line-height: 1.4;">
    Published International Journal Papers
    <br>
    <span style="font-size: 40px; font-weight: normal;">
        (<a href="{google_scholar_link}" target="_blank" style="text-decoration: none; color: #0068c9;">Google Scholar</a>)
    </span>
</div>
""", unsafe_allow_html=True)

st.caption(f"Last updated: {today_date}")
# --------------------------

if papers:
    for paper in papers:
        title = paper.get('title', 'Untitled')
        venue = paper.get('venue', 'Journal')
        year = paper.get('year', '')
        
        # --- LINK & DOI LOGIC ---
        external_ids = paper.get('externalIds', {})
        doi = external_ids.get('DOI')
        
        if doi:
            # Main title links to DOI
            main_link = f"https://doi.org/{doi}"
            # Create a clickable DOI text for the bottom line
            doi_html = f'• <a href="https://doi.org/{doi}" target="_blank" style="color: #666; text-decoration: none;">DOI: {doi}</a>'
        else:
            main_link = paper.get('url', '#')
            doi_html = ""

        # Format Authors
        author_list = [auth.get('name') for auth in paper.get('authors', [])]
        author_str = ", ".join(author_list)
        
        # --- HTML DESIGN ---
        st.markdown(f"""
        <div style="margin-bottom: 15px;">
            <a href="{main_link}" target="_blank" style="font-size: 18px; font-weight: bold; color: #0068c9; text-decoration: none;">
                {title}
            </a>
            <br>
            <span style="font-size: 16px; color: #333;">{author_str}</span>
            <br>
            <span style="font-size: 14px; color: #666; font-style: italic;">
                {venue} • {year} {doi_html}
            </span>
        </div>
        <hr style="margin: 5px 0; border: none; border-top: 1px solid #f0f0f0;">
        """, unsafe_allow_html=True)

else:
    st.write("No publications found.")

