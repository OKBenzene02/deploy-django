# 🤖 TalkPDF with Django and LangChain

## 👀 Project Overview
This project is a PDF and document chatbot application built using Django, LangChain, and multiple LLMs (Large Language Models) both local and API-driven. It allows users to upload documents (PDFs, DOCX) and chat with them using advanced language models such as Google Gemini, Mistral, and Llama 3.2. The application is designed to be highly flexible and scalable, capable of processing multiple document types and providing intelligent answers based on document content.

## 🧠 Project Structure

- **`chatpdf/`**:
    - The main Django application folder containing settings, URL routing, and view logic.
    
    - **`__init__.py`**: Initializes the application.
    
    - **`settings.py`**: Django project settings. This file contains database configurations, installed apps (like `corsheaders` for CORS), and static/media file handling.
    
    - **`urls.py`**: Manages URL routing for your Django application. It maps URLs to corresponding views, like handling uploads or chat interactions.
    
    - **`views.py`**: Contains the core logic for handling HTTP requests. Key views include PDF upload, model switching, and chat endpoints. Also includes integrating LangChain's LLMs, chains, and document processing features. This file contains functions like `get_vectorstore()` and `get_conversation_chain()`.

- **`media/`**: This folder is where uploaded PDF or DOCX files are stored temporarily. Django manages file uploads here for processing.

- **`static/`**:
    - This directory stores all static assets like CSS and JavaScript files.
    
    - **`css/style.css`**: Custom styling for the frontend, adjusting the look and feel of your application.
    
    - **`js/script.js`**: JavaScript code that handles interactions and dynamic behavior on the frontend.

- **`templates/`**: Stores HTML files for the frontend.
    
    - **`index.html`**: Main page for uploading files and interacting with the chatbot. It renders the frontend interface.

- **`uploads/`**: This folder stores uploaded files during runtime (not included in version control). Files are temporarily saved here for document processing.

- **`manage.py`**: Django's command-line utility, used to run the development server, migrate databases, and manage other project-related tasks.

## 🧳Technology Stack
- **LangChain**: Provides the framework to work with LLMs for document processing and conversational tasks.
- **LangChain Community**: Utilized for integrating with custom community-driven modules.
- **Retrieval-Augmented Generation (RAG) Chains**: Enables retrieval-based question answering over documents.
- **Ollama**: Facilitates the use of local models like Mistral and Llama 3.2 for LLMs.
- **LLMs (Local and API)**: Google Gemini, Mistral, and Llama models for both local and API-based inference.
- **Django**: Backend framework used to manage the API, routing, and handling frontend requests.
- **Flask**: Initially used for API handling (now migrated to Django).
- **AWS Deployment**: AWS services are leveraged for hosting and deploying the application.
- **Python Libraries**: `PyPDFLoader`, `ChromaDB`, `GoogleGenerativeEmbeddings` for document processing and vectorization. `GoogleGenerativeEmbeddings` requires GCP credentials.json file.

## ⚒ Key Code Components
- **`views.py`**: Handles the main functionality, such as file upload, processing PDFs and DOCX files, and serving chat responses.
Also includes integrations for the LangChain models and chains with Django views, allowing for seamless chat integration with document content.
- **`get_llm_model()`**: Function dynamically selects which Large Language Model (LLM) to use based on the model name passed as a parameter.
- **`upload_pdf()`**: Manages the upload of pdf files and creation of a vector store using `GoogleGenerativeEmbeddings` and `ChromaDB` for efficient document retrieval.
- **`chat()`**: Creates a conversation chain using LangChain's Conversational Retrieval Chain, which manages memory and interaction with the uploaded documents.
- **`corsheaders`**: Configured in Django to allow cross-origin requests (CORS) for flexibility in API access.
- **`urls.py`**: Handles routing to various endpoints like file uploads, model switching, and chat interactions.

## 📈📉📈📉 Running the Project

### 🔐 Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/OKBenzene02/talkpdf-django.git
   ```
2. Navigate to the project directory:
   ```bash
   cd talkpdf-django
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows use `venv\Scripts\activate`
   ```
4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Allow CORS (already set up in Django):
    ```bash 
    pip install django-cors-headers
    ```
   - Ensure `corsheaders` is added to `INSTALLED_APPS`.
   - Set `CORS_ALLOW_ALL_ORIGINS = True` in your `settings.py` file.
6. Run the Django development server:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

### 🔓🛜 Deploying on AWS
1. Set up an EC2 instance and SSH into it.
2. Install Python and dependencies on the EC2 instance.
3. Set up the project as described in the "Locally" section.
4. Use the following command to run the server on AWS:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
5. Ensure the appropriate security groups are set in AWS to allow traffic to port 8000.

## 💡References
- [LangChain Tutorials Youtube](https://www.youtube.com/playlist?list=PL0iK4i3eaebZDU1YvFil0sUbcuU8Dg-vH)
- [LangChain Documentation](https://langchain.readthedocs.io)
- [Ollama](https://ollama.com/)
- [Hugging Face Embeddings](https://huggingface.co/docs/transformers/index)
- [Google Gemini Model](https://cloud.google.com/genai)
- [Django Documentation](https://docs.djangoproject.com/en/stable/)
- [AWS Deployment Django App](https://youtu.be/uiPSnrE6uWE?si=7SLjRWfPravo5gIa)
- [AWS Deployment Flask App](https://youtu.be/ct1GbTvgVNM?si=oUO_kNKTNBmO_oWv)

## 🥹 Open for Issues
If you encounter any issues or have questions about the project, feel free to open an issue or contribute by submitting a pull request.
