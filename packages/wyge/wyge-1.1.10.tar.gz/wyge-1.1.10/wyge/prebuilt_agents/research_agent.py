from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain import hub
from langchain.tools import StructuredTool


class ResearchAgent:
    def __init__(self, api_key=None) -> None:
        # Create Tool objects with proper function references
        web_tool = StructuredTool.from_function(
            name="website_research",  # Changed from "Website Research" to "website_research"
            func=extract_relevant_sections_from_website,
            description=("Extract relevant information from a website based on keywords. "
            "Args: url (str): The URL of the website to analyze., "
            "keywords (list): A comprehesive list of keywords to search in the website based on the topic(more than 10). "
            "Returns: dict: A dictionary of relevant sections from the website."
            )
        )
        yt_tool = StructuredTool.from_function(
            name="youtube_transcript",  # Changed from "YouTube Transcript" to "youtube_transcript"
            func=youtube_transcript_loader,
            description="Extract transcript from a YouTube video"
        )
        video_to_audio_tool = StructuredTool.from_function(
            name="video_to_audio",  # Changed from "Video to Audio" to "video_to_audio"
            func=extract_audio_from_video,
            description="Extract audio from a video file"
        )
        audio_to_text_tool = StructuredTool.from_function(
            name="audio_to_text",  # Changed from "Audio to Text" to "audio_to_text"
            func=transcribe_audio,
            description="Transcribe audio to text"
        )
        self.tools = [web_tool, yt_tool, video_to_audio_tool, audio_to_text_tool]
        # self.functions = [convert_to_openai_function(t) for t in self.tools]



        # self.llm = ChatOpenAI(api_key=api_key).bind_tools(tools=self.tools)
        self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key).bind_tools(self.tools)

        


        # self.video_formats = ["mp4", "avi", "mkv", "mov", "flv", "wmv", "webm", "mpeg", "mpg", "3gp", "m4v", "mxf", "vob", "ogv"]
        # self.audio_formats = ["mp3", "wav", "aac", "flac", "ogg", "m4a"]

    def research_website(self, topic, url): 
        prompt1 = (
            f"Gather relavent information about topic from the website. "
            f"\nTopic: {topic} "
            f"\nWebsite: {url} "
        )
        # # context = self.llm.invoke(prompt1)
        # prompt = hub.pull("hwchase17/openai-functions-agent")
        # # Create an agent
        # agent = create_openai_tools_agent(self.llm, self.tools, prompt)

        # # Create an agent executor
        # agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

        # context = agent_executor.invoke({"input": prompt1})

        # return context['output']
        res = self.llm.invoke(prompt1)
        print(res.tool_calls[0])
        return extract_relevant_sections_from_website(**res.tool_calls[0]['args'])
    
    def extract_transcript_from_yt_video(self, url):
        prompt1 = f"Extract the text content from the youtube video. video url: {url}"
        # # context = self.llm.invoke(prompt1)
        # prompt = hub.pull("hwchase17/openai-functions-agent")
        # # Create an agent
        # agent = create_openai_tools_agent(self.llm, self.tools, prompt)

        # # Create an agent executor
        # agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

        # context = agent_executor.invoke({"input": prompt1})

        # return context['output']
        res = self.llm.invoke(prompt1)
        print(res.tool_calls[0])
        return youtube_transcript_loader(**res.tool_calls[0]['args'])

    
    def _video_to_text(self, video_path):
        audio_path = self.llm.invoke(f"Extract audio fromt the video. video path: {video_path}", return_tool_output=True)[0]
        print(audio_path)
        text = self.llm.invoke(f"Transcribe the audio into text. audio_path: {audio_path}", return_tool_output=True)[0]
        return text

    def _audio_to_text(self, audio_path):
        text = self.llm.invoke(f"Transcribe the audio into text. audio_path: {audio_path}", return_tool_output=True)[0]
        return text
    
    def extract_text_from_audio_or_video(self, file_path):
        file_format = 'Audio file' if file_path.endswith('mp3') else 'Video file'
        if file_format == 'Video file':
            text = self._video_to_text(file_path)
        elif file_format == 'Audio file':
            text = self._audio_to_text(file_path)
        return text
    

def extract_sections(url):
    import requests
    from bs4 import BeautifulSoup

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    sections = []
    for link in soup.find_all('a', href=True):
        sections.append({
            'text': link.get_text().strip(),
            'url': link['href']
        })
        
    return sections

def filter_relevant_sections(sections, keywords):
    relevant_sections = []
    for section in sections:
        if any(keyword.lower() in section['text'].lower() for keyword in keywords):
            relevant_sections.append(section)
    
    return relevant_sections

def filter_youtube_links(sections):
    youtube_sections = []
    for section in sections.copy():  # Use copy to avoid modifying during iteration
        if 'youtube' in section['url']:
            youtube_sections.append(section)
    return youtube_sections

def gather_info_from_sections(relevant_sections):
    import requests
    from bs4 import BeautifulSoup

    content = {}
    for section in relevant_sections:
        try:
            response = requests.get(section['url'])
            soup = BeautifulSoup(response.content, 'html.parser')
            clean_text = clean_scraped_text(soup.get_text())
            content[section['url']] = clean_text
        except Exception as e:
            # print(e)
            pass
    
    return content

def clean_scraped_text(text):
    import re

    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)

    patterns = [
        r'Home\s+About Us.*?\s+Contact Us',
        r'This website uses cookies.*?Privacy & Cookies Policy',  
        r'Copyright.*?Powered by.*',  
    ]

    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)

    text = re.sub(r'\|.*?\|', '', text)  
    text = text.strip()  

    return text

def youtube_transcript_loader(url):
    from youtube_transcript_api import YouTubeTranscriptApi
    try:
        video_id = url.split('/')[-1].split('=')[-1]
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])

        if transcript is None:
            raise ValueError('No English transcript found for video: {}'.format(video_id))

        list_t =  transcript.fetch()
    
        transcript_text = ""
        for transcript in list_t:
            transcript_text += transcript.text+ " "
        return transcript_text
    except Exception as e:
        return f"Error: {e}"
        # raise 
    
def gather_youtube_data(sections, keywords):

    youtube_sections = []
    for i, section in enumerate(sections):
        if 'youtube' in section['url']:
            youtube_sections.append(section)

    content = {}
    for section in youtube_sections:
        text = youtube_transcript_loader(section['url'])
        if text is not None:
            content[section['url']] = text

    relevant_content = {}
    for k, v in content.items():
        if any(keyword.lower() in v.lower() for keyword in keywords):
            relevant_content[k] = v

    return relevant_content

def extract_relevant_sections_from_website(url, keywords):
    try:
        sections = extract_sections(url)
        filtered_sections = filter_relevant_sections(sections, keywords)
        gathered_info = gather_info_from_sections(filtered_sections)
        youtube_info = gather_youtube_data(sections, keywords)
        total_info = gathered_info | youtube_info
        refined_info = {url: text for url, text in total_info.items() if len(text) > 200}  # Example threshold for content length
        return refined_info
    except Exception as e:
        # return {"error": str(e)}
        raise

def extract_audio_from_video(video_path):
    from moviepy.editor import VideoFileClip
    import tempfile
    print(video_path)
    with VideoFileClip(video_path) as video:
        audio = video.audio
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        audio.write_audiofile(temp_audio_file.name)
    return temp_audio_file.name

def transcribe_audio(audio_file_path):
    from openai import OpenAI
    client = OpenAI()
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )   
    return transcription.text