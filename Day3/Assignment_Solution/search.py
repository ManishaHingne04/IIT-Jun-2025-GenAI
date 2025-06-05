import streamlit as st



st.markdown("# GenAI")
st.markdown("## GenAI")
st.caption("caption is here")
st.subheader("Hello")
st.header("uu")
st.image("img.png")
st.multiselect("choose ",["gg","hh","gh"])
st.file_uploader("upload file")
st.balloons()

# # Initialize today's searches list in session state
if "today_searches" not in st.session_state:
    st.session_state.today_searches = []

search_bar = st.text_input("enter your querry")
st.session_state.today_searches.append(search_bar)
# st.write(search_bar)
#
st.sidebar.title("Todays Search")
# # st.sidebar.write(search_bar)
if st.session_state.today_searches:
    for search in st.session_state.today_searches:
        st.sidebar.write(search)
st.button("search")


