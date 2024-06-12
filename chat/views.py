from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.http import JsonResponse
# from django import forms
# from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import History

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
        # 질문 내용
        query = request.POST.get('question')

        # 현재 세션에 있는 채팅 기록을 CoversationBufferMemory에 추가
        chat_memory_data = request.session.get('chat_memory', [])
        memory = ConversationBufferMemory(memory_key='chat_history', input_key='question', output_key='answer', return_messages=True)
        for i in range(0, len(chat_memory_data), 2):
            memory.save_context({'question': chat_memory_data[i]}, 
                                {'answer': chat_memory_data[i+1]})
        
        # 모델 선언
        k = 3
        retriever = database.as_retriever(search_kwargs={'k': k})
        chat = ChatOpenAI(model='gpt-3.5-turbo')
        qa_model = ConversationalRetrievalChain.from_llm(llm=chat, retriever=retriever, memory=memory, 
                                                        return_source_documents=True, output_key='answer')
        
        # LLM을 통해 답변 생성
        response = qa_model(query)
        answer = response['answer']
        
        # 채팅 이력 DB에 저장 (chat_time, query, answer, sim1, sim2, sim3)
        chat_time = timezone.now()
        sim_docs = database.similarity_search_with_score(query)[:3]
        sim1, sim2, sim3 = float(0), float(0), float(0)
        for i, doc in enumerate(sim_docs):
            content, score = doc
            if i == 0:
                sim1 = score
            elif i == 1:
                sim2 = score
            elif i == 2:
                sim3 = score
        
        chat_history = History(chat_time=chat_time, query=query, answer=answer, sim1=sim1, sim2=sim2, sim3=sim3)
        chat_history.save()
        
        # 세션에 채팅 기록 저장
        chat_memory_data.append(query)
        chat_memory_data.append(answer)
        request.session['chat_memory'] = chat_memory_data
        
        return JsonResponse({'question': query, 'answer': answer})
    else:
        if 'chat_memory' not in request.session:
            request.session['chat_memory'] = []
        
        return render(request, 'chat/index.html')
    
#저장된 데이터 불러오기
def index(request):
    request.session.flush()
    
    embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
    database = Chroma(persist_directory='./database', embedding_function=embeddings)
    docs_info = database.get()
    metadatas = docs_info['metadatas']
    contents = docs_info['documents']
    
    qa = []
    
    for i in range(len(contents)):
        content_str = contents[i]
        content_lst = content_str.split('\n')
        q = content_lst[0]
        a = content_lst[1]
        cate = metadatas[i]['category']
        data = {
            'question': q, 
            'answer': a, 
            'category': cate
        }
        qa.append(data)
    
    return render(request, 'index.html', {'qa': qa})

