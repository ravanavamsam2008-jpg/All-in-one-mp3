import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="All in One MP3 Generator", page_icon="🎵")

st.markdown("<h1 style='text-align: center;'>🎵 ALL IN ONE MP3 GENERATOR 🎵</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>By Sada Uesan</p>", unsafe_allow_html=True)

url = st.text_input("Enter your YouTube / Insta URL...")

if st.button("Download MP3"):
    if not url:
        st.warning("Please enter a valid URL!")
    else:
        with st.spinner("Downloading, please wait...ing..."):
            # YouTube cookies/format mismatch avoid panra mukkhiya opts
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': 'downloaded_media.mp4',
                'noplaylist': True,
                'ignoreerrors': True,
                'no_warnings': True,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'ios', 'web']
                    }
                }
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    filename = 'downloaded_media.mp4'

                    if os.path.exists(filename):
                        with open(filename, "rb") as f:
                            st.success("Download Ready!")
                            st.download_button(
                                label="Click Here to Save File",
                                data=f,
                                file_name="downloaded_file.mp4",
                                mime="video/mp4"
                            )
                    else:
                        st.error("Error: File could not be processed. Try a different link.")

            except Exception as e:
                st.error(f"Error occurred: {str(e)}")
