from django.shortcuts import render

# Create your views here.

# from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Question
from .serializers import UserSerializer, QuestionSerializer
from django.http import JsonResponse
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.llms.gpt4all import GPT4All

import os

# from . import funcoes as fn



@api_view(['GET'])
def get_users(request):

    if request.method == 'GET':

        users = User.objects.all()                          # Get all objects in User's database (It returns a queryset)

        serializer = UserSerializer(users, many=True)       # Serialize the object data into json (Has a 'many' parameter cause it's a queryset)

        return Response(serializer.data)                    # Return the serialized data
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ask_question(request):
    if request.method == 'POST':
        
        serializer = QuestionSerializer(data=request.data)
        
        if serializer.is_valid():
            
            topic = serializer.validated_data.get('topic')
            question = serializer.validated_data.get('question')
            
            if not topic or not question:
                return Response({'error': 'Topic and question are required.'},status=status.HTTP_422_UNPROCESSABLE_ENTITY)        
           
        diretorio = f"./api_rest/docs/{topic}"
        
        if not os.path.exists(diretorio):
            return JsonResponse({'error': 'Topic not found.'},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        pdfs = os.listdir(diretorio)
        print(pdfs)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
        texts = []

        for pdf in pdfs:
            if pdf.endswith(".pdf"):
                pdf_path = os.path.join(diretorio, pdf)
                loader = PyPDFLoader(pdf_path)
                document = loader.load_and_split()
                text = text_splitter.split_documents(document)
                texts.extend(text)
                
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = Chroma.from_documents(texts, embeddings, persist_directory=f"db/{topic}")

        prompt = PromptTemplate.from_template(
            """
            Use the following pieces of context to answer the question at the end. If you 
            don't know the answer, just say that you don't know, don't try to make up an 
            answer.

            {context}

            Question: {question}
            Helpful Answer:
            """
        )

        local_path = "./api_rest/models/Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf"

        llm = GPT4All(model=local_path, verbose=True, n_threads=8)
        qa_chain = RetrievalQA.from_chain_type(
            llm, retriever=vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5}, chain_type_kwargs={"prompt": prompt})
        )

        result = qa_chain.invoke(question)
        answer = result['result']
        
        if answer:

            dir_path = f'./api_rest/data/{topic}'
            os.makedirs(dir_path, exist_ok=True)
            with open(f'{dir_path}/qa_log.txt', 'a') as f:
                f.write(f"Question: {question}\nAnswer: {answer}\n\n")

        return Response({'answer':answer},status=status.HTTP_200_OK)

    return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

def index(request):
    return render(request, 'frontend/build/index.html')


# class SaveQAMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
        
#         if request.path == '/chat/ask/' and request.method == 'POST':
#             body = json.loads(request.body)
#             question = body.get('question')
#             response_data = json.loads(response.content)
#             answer = response_data.get('answer')
#             tema = body.get('tema')

#             if question and answer:
#                 dir_path = f'data/{tema}'
#                 os.makedirs(dir_path, exist_ok=True)
#                 with open(f'{dir_path}/qa_log.txt', 'a') as f:
#                     f.write(f"Question: {question}\nAnswer: {answer}\n\n")
        
#         return response
