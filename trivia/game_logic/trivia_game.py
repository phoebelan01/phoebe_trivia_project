import random
from openai import OpenAI

class Question:
    def __init__(self, theme, question, options, answer):
        self.theme = theme
        self.question = question
        self.options = options
        self.answer = answer

    def ask(self):
        print(f"\nTheme: {self.theme}")
        print(self.question)
        print(f"1. {self.options[0]}")
        print(f"2. {self.options[1]}")
        print(f"3. {self.options[2]}")
        print(f"4. {self.options[3]}")
        user_answer = int(input("Your answer (number): "))
        print(f"Correct answer is {self.answer}")
        return user_answer == self.answer

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def update_score(self, correct):
        if correct:
            self.score += 1
            print(f"Correct! Well done, {self.name}!")
        else:
            print("Sorry, that's not right.")
        print(f"{self.name}'s current score: {self.score}")

class TriviaGame:
    def __init__(self):
        self.questions = [] 
        self.players = []  

    def add_question(self, question):
        self.questions.append(question)

    def add_player(self, player):
        self.players.append(player) 

    def play(self):
        for player in self.players:
            print(f"\n{player.name}'s turn to answer their set of questions:")
            for i in range(5):  # Assuming 5 questions per player
                question_index = self.players.index(player) * 5 + i
                if question_index < len(self.questions): 
                    question = self.questions[question_index]
                    correct = question.ask()
                    player.update_score(correct)
                else:
                    print("Ran out of questions.")
                    break
        print("\nAll players have answered their questions.")

    def show_scores(self):
        for player in self.players:
            print(f"\nIn total,{player.name} has {player.score} points.")
        highest_score = max(player.score for player in self.players)
        winners = [player.name for player in self.players if player.score == highest_score]
        print(f"\nThe winner is {winners} with {highest_score} points!")

def generate_trivia_questions(api_key, theme, num_questions):
    client = OpenAI(api_key=api_key)
    prompt = (
        f"Generate {num_questions} trivia questions on the theme '{theme}'. "
        "For each question, provide four multiple-choice options labeled as Option 1, Option 2, Option 3, Option 4. "
        "End each question with 'Correct Answer:' followed directly by the number of the correct option (1, 2, 3, or 4). "
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a trivia question generator."},
            {"role": "user", "content": prompt}
        ]
    )
    questions_text = response.choices[0].message.content.strip().split("\n\n")
    trivia_questions = []

    for q in questions_text:
        lines = q.split("\n")
        if len(lines) < 6:
            continue
        
        question_parts = lines[0].split(": ", 1)
        question_text = question_parts[1]
        
        options = [line.split(": ", 1)[1] for line in lines[1:5]]
        correct_answer = int(lines[5].split(": ", 1)[1])

        trivia_questions.append({
            "theme": theme,
            "question": question_text,
            "options": options,
            "answer": correct_answer
        })
    return trivia_questions

def start_game(api_key, theme, num_players, player_names):
    questions = generate_trivia_questions(api_key, theme, num_players * 5)
    game = TriviaGame()

    for question_info in questions:
        question = Question(
            question_info['theme'], 
            question_info['question'], 
            question_info['options'], 
            question_info['answer']
        )
        game.add_question(question)

    for name in player_names:
        player = Player(name)
        game.add_player(player)

    game.play()
    game.show_scores()

# Interactive mode
if __name__ == "__main__":
    api_key = "your_openai_api_key"  # Replace with your actual OpenAI API key
    theme = input("Enter the theme for the trivia questions: ")
    num_players = int(input("Enter the number of players: "))
    player_names = [input(f"Enter player {i + 1} name: ") for i in range(num_players)]
    start_game(api_key, theme, num_players, player_names)