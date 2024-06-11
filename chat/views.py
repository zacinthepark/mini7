from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.http import JsonResponse
# from django import forms
# from django.urls import reverse
# from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Chroma DB
embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
database = Chroma(persist_directory='./database', embedding_function=embeddings)

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        query = request.POST.get('question')

        chat_memory_data = request.session.get('chat_memory', [])
        memory = ConversationBufferMemory(memory_key='chat_history', input_key='question', output_key='answer', return_messages=True)
        for i in range(0, len(chat_memory_data), 2):
            memory.save_context({'question': chat_memory_data[i]}, 
                                {'answer': chat_memory_data[i+1]})
        
        k = 3
        retriever = database.as_retriever(search_kwargs={'k': k})
        chat = ChatOpenAI(model='gpt-3.5-turbo')
        qa_model = ConversationalRetrievalChain.from_llm(llm=chat, retriever=retriever, memory=memory, 
                                                        return_source_documents=True, output_key='answer')
        
        response = qa_model(query)
        answer = response['answer']
        chat_memory_data.append(query)
        chat_memory_data.append(answer)
        request.session['chat_memory'] = chat_memory_data
        
        return JsonResponse({'question': query, 'answer': answer})
    else:
        if 'chat_memory' not in request.session:
            request.session['chat_memory'] = []
        
        return render(request, 'chat/index.html')
