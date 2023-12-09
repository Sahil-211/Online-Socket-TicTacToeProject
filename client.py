import random
import socket
import threading

def send_message(client_socket,move):
   client_socket.send(move.encode())

def receive_message(client_socket):
   while True:
       data = client_socket.recv(1024)
       #print("Received message:", data.decode('utf-8'))
       return data

board = [["-","-","-"],
       ["-","-","-"],
       ["-","-","-"]]


def print_board(TwoDArray):
   for row in TwoDArray:
       row_str = ' '.join('{:2}'.format(item) for item in row)
       print(*row)

def checkGame(TwoDarray):
   if TwoDarray[0][0]=="O" and TwoDarray[0][1]=="O" and TwoDarray[0][2]=="O":
       return 1
   if TwoDarray[1][0]=="O" and TwoDarray[1][1]=="O" and TwoDarray[1][2]=="O":
       return 1
   if TwoDarray[2][0]=="O" and TwoDarray[2][1]=="O" and TwoDarray[2][2]=="O":
       return 1
   if TwoDarray[0][0]=="O" and TwoDarray[1][0]=="O" and TwoDarray[2][0]=="O":
       return 1
   if TwoDarray[0][1]=="O" and TwoDarray[1][1]=="O" and TwoDarray[2][1]=="O":
       return 1
   if TwoDarray[0][2]=="O" and TwoDarray[1][2]=="O" and TwoDarray[2][2]=="O":
       return 1
   if TwoDarray[0][0]=="O" and TwoDarray[1][1]=="O" and TwoDarray[2][2]=="O":
       return 1
   if TwoDarray[0][2]=="O" and TwoDarray[1][1]=="O" and TwoDarray[2][0]=="O":
       return 1

   if TwoDarray[0][0]=="X" and TwoDarray[0][1]=="X" and TwoDarray[0][2]=="X":
       return 2
   if TwoDarray[1][0]=="X" and TwoDarray[1][1]=="X" and TwoDarray[1][2]=="X":
       return 2
   if TwoDarray[2][0]=="X" and TwoDarray[2][1]=="X" and TwoDarray[2][2]=="X":
       return 2
   if TwoDarray[0][0]=="X" and TwoDarray[1][0]=="X" and TwoDarray[2][0]=="X":
       return 2
   if TwoDarray[0][1]=="X" and TwoDarray[1][1]=="X" and TwoDarray[2][1]=="X":
       return 2
   if TwoDarray[0][2]=="X" and TwoDarray[1][2]=="X" and TwoDarray[2][2]=="X":
       return 2
   if TwoDarray[0][0]=="X" and TwoDarray[1][1]=="X" and TwoDarray[2][2]=="X":
       return 2
   if TwoDarray[0][2]=="X" and TwoDarray[1][1]=="X" and TwoDarray[2][0]=="X":
       return 2

   return 0


def tictactoe():#human to human
   client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   client_socket.connect(('129.8.223.159', 8080))                       #WE WILL HAVE TO CHANGE THE IP ADDRESS
                                                                        #TO WHATEVER THE SERVER FILE IS RUN ON
   stuff1=client_socket.recv(4096)
   stuff1=stuff1.decode('utf-8')
   print("You are player:",stuff1[0])
   global board
   tutorial_board= [
           ["00","10","20"],
           ["01","11","21"],
           ["02","12","22"]]


   turn = int(stuff1[0])

   yourSymbol=None
   theirSymbol=None
   if turn==1:
       yourSymbol="O"
       theirSymbol="X"
   elif turn==2:
       yourSymbol="X"
       theirSymbol="O"
   inval=0
   gameStatus = 0 #0 means game is running, 1 means game is finish
   print_board(tutorial_board)
   print("Above is a map of the board")
   print("Enter coordinates as xy, for example: 00 or 01")
   x= None
   y= None

   while gameStatus == 0:
       if turn == 1:
           while 1:
               inval = input(f"Player {stuff1}'s turn, Enter xy coordinate or T for the tutorial board:")
               if inval.isdigit():
                   x = int(inval[0])
                   y = int(inval[1])

               elif inval[0] == "T" or "t":
                   print_board(tutorial_board)
               if x>2 or y>2:
                   print("Try Again")
               if board[y][x] =="X" or board[y][x]=="O" or board[y][x] !="-" :
                   print("Invalid Move Try Again")

               else:
                   break
           board[y][x]=yourSymbol
           move=str(x)+str(y)
           #print("entering send_message")
           send_message(client_socket,move)
           #print("out of send_message")
           turn=2

       elif turn == 2:
           print("Other Players Turn...")
           move=receive_message(client_socket)
           move=move.decode('utf-8')
           print("Other players move was:",move)
           x=int(move[0])
           y=int(move[1])
           board[y][x]=theirSymbol
           turn=1

       print_board(board)
       if checkGame(board)==1:
           print("Player 1 Won")
           break
       elif checkGame(board)==2:
           print("Player 2 Won")
           break
   else:
       print("Game Ended")


def tictactoeWithComputer():

   global board
   tutorial_board= [
           ["00","10","20"],
           ["01","11","21"],
           ["02","12","22"]]


   turn = 1

   inval=0
   gameStatus = 0 #0 means game is running, 1 means game is finish
   print_board(tutorial_board)
   print("Above is a map of the board")
   print("Enter coordinates as xy, for example: 00 or 01")
   x= None
   y= None

   while gameStatus == 0:
       if turn == 1:
           while 1:
               inval = input("Player 1's turn, Enter xy coordinate or T for the tutorial board:")
               if inval.isdigit():
                   x = int(inval[0])
                   y = int(inval[1])

               elif inval[0] == "T" or "t":
                   print_board(tutorial_board)
               if x>2 or y>2:
                   print("Try Again")
               if board[y][x] =="X" or board[y][x]=="O" or board[y][x] !="-" :
                   print("Invalid Move Try Again")

               else:
                   break
           board[y][x]="O"
           turn=2

       elif turn == 2:
            print("Computers Turn")
            while 1:
                y=random.randint(0,2)
                x=random.randint(0,2)
                if board[y][x]=="-":
                    break
            print("Computer Chose: ", x , "," , y)

            board[y][x]="X"
            turn=1

       print_board(board)
       if checkGame(board)==1:
           print("Player 1 Won")
           break
       elif checkGame(board)==2:
           print("Player 2 Won")
           break
   else:
       print("Game Ended")




def main():
    global board
    while 1:
        board = [["-","-","-"], #reset the board after a game with a human or computer
                ["-","-","-"],
                ["-","-","-"]]
        inval=input("Press 1 to play with a computer or press 2 to play with a Human:")
        if(int(inval)==1): #computer function
            tictactoeWithComputer()
        elif(int(inval)==2):
            tictactoe()#play with human


main()
