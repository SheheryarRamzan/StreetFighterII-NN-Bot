from command import Command
import numpy as np
from buttons import Buttons
from keras.models import load_model
from sklearn.preprocessing import StandardScaler

def get_features(p1Xcoord, p1Health, p1Ycoord, isJumpP1, isCrouchP1, p2Xcoord, p2Health, p2Ycoord, isJumpP2, isCrouchP2, p1PlayerId, P1InMove, P1MoveId, p2PlayerId, P2InMove, P2MoveId, timer, RoundStart, RoundOver, delta_p1_health, delta_p2_health, delta_distance):

        # Extract the first value of each delta list
        delta_p1_health_value = delta_p1_health[0] if len(delta_p1_health) > 0 else 0
        delta_p2_health_value = delta_p2_health[0] if len(delta_p2_health) > 0 else 0
        delta_distance_value = delta_distance[0] if len(delta_distance) > 0 else 0

        # Build the list x by appending the values to the end of the other variables
        x = [p1Xcoord, p1Health, p1Ycoord, isJumpP1, isCrouchP1, p2Xcoord, p2Health, p2Ycoord, isJumpP2, isCrouchP2, p1PlayerId, P1InMove, P1MoveId, p2PlayerId, P2InMove, P2MoveId, timer, RoundStart, RoundOver, delta_p1_health_value, delta_p2_health_value, delta_distance_value]
        x = x[:-3]
        # Print the current x value
        print("x: ", x)

        # Append the next value of each delta list to x
        if len(delta_p1_health) > 1:
            x.append(delta_p1_health[1])
            delta_p1_health = delta_p1_health[1:]
        else:
            x.append(0)
        if len(delta_p2_health) > 1:
            x.append(delta_p2_health[1])
            delta_p2_health = delta_p2_health[1:]
        else:
            x.append(0)
        if len(delta_distance) > 1:
            x.append(delta_distance[1])
            delta_distance = delta_distance[1:]
        else:
            x.append(0)
            
        return x

