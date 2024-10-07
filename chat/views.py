import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import UploadedPDF
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyDeKAib3mKMfM8SXYvGwnlVpygboUbkxLw")
# GOOGLE_APPLICATION_CREDENTIALS=os.getenv("GOOGLE_APPLICATION_CREDENTIALS", 'credentials.json')

# Global variables
vector_store = None
chat_history = []

def clean_pages(pages):
    def clean_text(text):
        return text.encode('ascii', 'ignore').decode('ascii')
    
    for i, doc in enumerate(pages):
        pages[i].page_content = clean_text(doc.page_content)
    return pages

def get_llm_model(model_name='gemini'):
    if model_name == 'gemini':
        return GoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model='gemini-pro')
    elif model_name == 'mistral':
        return Ollama(model='mistral')
    elif model_name == 'llama3.2':
        return Ollama(model='llama3.2')
    else:
        return GoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model='gemini-pro')

def home(request):
    return render(request, 'chat/index.html')

@csrf_exempt
def update_model(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        model = data.get('model')
        request.session['current_model'] = model
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def upload_pdf(request):
    global vector_store, chat_history
    chat_history = []
    vector_store = None

    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        if not file.name.endswith('.pdf'):
            return HttpResponse('Invalid file type', status=400)

        # Save the uploaded file using the model
        uploaded_pdf = UploadedPDF(file=file)
        uploaded_pdf.save()  # Save the file to the database

        # Process the PDF
        file_path = uploaded_pdf.file.path  # Get the file path from the model
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()
        pages = clean_pages(pages)

        text_splits = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
        docs = text_splits.split_documents(pages)

        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = Chroma.from_documents(documents=docs, embedding=embeddings)

        # Summarize the PDF content
        google_model = GoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model='gemini-pro')
        combined_text = "\n".join([doc.page_content for doc in docs])
        
        summary_prompt = ChatPromptTemplate.from_messages([
            ("system", "Please provide a brief summary of the following document."),
            ("human", combined_text)
        ])

        summary_response = summary_prompt | google_model | StrOutputParser()
        chat_history.append(AIMessage(content=f"Summary of the PDF: {summary_response}"))

        return HttpResponse('PDF uploaded and processed successfully')
    return HttpResponse('No file uploaded', status=400)


@csrf_exempt
def chat(request):
    global vector_store, chat_history
    
    if request.method == 'POST':
        question = request.POST.get('question')
        model_name = request.session.get('current_model', 'gemini')

        if not vector_store:
            return HttpResponse('Please upload a PDF first', status=400)

        model = get_llm_model(model_name)
        out_parse = StrOutputParser()
        retriever = vector_store.as_retriever()

        instruction_to_system = """
        You are an AI assistant specialized in providing in-depth answers about a PDF document. 
        When a user asks a question, analyze the provided context and any previously answered 
        questions to deliver comprehensive, detailed responses. Aim to include relevant examples, 
        explanations, and connections to enhance the user's understanding. If you cannot find 
        the answer in the context, be transparent about it.
        """

        prompt = ChatPromptTemplate.from_messages([
            ("system", instruction_to_system),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
            ("system", "Relevant context: {context}")
        ])

        chain = (
            {"context": retriever, "question": RunnablePassthrough(), "chat_history": lambda _: chat_history}
            | prompt
            | model
            | out_parse
        )

        response = chain.invoke(question)
        chat_history.extend([HumanMessage(content=question), AIMessage(content=response)])

        return HttpResponse(response)
    return HttpResponse('Method not allowed', status=405)