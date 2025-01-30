import os
import openai
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Konfigurasi OpenAI
openai.api_key = 'your-openai-api-key'  # Ganti dengan API key OpenAI Anda

# Scope untuk Blogger API
SCOPES = ['https://www.googleapis.com/auth/blogger']

# Fungsi untuk autentikasi Blogger
def authenticate_blogger():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Fungsi untuk menghasilkan konten menggunakan AI
def generate_content(prompt, max_tokens=300, temperature=0.7):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Anda bisa mengganti dengan model lain
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

# Fungsi untuk membuat postingan di Blogger
def create_post(blog_id, title, content):
    creds = authenticate_blogger()
    service = build('blogger', 'v3', credentials=creds)

    body = {
        "kind": "blogger#post",
        "blog": {
            "id": blog_id
        },
        "title": title,
        "content": content
    }

    try:
        posts = service.posts()
        request = posts.insert(blogId=blog_id, body=body)
        response = request.execute()
        print(f"Post created: {response['url']}")
    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    # Konfigurasi
    BLOG_ID = 'your-blog-id'  # Ganti dengan ID blog Anda
    PROMPT = "Buat artikel tentang manfaat teknologi AI dalam kehidupan sehari-hari."  # Prompt untuk AI

    # Generate konten menggunakan AI
    print("Generating content using AI...")
    generated_content = generate_content(PROMPT)
    print("\nGenerated Content:\n", generated_content)

    # Buat postingan di Blogger
    print("\nPosting to Blogger...")
    create_post(BLOG_ID, "Manfaat Teknologi AI dalam Kehidupan Sehari-hari", generated_content)