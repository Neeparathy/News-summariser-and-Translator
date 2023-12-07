import streamlit as st
from googletrans import Translator
from collections import Counter
from string import punctuation
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stop_words
import base64
from PIL import Image

def tokenizer(s):
    tokens = []
    for word in s.split(' '):
        tokens.append(word.strip().lower())
    return tokens

def sent_tokenizer(s):
    sents = []
    for sent in s.split('.'):
        sents.append(sent.strip())
    return sents

def count_words(tokens):
    word_counts = {}
    for token in tokens:
        if token not in stop_words and token not in punctuation:
            if token not in word_counts.keys():
                word_counts[token] = 1
            else:
                word_counts[token] += 1
    return word_counts

def word_freq_distribution(word_counts):
    freq_dist = {}
    max_freq = max(word_counts.values())
    for word in word_counts.keys():
        freq_dist[word] = (word_counts[word]/max_freq)
    return freq_dist

def score_sentences(sents, freq_dist, max_len=40):
    sent_scores = {}
    for sent in sents:
        words = sent.split(' ')
        for word in words:
            if word.lower() in freq_dist.keys():
                if len(words) < max_len:
                    if sent not in sent_scores.keys():
                        sent_scores[sent] = freq_dist[word.lower()]
                    else:
                        sent_scores[sent] += freq_dist[word.lower()]
    return sent_scores

def summarize_paragraph(sent_scores, k):
    top_sents = Counter(sent_scores)
    summary = ''
    sentences_added = 0

    top = top_sents.most_common()

    for t in top:
        if sentences_added >= k:
            break
        summary += t[0].strip() + '. '
        sentences_added += 1

    return summary[:-1]

def translate_summary(summary, language):
    translator = Translator()
    translated_summary = translator.translate(summary, dest=language).text
    return translated_summary


def about_content():
    st.markdown("""
    <style>
    .about-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)
    st.subheader("About This Application")
    st.markdown("""
    <div class="about-box">
        This application performs news summarization and translation. It uses Streamlit for the interface and Google Translate for translations.

        SUMMARISATION:The article content you give will be summarized within seconds.
        TRANSLATION  : The summarized can be translated to the language you wish.

       Languages Available: Hindi, Tamil, Telugu, Bengali, Gujarati, Kannada, Malayalam, Marathi, Punjabi, Urdu.
    """, unsafe_allow_html=True)



#LOGO --- SHOULD BE FIRST ALWAYS
im = Image.open('C:\\Users\\npnee\\bg.png')
st.set_page_config(page_title="NEWS BYTES", page_icon=im)

# BACKGROUND IMAGE
def set_bg_hack(main_bg):
    main_bg_ext = "png"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_hack('C:\\Users\\npnee\\download.png')

# Streamlit app code

st.sidebar.header('Navigation')

# Add navigation options
page = st.sidebar.selectbox("Go to", ["Home","Summarize", "About"])

if page == "Home":
    st.markdown(
        """
        <style>
        .centered-title {
            text-align: left;
            margin-top: 300px;  # Adjust the margin-top value to move the title down
            font-size: 15px;
            font-family: 'Arial';
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<h1 style='text-align: left; margin-top: 0.5px;margin-left: 10px;  font-size: 150px;'>NEWS BYTES</h1>", unsafe_allow_html=True)
    
if page == "Summarize":
    st.title('NEWS BYTES')
    text_input = st.text_area("Enter your text here:", height=200)
    no_of_lines = st.number_input('Choose the no. of lines in the summary', min_value=1)
    languages = {
        'Hindi': 'hi',
        'Tamil': 'ta',
        'Telugu': 'te',
        'Bengali': 'bn',
        'Gujarati':'gu',
        'Kannada':'kn',
        'Malayalam':'ml',
        'Marathi':'mr',
        'Punjabi':'pa',
        'Urdu':'ur'
    }
    selected_language = st.selectbox('Select language for translation', list(languages.keys()))

    if text_input and no_of_lines and selected_language and st.button('Summarize and Translate'):
        text = text_input

        st.subheader('Original text:')
        st.write(text)

        tokens = tokenizer(text)
        sents = sent_tokenizer(text)
        word_counts = count_words(tokens)
        freq_dist = word_freq_distribution(word_counts)
        sent_scores = score_sentences(sents, freq_dist)
        summary = summarize_paragraph(sent_scores, no_of_lines)

        st.subheader('Summarised text:')
        st.write(summary)

        translated_summary = translate_summary(summary, languages[selected_language])
        
        st.subheader(f'Translated summary to {selected_language}:')
        st.write(translated_summary)

        st.info('An application made by Neeparathy N P , Mitun J S')

elif page == "About":
    about_content()