class Bot:

    def __init__(self):
        #< - v + < - v - v + > - > + Y
        self.fire_code=["<","!<","v+<","!v+!<","v","!v","v+>","!v+!>",">+Y","!>+!Y"]
        self.exe_code = 0
        self.start_fire=True
        self.remaining_code=[]
        self.my_command = Command()
        self.buttn= Buttons()

    def fight(self,current_game_state,player):
        bot_cmd = []
        
        #python Videos\gamebot-competition-master\PythonAPI\controller.py 1
        if player=="1":
            #print("1")
            #v - < + v - < + B spinning
            
            #player 1
            p1Xcoord = current_game_state.player1.x_coord
            p1Health = current_game_state.player1.health
            p1Ycoord = current_game_state.player1.y_coord
            isJumpP1 = current_game_state.player1.is_jumping
            isCrouchP1 = current_game_state.player1.is_crouching 
            P1ButtonsUp = current_game_state.player1.player_buttons.up
            P1ButtonsDown = current_game_state.player1.player_buttons.down
            P1ButtonsRight = current_game_state.player1.player_buttons.right
            P1ButtonsLeft = current_game_state.player1.player_buttons.left
            P1ButtonsY = current_game_state.player1.player_buttons.Y
            P1ButtonsB = current_game_state.player1.player_buttons.B
            P1ButtonsX = current_game_state.player1.player_buttons.X
            P1ButtonsA = current_game_state.player1.player_buttons.A
            P1ButtonsL = current_game_state.player1.player_buttons.L
            P1ButtonsR = current_game_state.player1.player_buttons.R
            
            p1PlayerId = current_game_state.player1.player_id
            P1InMove = current_game_state.player1.is_player_in_move
            P1MoveId = current_game_state.player1.move_id
            
            #player 2
            p2Xcoord = current_game_state.player2.x_coord
            p2Health = current_game_state.player2.health
            p2Ycoord = current_game_state.player2.y_coord
            isJumpP2 = current_game_state.player2.is_jumping
            isCrouchP2 = current_game_state.player2.is_crouching
            P2ButtonsUp = current_game_state.player2.player_buttons.up
            P2ButtonsDown = current_game_state.player2.player_buttons.down
            P2ButtonsRight = current_game_state.player2.player_buttons.right
            P2ButtonsLeft = current_game_state.player2.player_buttons.left
            # P2ButtonsY = current_game_state.player2.player_buttons.Y
            # P2ButtonsB = current_game_state.player2.player_buttons.B
            # P2ButtonsX = current_game_state.player2.player_buttons.X
            # P2ButtonsA = current_game_state.player2.player_buttons.A
            # P2ButtonsL = current_game_state.player2.player_buttons.L
            # P2ButtonsR = current_game_state.player2.player_buttons.R
            p2PlayerId = current_game_state.player2.player_id
            P2InMove = current_game_state.player2.is_player_in_move
            P2MoveId = current_game_state.player2.move_id
            
            #other variables            
            timer = current_game_state.timer
            RoundStart = current_game_state.has_round_started 
            RoundOver = current_game_state.is_round_over
            FightResult = current_game_state.fight_result
            
            #print all p1 variables
            print("p1Xcoord: ", p1Xcoord)
            print("p1Health: ", p1Health)
            print("p1Ycoord: ", p1Ycoord)
            print("isJumpP1: ", isJumpP1)
            print("isCrouchP1: ", isCrouchP1)
            print("P1ButtonsUp: ", P1ButtonsUp)
            print("P1ButtonsDown: ", P1ButtonsDown)
            print("P1ButtonsRight: ", P1ButtonsRight)
            print("P1ButtonsLeft: ", P1ButtonsLeft)
            print("P1ButtonsY: ", P1ButtonsY)
            print("P1ButtonsB: ", P1ButtonsB)
            print("P1ButtonsX: ", P1ButtonsX)
            print("P1ButtonsA: ", P1ButtonsA)
            print("P1ButtonsL: ", P1ButtonsL)
            print("P1ButtonsR: ", P1ButtonsR)
            print("p1PlayerId: ", p1PlayerId)
            print("P1InMove: ", P1InMove)
            print("P1MoveId: ", P1MoveId)
            
            #print all 2 variables
            print("p2Xcoord: ", p2Xcoord)
            print("p2Health: ", p2Health)
            print("p2Ycoord: ", p2Ycoord)
            print("isJumpP2: ", isJumpP2)
            print("isCrouchP2: ", isCrouchP2)
            print("P2ButtonsUp: ", P2ButtonsUp)
            print("P2ButtonsDown: ", P2ButtonsDown)
            print("P2ButtonsRight: ", P2ButtonsRight)
            print("P2ButtonsLeft: ", P2ButtonsLeft)
            # print("P2ButtonsY: ", P2ButtonsY)
            # print("P2ButtonsB: ", P2ButtonsB)
            # print("P2ButtonsX: ", P2ButtonsX)
            # print("P2ButtonsA: ", P2ButtonsA)
            # print("P2ButtonsL: ", P2ButtonsL)
            # print("P2ButtonsR: ", P2ButtonsR)
            print("p2PlayerId: ", p2PlayerId)
            print("P2InMove: ", P2InMove)
            print("P2MoveId: ", P2MoveId)

            #print other variables
            print("timer: ", timer)
            print("RoundStart: ", RoundStart)
            print("RoundOver: ", RoundOver) 
            print("FightResult: ", FightResult)
            print("---------------------------------------------------")
            
            import os
            import csv

            filename = 'data.csv'

            # check if the file exists and is empty
            if os.path.isfile(filename) and os.stat(filename).st_size > 0:
                # file exists and is not empty, append data without header row
                with open(filename, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([p1Xcoord,p1Health,p1Ycoord,isJumpP1,isCrouchP1,P1ButtonsUp,P1ButtonsDown,P1ButtonsRight,P1ButtonsLeft,P1ButtonsY,P1ButtonsB,P1ButtonsX,P1ButtonsA,P1ButtonsL,P1ButtonsR,p1PlayerId,P1InMove,P1MoveId,p2Xcoord,p2Health,p2Ycoord,isJumpP2,isCrouchP2,p2PlayerId,P2InMove,P2MoveId,timer,RoundStart,RoundOver,FightResult])
            else:
                # file does not exist or is empty, write data with header row
                with open(filename, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['p1Xcoord','p1Health','p1Ycoord','isJumpP1','isCrouchP1','P1ButtonsUp','P1ButtonsDown','P1ButtonsRight','P1ButtonsLeft','P1ButtonsY','P1ButtonsB','P1ButtonsX','P1ButtonsA','P1ButtonsL','P1ButtonsR','p1PlayerId','P1InMove','P1MoveId','p2Xcoord','p2Health','p2Ycoord','isJumpP2','isCrouchP2','p2PlayerId','P2InMove','P2MoveId','timer','RoundStart','RoundOver','FightResult'])
                    writer.writerow([p1Xcoord,p1Health,p1Ycoord,isJumpP1,isCrouchP1,P1ButtonsUp,P1ButtonsDown,P1ButtonsRight,P1ButtonsLeft,P1ButtonsY,P1ButtonsB,P1ButtonsX,P1ButtonsA,P1ButtonsL,P1ButtonsR,p1PlayerId,P1InMove,P1MoveId,p2Xcoord,p2Health,p2Ycoord,isJumpP2,isCrouchP2,p2PlayerId,P2InMove,P2MoveId,timer,RoundStart,RoundOver,FightResult])

            
            #---------------------------------------------------------------       
        
            if( self.exe_code!=0  ):
                self.run_command([],current_game_state.player1)
                model = load_model('model.h5')
                sc = StandardScaler()

                #print("model loaded")
                #print("p1Xcoord: ", p1Xcoord)
                
                 # # p1HealthList

                # p1HealthList = []
                # p1HealthList.append(p1Health)
                
                # # p2HealthList
                # p2HealthList = []
                # p2HealthList.append(p2Health)
                
                # # delta p1 health 
                # delta_p1_health = []
                # for i in range(0,len(p1HealthList)-1):
                #     delta_p1_health.append(p1HealthList[i+1]-p1HealthList[i])
                
                # # delta p2 health
                # delta_p2_health = []
                # for i in range(0,len(p2HealthList)-1):
                #     delta_p2_health.append(p2HealthList[i+1]-p2HealthList[i])
                
                # # p1XcoordList
                # p1XcoordList = []
                # p1XcoordList.append(p1Xcoord)
                # # p1YcoordList
                # p1YcoordList = []
                # p1YcoordList.append(p1Ycoord)
                # # p2XcoordList
                # p2XcoordList = []
                # p2XcoordList.append(p2Xcoord)
                # # p2YcoordList
                # p2YcoordList = []
                # p2YcoordList.append(p2Ycoord)
                
                # #----------------------------------------------------------------
                
                # # Initialize the previous values
                # previous_p1_x = p1XcoordList[0]
                # previous_p1_y = p1YcoordList[0]
                # previous_p2_x = p2XcoordList[0]
                # previous_p2_y = p2YcoordList[0]
                # previous_distance = ((previous_p1_x - previous_p2_x) * 2 + (previous_p1_y - previous_p2_y) * 2) * 0.5

                # # Initialize the delta distance list
                # delta_distance = []

                # # Loop through the lists
                # for i in range(1, len(p1XcoordList)):
                #     # Extract the current values
                #     current_p1_x = p1XcoordList[i]
                #     current_p1_y = p1YcoordList[i]
                #     current_p2_x = p2XcoordList[i]
                #     current_p2_y = p2YcoordList[i]

                #     # Calculate the delta distance using the provided formula
                #     current_distance = ((current_p1_x - current_p2_x) * 2 + (current_p1_y - current_p2_y) * 2) * 0.5 - ((previous_p1_x - previous_p2_x) * 2 + (previous_p1_y - previous_p2_y) * 2) * 0.5

                #     # Append the delta distance to the list
                #     delta_distance.append(current_distance)

                #     # Update the previous values
                #     previous_p1_x = current_p1_x
                #     previous_p1_y = current_p1_y
                #     previous_p2_x = current_p2_x
                #     previous_p2_y = current_p2_y
                #     previous_distance = current_distance

                # # Print the delta values
                # print("Delta p1 health: ", delta_p1_health)
                # print("Delta p2 health: ", delta_p2_health)
                # print("Delta distance: ", delta_distance)            

                #print("model loaded")
                #print("p1Xcoord: ", p1Xcoord)
                
                
                delta_p1_health = 15
                delta_p2_health = 0
                delta_distance =  ((p1Xcoord - p2Xcoord)**2 + (p1Ycoord - p2Ycoord)**2) ** 0.5

                x = [p1Xcoord, p1Health, p1Ycoord, isJumpP1, isCrouchP1, p2Xcoord, p2Health, p2Ycoord, isJumpP2, isCrouchP2, p1PlayerId, P1InMove, P1MoveId, p2PlayerId, P2InMove, P2MoveId, timer, RoundStart, RoundOver, delta_p1_health, delta_p2_health, delta_distance]
                print("x: ", x)
                
                # call get features function
                # x = get_features(p1Xcoord, p1Health, p1Ycoord, isJumpP1, isCrouchP1, p2Xcoord, p2Health, p2Ycoord, isJumpP2, isCrouchP2, p1PlayerId, P1InMove, P1MoveId, p2PlayerId, P2InMove, P2MoveId, timer, RoundStart, RoundOver, delta_p1_health, delta_p2_health, delta_distance)
                # print("x: ", x)
                
                x = sc.fit_transform(np.array([x]))

                y_pred = model.predict(x)
                pred_move = []
                for i in range(0,len(y_pred[0])):
                    if y_pred[0][i] > 0.1:
                        pred_move.append(i)

                print("pred_move: ", pred_move)

                for i in range(len(pred_move)):
                    print("pred_move[i]: , i", pred_move[i] , i)
                    if pred_move[i] == 0:
                        bot_cmd.append("^")
                    if pred_move[i] == 1:
                        bot_cmd.append("v")
                    if pred_move[i] == 2:
                        bot_cmd.append(">")
                    if pred_move[i] == 3:
                        bot_cmd.append("<")
                    if pred_move[i] == 4:
                        bot_cmd.append("Y")
                    if pred_move[i] == 5:
                        bot_cmd.append("B")
                    if pred_move[i] == 6:
                        bot_cmd.append("X")
                    if pred_move[i] == 7:
                        bot_cmd.append("A")
                    if pred_move[i] == 8:
                        bot_cmd.append("L")
                    if pred_move[i] == 9:
                        bot_cmd.append("R")

                print("bot_cmd: ", bot_cmd)
            self.run_command(bot_cmd,current_game_state.player1)
            self.my_command.player_buttons = self.buttn
                
            # if (  diff > 60 ) :
            #     toss=np.random.randint(3)
            #     if (toss==0):
            #         #self.run_command([">+^+Y",">+^+Y",">+^+Y","!>+!^+!Y"],current_game_state.player1)
            #         self.run_command([">","-","!>","v+>","-","!v+!>","v","-","!v","v+<","-","!v+!<","<+Y","-","!<+!Y"],current_game_state.player1)
            #     elif ( toss==1 ):
            #         self.run_command([">+^+B",">+^+B","!>+!^+!B"],current_game_state.player1)
            #     else: #fire
            #         self.run_command(["<","-","!<","v+<","-","!v+!<","v","-","!v","v+>","-","!v+!>",">+Y","-","!>+!Y"],current_game_state.player1)
            # elif (  diff < -60 ) :
            #     toss=np.random.randint(3)
            #     if (toss==0):#spinning
            #         #self.run_command(["<+^+Y","<+^+Y","<+^+Y","!<+!^+!Y"],current_game_state.player1)
            #         self.run_command(["<","-","!<","v+<","-","!v+!<","v","-","!v","v+>","-","!v+!>",">+Y","-","!>+!Y"],current_game_state.player1)
            #     elif ( toss==1):#
            #         self.run_command(["<+^+B","<+^+B","!<+!^+!B"],current_game_state.player1)
            #     else: #fire
            #         self.run_command([">","-","!>","v+>","-","!v+!>","v","-","!v","v+<","-","!v+!<","<+Y","-","!<+!Y"],current_game_state.player1)
            # else:
            #     toss=np.random.randint(2)  # anyFightActionIsTrue(current_game_state.player2.player_buttons)
            #     if ( toss>=1 ):
            #         if (diff>0):
            #             self.run_command(["<","<","!<"],current_game_state.player1)
            #         else:
            #             self.run_command([">",">","!>"],current_game_state.player1)
            #     else:
            #         self.run_command(["v+R","v+R","v+R","!v+!R"],current_game_state.player1)
            # self.my_command.player_buttons=self.buttn
            return self.my_command


    def run_command( self , com , player   ):

        if self.exe_code-1==len(self.fire_code):
            self.exe_code=0
            self.start_fire=False
            print ("compelete")
            #exit()
            # print ( "left:",player.player_buttons.left )
            # print ( "right:",player.player_buttons.right )
            # print ( "up:",player.player_buttons.up )
            # print ( "down:",player.player_buttons.down )
            # print ( "Y:",player.player_buttons.Y )

        elif len(self.remaining_code)==0 :

            self.fire_code=com
            #self.my_command=Command()
            self.exe_code+=1

            self.remaining_code=self.fire_code[0:]

        else:
            self.exe_code+=1
            if self.remaining_code[0]=="v+<":
                self.buttn.down=True
                self.buttn.left=True
                print("v+<")
            elif self.remaining_code[0]=="!v+!<":
                self.buttn.down=False
                self.buttn.left=False
                print("!v+!<")
            elif self.remaining_code[0]=="v+>":
                self.buttn.down=True
                self.buttn.right=True
                print("v+>")
            elif self.remaining_code[0]=="!v+!>":
                self.buttn.down=False
                self.buttn.right=False
                print("!v+!>")

            elif self.remaining_code[0]==">+Y":
                self.buttn.Y= True #not (player.player_buttons.Y)
                self.buttn.right=True
                print(">+Y")
            elif self.remaining_code[0]=="!>+!Y":
                self.buttn.Y= False #not (player.player_buttons.Y)
                self.buttn.right=False
                print("!>+!Y")

            elif self.remaining_code[0]=="<+Y":
                self.buttn.Y= True #not (player.player_buttons.Y)
                self.buttn.left=True
                print("<+Y")
            elif self.remaining_code[0]=="!<+!Y":
                self.buttn.Y= False #not (player.player_buttons.Y)
                self.buttn.left=False
                print("!<+!Y")

            elif self.remaining_code[0]== ">+^+L" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.L= not (player.player_buttons.L)
                print(">+^+L")
            elif self.remaining_code[0]== "!>+!^+!L" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.L= False #not (player.player_buttons.L)
                print("!>+!^+!L")

            elif self.remaining_code[0]== ">+^+Y" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.Y= not (player.player_buttons.Y)
                print(">+^+Y")
            elif self.remaining_code[0]== "!>+!^+!Y" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.Y= False #not (player.player_buttons.L)
                print("!>+!^+!Y")


            elif self.remaining_code[0]== ">+^+R" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.R= not (player.player_buttons.R)
                print(">+^+R")
            elif self.remaining_code[0]== "!>+!^+!R" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.R= False #ot (player.player_buttons.R)
                print("!>+!^+!R")

            elif self.remaining_code[0]== ">+^+A" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.A= not (player.player_buttons.A)
                print(">+^+A")
            elif self.remaining_code[0]== "!>+!^+!A" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.A= False #not (player.player_buttons.A)
                print("!>+!^+!A")

            elif self.remaining_code[0]== ">+^+B" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.B= not (player.player_buttons.B)
                print(">+^+B")
            elif self.remaining_code[0]== "!>+!^+!B" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.B= False #not (player.player_buttons.A)
                print("!>+!^+!B")

            elif self.remaining_code[0]== "<+^+L" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.L= not (player.player_buttons.L)
                print("<+^+L")
            elif self.remaining_code[0]== "!<+!^+!L" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.L= False  #not (player.player_buttons.Y)
                print("!<+!^+!L")

            elif self.remaining_code[0]== "<+^+Y" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.Y= not (player.player_buttons.Y)
                print("<+^+Y")
            elif self.remaining_code[0]== "!<+!^+!Y" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.Y= False  #not (player.player_buttons.Y)
                print("!<+!^+!Y")

            elif self.remaining_code[0]== "<+^+R" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.R= not (player.player_buttons.R)
                print("<+^+R")
            elif self.remaining_code[0]== "!<+!^+!R" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.R= False  #not (player.player_buttons.Y)
                print("!<+!^+!R")

            elif self.remaining_code[0]== "<+^+A" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.A= not (player.player_buttons.A)
                print("<+^+A")
            elif self.remaining_code[0]== "!<+!^+!A" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.A= False  #not (player.player_buttons.Y)
                print("!<+!^+!A")

            elif self.remaining_code[0]== "<+^+B" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.B= not (player.player_buttons.B)
                print("<+^+B")
            elif self.remaining_code[0]== "!<+!^+!B" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.B= False  #not (player.player_buttons.Y)
                print("!<+!^+!B")

            elif self.remaining_code[0]== "v+R" :
                self.buttn.down=True
                self.buttn.R= not (player.player_buttons.R)
                print("v+R")
            elif self.remaining_code[0]== "!v+!R" :
                self.buttn.down=False
                self.buttn.R= False  #not (player.player_buttons.Y)
                print("!v+!R")

            else:
                if self.remaining_code[0] =="v" :
                    self.buttn.down=True
                    print ( "down" )
                elif self.remaining_code[0] =="!v":
                    self.buttn.down=False
                    print ( "Not down" )
                elif self.remaining_code[0] =="<" :
                    print ( "left" )
                    self.buttn.left=True
                elif self.remaining_code[0] =="!<" :
                    print ( "Not left" )
                    self.buttn.left=False
                elif self.remaining_code[0] ==">" :
                    print ( "right" )
                    self.buttn.right=True
                elif self.remaining_code[0] =="!>" :
                    print ( "Not right" )
                    self.buttn.right=False

                elif self.remaining_code[0] =="^" :
                    print ( "up" )
                    self.buttn.up=True
                elif self.remaining_code[0] =="!^" :
                    print ( "Not up" )
                    self.buttn.up=False
            self.remaining_code=self.remaining_code[1:]
        return
