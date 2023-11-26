import random
import numpy as np

board = [' ' for _ in range(9)]
available_actions = [i for i in range(9)]
player_symbol = 'X'
random_agent_symbol = ''
agent_symbol = 'O'
Q = np.zeros((9, 9))

# Устанавливаем параметры обучения
alpha = 0.1
gamma = 0.6
sigma = 0.1

def draw_board(board):
  print('---------')
  print('|', board[0], '|', board[1], '|', board[2], '|')
  print('---------')
  print('|', board[3], '|', board[4], '|', board[5], '|')
  print('---------')
  print('|', board[6], '|', board[7], '|', board[8], '|')
  print('---------')

def check_winner(board, symbol):
  # Проверяем горизонтали
  for i in range(0, 9, 3):
    if board[i] == symbol and board[i + 1] == symbol and board[i + 2] == symbol:
      return True

  # Проверяем вертикали
  for i in range(3):
    if board[i] == symbol and board[i + 3] == symbol and board[i + 6] == symbol:
      return True

  # Проверяем диагонали
  if board[0] == symbol and board[4] == symbol and board[8] == symbol:
    return True
  if board[2] == symbol and board[4] == symbol and board[6] == symbol:
    return True

  return False

def agent_move():
  # Получаем случайный доступный ход
  action = random.choice(available_actions)
  available_actions.remove(action)
  board[action] = agent_symbol

def player_move():
  while True:
    # Просим игрока сделать ход
    action = input("Введите номер ячейки (от 0 до 8): ")

    # Проверяем, что номер ячейки валидный и доступен
    if int(action) not in available_actions:
      print("Неправильный ход, попробуйте еще раз.")
    else:
      break

  available_actions.remove(int(action))
  board[int(action)] = player_symbol

def game_over():
  # Проверяем, что все ячейки заполнены
  if ' ' not in board:
    return True

  # Проверяем победу агента
  if check_winner(board, agent_symbol):
    return True

  # Проверяем победу игрока
  if check_winner(board, player_symbol):
    return True

  return False

def train_agent():
  for _ in range(10000):
    # Сбрасываем игровое поле и доступные действия
    board = [' ' for _ in range(9)]
    available_actions = [i for i in range(9)]

    # Играем до окончания игры
    while not game_over():
      # Агент делает ход
      if random.uniform(0, 1) < sigma:
        if available_actions:
          action = random.choice(available_actions)
        else:
          break
      else:
        if available_actions:
          action = np.argmax(Q[available_actions])
        else:
          break

      if action in available_actions:
        available_actions.remove(action)
        board[action] = agent_symbol

        # Обновляем таблицу Q-значений
        if game_over():
          if check_winner(board, agent_symbol):
            reward = 1
          elif check_winner(board, player_symbol):
            reward = -1
          else:
            reward = 0
        else:
          reward = 0
          next_state = board.copy()

          if available_actions:
            next_action = random.choice(available_actions)
            available_actions.remove(next_action)
            next_state[next_action] = player_symbol

            reward += gamma * np.max(Q[available_actions])

            board = next_state

        Q[action] = Q[action] + alpha * (reward - Q[action])

train_agent()

def play_with_agent_vs_random():
  draw_board(board)  # Рисуем игровое поле

  while not game_over():
    agent_move()  # Ход агента
    draw_board(board)

    if not game_over():
      random_agent_move()  # Ход случайного агента
      draw_board(board)

   # Проверяем результат игры
  if check_winner(board, agent_symbol):
    print("Агент победил!")
  elif check_winner(board, random_agent_symbol):
    print("Агент, делающий случайные ходы, победил!")
  elif check_winner(board, player_symbol):
    print("Игрок победил!")  
  else:
    print("Ничья!")   

def play_with_agent():
  draw_board(board)  # Рисуем игровое поле

  while not game_over():
    player_move()  # Ход агента
    draw_board(board)

    if not game_over():
      agent_move()  # Ход случайного агента
      draw_board(board)
      
   # Проверяем результат игры
  if check_winner(board, agent_symbol):
    print("Агент победил!")
  elif check_winner(board, random_agent_symbol):
    print("Агент, делающий случайные ходы, победил!")
  elif check_winner(board, player_symbol):
    print("Игрок победил!")  
  else:
    print("Ничья!")   

def play_with_random_agent():
  draw_board(board)  # Рисуем игровое поле

  while not game_over():
    player_move()  # Ход агента
    draw_board(board)

    if not game_over():
      random_agent_move()  # Ход случайного агента
      draw_board(board)     

  # Проверяем результат игры
  if check_winner(board, agent_symbol):
    print("Агент победил!")
  elif check_winner(board, random_agent_symbol):
    print("Агент, делающий случайные ходы, победил!")
  elif check_winner(board, player_symbol):
    print("Игрок победил!")  
  else:
    print("Ничья!")

def random_agent_move():
  action = random.choice(available_actions)
  available_actions.remove(action)
  board[action] = random_agent_symbol

# Выбор режима игры
mode = input("Выберите режим игры (1 - с агентом, 2 - с агентом, делающим случайные ходы, 3 - агент против агента, делающего случайные ходы): ")

if mode == '1':
  play_with_agent()
elif mode == '2':
  random_agent_symbol = 'O'
  play_with_random_agent()
elif mode == '3':
  random_agent_symbol = 'X'
  play_with_agent_vs_random()
else:
  print("Неправильный режим игры.")