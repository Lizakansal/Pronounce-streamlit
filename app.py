import streamlit as st
from utils.audio_utils import text_to_speech_autoplay, transcribe_audio
from utils.text_utils import calculate_similarity
from utils.free_speech import free_speech_accuracy
from utils.sentence_data import get_sentence_by_difficulty

st.set_page_config(
    page_title="Pro-Nounce | AI Pronunciation Trainer",
    page_icon="🎙️",
    layout="centered"
)

with open("assets/style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# SESSION STATE
if 'target_sentence' not in st.session_state:
    st.session_state.target_sentence = "The quick brown fox jumps over the lazy dog."

# HEADER
st.markdown("<h1 class='main-header'>🎙️ Pro-Nounce AI</h1>", unsafe_allow_html=True)
st.markdown("### Master your English Pronunciation")

# SIDEBAR
with st.sidebar:
    st.header("⚙️ Settings")

    mode = st.radio(
        "Practice Mode",
        ["Sentence Practice", "Free Speech"]
    )

    if mode == "Sentence Practice":
        difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])

        if st.button("🎲 New Sentence"):
            st.session_state.target_sentence = get_sentence_by_difficulty(difficulty)

# SENTENCE 
if mode == "Sentence Practice":
    col1, col2 = st.columns([1, 1])

    with col1:
        st.info("👇 **Read this sentence:**")
        st.markdown(f"## *\"{st.session_state.target_sentence}\"*")

    with col2:
        st.markdown("**👂 Listen to correct pronunciation:**")
        ref_audio = text_to_speech_autoplay(st.session_state.target_sentence)
        if ref_audio:
            st.audio(ref_audio, format="audio/mp3")

else:
    st.info("🎤 **Free Speech Mode**")
    st.write("Speak anything freely. Your pronunciation clarity will be evaluated.")

st.divider()

# RECORD 
st.markdown("### 🔴 Record Your Voice")
st.write("Click the mic icon below to start recording. Speak clearly!")

audio_value = st.audio_input("Record")

# ANALYSIS 
if audio_value:
    st.markdown("---")
    with st.spinner("🎧 Analyzing your pronunciation..."):

        user_text, error = transcribe_audio(audio_value.getvalue())

        if error:
            st.error(error)
        else:

# MODE
            if mode == "Sentence Practice":
                score, html_diff = calculate_similarity(
                    st.session_state.target_sentence,
                    user_text
                )
                feedback_html = f"""
                <div class='result-text'>{html_diff}</div>
                """
            else:
                score, feedback = free_speech_accuracy(user_text)
                feedback_html = f"""
                <div class='result-text'>
                    <span class='correct'>{feedback}</span>
                </div>
                """

# Scoring 
            st.markdown(f"""
            <div class='score-card'>
                <h2>Your Score</h2>
                <h1 style='color: {"#28a745" if score > 80 else "#ffc107" if score > 50 else "#dc3545"}; font-size: 4rem;'>
                    {int(score)}%
                </h1>
            </div>
            """, unsafe_allow_html=True)

            col_a, col_b = st.columns(2)

            with col_a:
                st.markdown("#### 🗣️ You Said:")
                st.info(user_text)

            with col_b:
                st.markdown("#### 🔍 Detailed Feedback:")
                st.caption("💚 Good | 🔴 Needs improvement")
                st.markdown(feedback_html, unsafe_allow_html=True)

#Effects
            if score == 100:
                st.balloons()
                st.success("🎉 Perfect Pronunciation! Amazing job!")
            elif score > 80:
                st.snow()
                st.success("🌟 Great job! Almost perfect.")
            else:
                st.warning("💪 Keep practicing! Speak slowly and clearly.")

st.markdown("---")

