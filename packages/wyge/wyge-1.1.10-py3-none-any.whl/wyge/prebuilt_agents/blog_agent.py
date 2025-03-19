from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain import hub
from langchain.tools import StructuredTool


class BlogAgent:
    def __init__(self, api_key=None) -> None:
        self.llm = ChatOpenAI(api_key=api_key)

        # blog_img_tool = generate_images_and_add_to_blog()
        blog_img_tool = StructuredTool.from_function(
            name="generate_images_and_add_to_blog", 
            func=generate_images_and_add_to_blog,
            description="This tool helps to generate images and add them to blog. Blog should contain image prompts in <image> prompt </image> tag."
        )
        self.tools = [blog_img_tool]

        self.llm = ChatOpenAI(api_key=api_key)#.bind_tools(self.tools)

    def write_blog_text(self, topic, context):
        prompt2 = (
            f"You are an effective Blog writer. Output only blog, without any additional text. "
            f"Write a comprehensive blog post based on the following details:\n\n"
            f"Topic: {topic}\n"
            f"Summarized context about the topic: {context}\n\n"
            f"The blog should include an engaging introduction to topic, then detailed stections about how the context addresses the topic, "
            f"and a conclusion summarizing the key points. Structure the blog with clear headings, and write it in a conversational style.  "
            f"Output the blog in markdown format, including a title, introduction, body sections, and conclusion. Write in a conversational style to engage readers. "
        )
        # f"Remember to add image description in '<image/>' tag where image is required(total 1 image only, <image>image description</image>). "
        # f"Remember to use '<IMAGE/>' placeholder where image is required.(total 1 image only) "

        blog_text = self.llm.invoke(prompt2)
        return blog_text

    def generate_blog(self, topic, content):
        self.topic = topic
        blog_text = self.write_blog_text(topic, content)
        # blog_content = self.add_image_prompts(blog_text)
        # self.blog_content = blog_content
        # print(blog_content)
        # output = self.add_images(blog_content)
        # self.image_path = output[-1][-1][0]
        # doc_file = output[0][1]
        # return blog_text.replace("<-IMAGE->", "") , doc_file, self.image_path
        return blog_text
    
    # res = self.llm.invoke(prompt2)
    #     print(res.tool_calls[0])
    #     return generate_images_and_add_to_blog(**res.tool_calls[0]['args'])
    
def generate_images_and_add_to_blog(blog_content, save_temp=False):
    """This tool is used to generate images and add them to blog
    Args:
    blog_content: A complete blog with image prompts enclosed in <image> prompt </image> tag.
    Returns:
    A complete blog"""
    import tempfile
    import os
    import re
    import base64

    blog_content = str(blog_content)
    # print(f"****************\n{blog_content}\n**********")
    image_descriptions = re.findall(r'<image>(.*?)</image>', blog_content)
    
    md_file_path = 'blog_post.md'
    docx_file_path = 'blog_post.docx'
    if save_temp:
        temp_folder = tempfile.gettempdir()
        md_file_path = os.path.join(temp_folder, 'blog_post.md')
        docx_file_path = os.path.join(temp_folder, 'blog_post.docx')
    
    if os.path.exists(md_file_path):
        os.remove(md_file_path)
    if os.path.exists(docx_file_path):
        os.remove(docx_file_path)
    
    print(image_descriptions)
    images = []
    # base64_images = []
    for i, text in enumerate(image_descriptions):
        try:
            img_path = generate_image_openai(text,save_temp=save_temp, _i=i)
            print("image_generated")
            blog_content = blog_content.replace(f'<image>{text}</image>', f'![]({img_path})')
            images.append(img_path)
            
            # with open(img_path, 'rb') as img_file:
            #     base64_encoded = base64.b64encode(img_file.read()).decode('utf-8')
            #     base64_images.append(base64_encoded)
        except Exception as e:
            raise str(Exception(f"Image generation failed: {e}"))

    try:
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(blog_content)
        
        convert_md_to_docx(md_file_path, docx_file_path)
        # print(f"Markdown file saved at: {md_file_path}")
        # print(f"Document file saved at: {docx_file_path}")
    except Exception as error:
        print(error)

def generate_image_openai(text, openai_api_key=None, model_name="dall-e-2", resolution="512x512", quality='standard', n=1, save_temp = False, _i=1):
    import tempfile
    from openai import OpenAI
    import requests
    import os
    
    output_image = f'image_{_i}.png'
    if save_temp:
        temp_output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        output_image = temp_output_file.name

    api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
    print(api_key)
    client = OpenAI(api_key=api_key)

    try:
        response = client.images.generate(
            model=model_name,
            prompt=text,
            size=resolution,
            quality=quality,
            n=n
        )
        image_url = response.data[0].url
        # print(image_url)

        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            with open(output_image, 'wb') as file:
                file.write(image_response.content)
        else:
            raise str(Exception(f"Failed to download image with status code {image_response.status_code} and message: {image_response.text}"))

    except Exception as e:
        print(e)
        raise str(Exception(f"Image generation failed: {e}"))

    return output_image

def convert_md_to_docx(md_file_path, docx_file_path):
    import pypandoc

    output = pypandoc.convert_file(md_file_path, 'docx', outputfile=docx_file_path)
    assert output == "", "Conversion failed"