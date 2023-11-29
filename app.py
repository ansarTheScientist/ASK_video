import os
import re
import openai
import gradio as gr
from pytube import YouTube

  # Replace with your OpenAI API key

chat_history = []  # Initialize an empty chat history list

def youtube_audio_downloader(link):
    if "youtube.com" not in link:
        return "Please enter a valid YouTube URL"
    yt = YouTube(link)
    audio_stream = yt.streams.filter(only_audio=True).first()
    download_result = audio_stream.download(output_path='audios')
    basename = os.path.basename(download_result)
    name, extension = os.path.splitext(basename)
    audio_file = re.sub('\s+', '-', name)
    complete_audio_path = f'{audio_file}.mp3'
    os.rename(download_result, complete_audio_path)
    return complete_audio_path

def transcribe_audio(audio_file, target_language):
    if not os.path.exists(audio_file):
        return f'The following file does not exist: {audio_file}'

    with open(audio_file, 'rb') as f:
        if target_language == 'korean':
            transcript = openai.Audio.translate('whisper-1', f, target_language='ko')
        else:
            transcript = openai.Audio.transcribe('whisper-1', f)

    name, extension = os.path.splitext(audio_file)
    transcript_filename = f'transcript-{name}.txt'
    with open(transcript_filename, 'w') as f:
        f.write(transcript['text'])
    return transcript_filename

def summarize_text(transcript_text, user_question, target_language, youtube_link):
    system_prompt = "Act as Expert one who can summarize any topic in user's language"
    prompt = f'''
    Text: {transcript_text}

    User Question: {user_question} YouTube Link: {youtube_link}'''

    if target_language == 'korean':
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-16k',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=4096,
            temperature=1
        )
    else:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-16k',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=4096,
            temperature=1
        )

    # Access the correct key in the response dictionary to get the generated text
    generated_text = response['choices'][0]['message']['content']

    # Append the YouTube link to the generated text
   # generated_text = f"{generated_text}\nYouTube Link: {youtube_link}"

    return generated_text

def youtube_summary_app(youtube_url, user_question, language_selection):
    user_question_with_link = f"{user_question} YouTube Link: {youtube_url}"
    downloaded_audio_file = youtube_audio_downloader(youtube_url)
    transcribed_file = transcribe_audio(downloaded_audio_file, target_language=language_selection)
    with open(transcribed_file, 'r') as file:
        transcribed_text = file.read()
    user_question_with_link = user_question_with_link.strip()  # Remove leading/trailing spaces
    response = summarize_text(transcribed_text, user_question_with_link, language_selection, youtube_url)
    chat_history.append((user_question_with_link, response))
    return transcribed_text,chat_history  # Return the entire chat history and the transcribed text

DEFAULT_YOUTUBE_URL = "https://www.youtube.com/watch?v=65c7o_EVqUs"
DEFAULT_QUESTION = "영상 제목이 뭔가요?"
youtube_url = gr.components.Textbox(label=f"YouTube URL (Default: {DEFAULT_YOUTUBE_URL})")
user_question = gr.components.Textbox(label=f"Your Question (Default: {DEFAULT_QUESTION})")
transcribed_text = gr.components.Textbox(label="Text in the Video")
iface = gr.Interface(
    fn=youtube_summary_app,
    inputs=[youtube_url, user_question, gr.Radio(['English', 'Korean'],value='English')],
    outputs=[transcribed_text,gr.Chatbot(chat_history=True, display_role=False,label="Question-Answer Chatbot")],
    title="Youtube Video Summarizer",
    description="Just Past link and ask Question.",
    theme='soft'
)
iface.launch()
