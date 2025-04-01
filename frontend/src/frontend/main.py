import streamlit as st
import os

# Sample video data (replace with your actual video files)
VIDEOS = [
    {
        "title": "Funny Cat Compilation",
        "tags": ["cats", "funny", "animals"],
        "file": "cat_video.mp4",
        "likes": 0
    },
    {
        "title": "Awesome Dance Moves",
        "tags": ["dance", "music", "hiphop"],
        "file": "dance_video.mp4",
        "likes": 0
    },
    {
        "title": "Cooking Tutorial",
        "tags": ["food", "cooking", "recipe"],
        "file": "cooking_video.mp4",
        "likes": 0
    },
]

def main():
    st.set_page_config(layout="wide")
    
    # Initialize session state
    if "current_video" not in st.session_state:
        st.session_state.current_video = 0
    if "likes" not in st.session_state:
        st.session_state.likes = {i: 0 for i in range(len(VIDEOS))}

    # Navigation functions
    def next_video():
        st.session_state.current_video = (st.session_state.current_video + 1) % len(VIDEOS)

    def prev_video():
        st.session_state.current_video = (st.session_state.current_video - 1) % len(VIDEOS)

    # Like function
    def like_video():
        video_index = st.session_state.current_video
        st.session_state.likes[video_index] += 1

    # Page layout
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col1:
        st.button("◀ Previous", on_click=prev_video)
    
    with col3:
        st.button("Next ▶", on_click=next_video)

    # Current video display
    with col2:
        current = VIDEOS[st.session_state.current_video]
        
        # Video player
        st.video(os.path.join("src/frontend/videos", current["file"]), autoplay=True, start_time=0, format="video/mp4", loop=True)
        
        # Video info
        st.subheader(current["title"])
        tags = " ".join([f"#{tag}" for tag in current["tags"]])
        st.caption(tags)
        
        # Like button
        st.button(
            f"❤️ {st.session_state.likes[st.session_state.current_video]}",
            on_click=like_video,
            key=f"like_{st.session_state.current_video}"
        )

if __name__ == "__main__":
    main()