from langchain_openai import ChatOpenAI

class LinkedInAgent:
    def __init__(self, api_key=None) -> None:
        # linkedin_tool = post_on_linkedin()
        
        # self.tools = [linkedin_tool]

        self.llm = ChatOpenAI(api_key=api_key)

    def generate_linkedin_post(self, content):
        prompt1 = (
            "Create a LinkedIn post based on the following topic and blog. The post should be professional, engaging, and suitable for a LinkedIn audience. "
            "It should introduce the topic, provide a brief summary, and include a call-to-action if relevant. The text should be concise yet informative."
            f"Blog content:\n{content}\n\n"
            
            "Expected Output: A well-structured LinkedIn post(around 250 words)."
            "Note: Do not post it on LinkedIn."
        )
        content = self.llm.invoke(prompt1)
        return content.content

    def post_content_on_linkedin(self, token, post_content, image_path=None):
        # prompt5 = (
        #     "Post the following content as linkedin post. "
        #     f"Post content: {post_content}"
        #     f"image path: {image_path}"
        #     f"linkedin token: {token}"
        # )
        # ack = self.llm.run(prompt5, return_tool_output=True)[0]
        ack = post_on_linkedin(token, post_content, image_path)
        return ack
    


def escape_text(text):
    chars = ["\\", "|", "{", "}", "@", "[", "]", "(", ")", "<", ">", "#", "*", "_", "~"]
    for char in chars:
        text = text.replace(char, "\\"+char)
    return text

def get_urn(token):
    import requests

    url = 'https://api.linkedin.com/v2/userinfo'

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        # print(user_info['sub'])
        return user_info['sub']
    else:
        print(f'Failed to fetch user info: {response.status_code}')
        # print(response.text)

def post_on_linkedin(token, text_content, image_path=None):
    """
    Posts an article on LinkedIn with or without an image.

    Args:
    token: LinkedIn OAuth token.
    title: LinkedIn post title.
    text_content: LinkedIn post content.
    image_path: file path of the image (optional).
    """
    import requests
    import json

    title = ""
    text_content = escape_text(text_content)
    owner = get_urn(token)

    # If an image is provided, initialize upload and post with image
    if image_path:
        if image_path.startswith('sandbox'):
            image_path = image_path.split(':')[1].strip()

        # Initialize the upload to get the upload URL and image URN
        init_url = "https://api.linkedin.com/rest/images?action=initializeUpload"
        headers = {
            "LinkedIn-Version": "202401",
            "X-RestLi-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        init_data = json.dumps({"initializeUploadRequest": {"owner": f'urn:li:person:{owner}'}})
        init_response = requests.post(init_url, headers=headers, data=init_data)

        if init_response.status_code != 200:
            raise str(Exception(f"Failed to initialize upload: {init_response.text}"))

        init_response_data = init_response.json()["value"]
        upload_url = init_response_data["uploadUrl"]
        image_urn = init_response_data["image"]

        # Upload the file
        with open(image_path, "rb") as f:
            upload_response = requests.post(upload_url, files={"file": f})
            if upload_response.status_code not in [200, 201]:
                raise str(Exception(f"Failed to upload file: {upload_response.text}"))

        # Create the post with the uploaded image URN as thumbnail
        post_data = json.dumps({
            "author": f'urn:li:person:{owner}',
            "commentary": text_content,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "content": {
                "media": {
                    "title": title,
                    "id": image_urn,
                }
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        })
    else:
        # Create a post without image
        post_data = json.dumps({
            "author": f'urn:li:person:{owner}',
            "commentary": text_content,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        })

    # Send the post request
    post_url = "https://api.linkedin.com/rest/posts"
    headers = {
        "LinkedIn-Version": "202401",
        "X-RestLi-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    post_response = requests.post(post_url, headers=headers, data=post_data)

    if post_response.status_code in [200, 201]:
        return "Linkedin article has been posted successfully!"
    else:
        print(post_response.text)
        # raise #str(Exception(f"Failed to post article: {post_response.text}"))