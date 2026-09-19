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
        with st.spinner("Downloading audio, please wait..."):
            # Format-a universal audio-ku update panrom
            ydl_opts = {
                'format': 'bestaudio',
                'outtmpl': 'downloaded_audio.mp3',
                'restrictfilenames': True,
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                    }
                },
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    filename = 'downloaded_audio.mp3'

                    if os.path.exists(filename):
                        with open(filename, "rb") as f:
                            st.success("Download Ready!")
                            st.download_button(
                                label="Click Here to Save MP3",
                                data=f,
                                file_name="audio.mp3",
                                mime="audio/mp3"
                            )
                    else:
                        st.error("Error: File could not be processed.")

            except Exception as e:
                st.error(f"Error: {str(e)}")
                
