from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # Route everything to your app
    path('rag_app/', include('rag_app.urls')),  # Include URLs from rag_app
    path('sentiment/', include('sentiment_analysis.urls')),
    path('webscrape/', include('webscrape_qa.urls')),  # 👈 Add this line
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)