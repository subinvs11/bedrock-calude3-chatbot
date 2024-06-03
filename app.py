import uuid
import bedrock
import utility
import streamlit as st


USER_ICON = "images/user-icon.png"
AI_ICON = "images/ai-icon.png"

if "user_id" in st.session_state:
    user_id = st.session_state["user_id"]
else:
    user_id = str(uuid.uuid4())
    st.session_state["user_id"] = user_id

if "llm_chain" not in st.session_state:
    st.session_state["llm_app"] = bedrock
    st.session_state["llm_chain"] = bedrock.bedrock_chain()

if "questions" not in st.session_state:
    st.session_state.questions = []
    input_label = "Enter the youtube url to summarize"
else:
    input_label = "Now you can ask questions"

if "answers" not in st.session_state:
    st.session_state.answers = []

if "input" not in st.session_state:
    st.session_state.input = ""


def write_top_bar():
    col1, col2, col3 = st.columns([2, 10, 3])
    with col2:
        header = "Amazon Bedrock Chatbot"
        st.write(f"<h3 class='main-header'>{header}</h3>", unsafe_allow_html=True)
        description = """
        This is an AI ChatBot application.
        You can start chat by entering a youtube url which has transcript.
        The Bot will provide a summary of the transcript first.
        Then you can ask further questions.
        <br>
        Note: If you want to enter a new youtube url, click on the <b>Clear Chat</b> button and start a fresh chat.
        """
        st.write(f"<p class=''>{description}</p>", unsafe_allow_html=True)
    with col3:
        clear = st.button("Clear Chat")

    return clear


clear = write_top_bar()

if clear:
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.input = ""
    input_label = "Enter the youtube url to summarize"
    bedrock.clear_memory(st.session_state["llm_chain"])


def handle_input():
    input = st.session_state.input
    llm_chain = st.session_state["llm_chain"]
    chain = st.session_state["llm_app"]

    question = input

    if len(st.session_state.questions)==0:
        # Get video id from youtube url eg: https://www.youtube.com/watch?v=kNrvc0hkPuE
        video_id = utility.get_video_id_from_url(input)

        # Get transcript from youtube video
        transcript = utility.get_transcript(video_id)

        # Generate prompt from transcript
        input = utility.generate_prompt_from_transcript(transcript)
        
    result = chain.run_chain(llm_chain, input)

    question_with_id = {
        "question": question,
        "id": len(st.session_state.questions)
    }
    st.session_state.questions.append(question_with_id)

    st.session_state.answers.append(
        {"answer": result, "id": len(st.session_state.questions)}
    )
    st.session_state.input = ""


def write_user_message(md):
    col1, col2 = st.columns([1, 12])

    with col1:
        st.image(USER_ICON, use_column_width="always")
    with col2:
        st.warning(md["question"])


def render_answer(answer):
    col1, col2 = st.columns([1, 12])
    with col1:
        st.image(AI_ICON, use_column_width="always")
    with col2:
        st.info(answer["response"])


def write_chat_message(md):
    chat = st.container()
    with chat:
        render_answer(md["answer"])


with st.container():
    for q, a in zip(st.session_state.questions, st.session_state.answers):
        write_user_message(q)
        write_chat_message(a)


st.markdown("---")
input = st.text_input(
    input_label, key="input", on_change=handle_input
)