from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, ScoreViewSet, TriviaQuestionViewSet

router = DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'scores', ScoreViewSet)
router.register(r'trivia', TriviaQuestionViewSet)

urlpatterns = [
    path('start/', views.start_game, name='start_game'),
    path('', include(router.urls)),
]

