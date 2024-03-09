from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path,include
from rest_framework import routers
from . import views
from . import Aiviews
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('',views.index),
    path('',include(router.urls)),
    path('login', views.UserLoginView.as_view()),
    path('conversation', Aiviews.AiViewSet.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
