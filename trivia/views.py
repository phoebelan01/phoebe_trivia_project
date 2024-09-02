from django.shortcuts import render
from .game_logic.trivia_game import TriviaGame, generate_trivia_questions
from .models import Player, Score
from rest_framework import viewsets
from .models import Player, Score, TriviaQuestion
from .serializers import PlayerSerializer, ScoreSerializer, TriviaQuestionSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

class TriviaQuestionViewSet(viewsets.ModelViewSet):
    queryset = TriviaQuestion.objects.all()
    serializer_class = TriviaQuestionSerializer

def start_game(request):
    if request.method == 'POST':
        player_name = request.POST.get('player_name')
        theme = request.POST.get('theme')
        api_key = "your-api-key"

        questions = generate_trivia_questions(api_key, theme, 5)
        game = TriviaGame()

        for question_info in questions:
            question = Question(
                question_info['theme'],
                question_info['question'],
                question_info['options'],
                question_info['answer']
            )
            game.add_question(question)

        score = game.play(player_name)
        player, created = Player.objects.get_or_create(name=player_name)
        Score.objects.create(player=player, score=score)

        return render(request, 'trivia/result.html', {'player_name': player_name, 'score': score})
    return render(request, 'trivia/start.html')