import pandas as pd
import streamlit as st

import utils
from analyzer import TextAnalyzer

analyzer = TextAnalyzer()

with st.form("my_form"):
    st.write('Please enter a URL or a text')

    text_input = st.text_area('Please enter a URL or a text', 'https://www.enelx.com/it/it/privati/mobilita-elettrica')
    is_url = utils.is_url(text_input)
    meta_tags_only = st.checkbox('Extract only using meta tags')
    if meta_tags_only and is_url:
        text_input = utils.extract_tags_text(text_input)
        st.info(text_input)
        is_url = False
    submitted = st.form_submit_button("Submit")
    if submitted:
        response = analyzer.analyze(text_input, is_url)
        output = []
        known_entities = []
        for entity in response.entities():
            if entity.id not in known_entities:
                output.append({
                    "type": "thing",
                    "name": entity.id,
                    "Freebase Id": entity.freebase_id,
                    "Wikidata Id": entity.wikidata_id,
                    "wikipedia Link": entity.wikipedia_link
                })
                known_entities.append(entity.id)
        df = pd.DataFrame(output)
        st.dataframe(df)


