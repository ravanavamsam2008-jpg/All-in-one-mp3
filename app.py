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
        with st.spinner("Downloading, please wait..."):
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloaded_audio.mp4',
                'restrictfilenames': True,
                'noplaylist': True,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    filename = 'downloaded_audio.mp4'

                    if os.path.exists(filename):
                        with open(filename, "rb") as f:
                            st.success("Download Ready!")
                            st.download_button(
                                label="Click Here to Save File",
                                data=f,
                                file_name="media.mp4",
                                mime="video/mp4"
                            )
                    else:
                        st.error("Error: File could not be processed.")

            except Exception as e:
                st.error(f"Error: {str(e)}")
