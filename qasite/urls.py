"""
URL configuration for qasite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from chat import views 

from langchain.schema import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index ,name='index'),
    path('chat/', include('chat.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
