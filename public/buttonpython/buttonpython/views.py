from django.shortcuts import render
import sys
import time
import random

num_trials = 5
mutation_rate = .8
num_clones = 3
population_size = 75
tournament_win_prob = .75
tournament_size = 10
crossover_locations = 3


blank_row = "          "
full_row  = "##########"
score_by_row = dict()
score_by_row[0] = 0
score_by_row[1] = 40
score_by_row[2] = 100
score_by_row[3] = 300
score_by_row[4] = 1200

#PIECES
pieces = dict()
pieces_list = ((0,1),(2,),(3,4,5,6),(7,8,9,10),(11,12,13,14),(15,16),(17,18))
pieces[0] = ((0,4),)                            # 0 : I1
pieces[1] = ((0,1),(0,1),(0,1),(0,1))           # 1 : I0

pieces[2] = ((0,2),(0,2))                       # 2 : O0

pieces[3] = ((0,3),(0,1))                       # 3 : L1
pieces[4] = ((0,2),(1,1),(1,1))                 # 4 : L2
pieces[5] = ((2,1),(0,3))                       # 5 : L3
pieces[6] = ((0,1),(0,1),(0,2))                 # 6 : L0

pieces[7] = ((0,1),(0,3))                       # 7 : J3
pieces[8] = ((0,2),(0,1),(0,1))                 # 8 : J0
pieces[9] = ((0,3),(2,1))                       # 9 : J1
pieces[10] = ((1,1),(1,1),(0,2))                #10 : J2

pieces[11] = ((0,1),(0,2),(0,1))                #11 : T0
pieces[12] = ((0,3),(1,1))                      #12 : T1
pieces[13] = ((1,1),(0,2),(1,1))                #13 : T2
pieces[14] = ((1,1),(0,3))                      #14 : T3

pieces[15] = ((1,2),(0,2))                      #15 : S1
pieces[16] = ((0,1),(0,2),(1,1))                #16 : S0

pieces[17] = ((0,2),(1,2))                      #17 : Z1
pieces[18] = ((1,1),(0,2),(0,1))                #18 : Z0

def display_board(board):
    s = "=====================\n"
    for h in range(0,20):
        s+="|"
        for w in range(0,10):
            s+=board[h*10+w]+ " "
        s = s[:len(s)-1]
        s+="|\t" + str(h) + "\n"
    s += "=====================\n"
    s += " 0 1 2 3 4 5 6 7 8 9 "
    print(s[:len(s)])
    return s

def get_possible_boards(board):
    possible_boards = []
    for l in range(0,10):
        for p in range(0,19):
            piece = pieces[p]
            width = len(piece)
            if width + l > 10:
                continue
            max_y = 20
            min_y = 20
            for i in range(l,l+width):
                for h in range(0,max_y):
                    if board[h*10+i]=="#":
                        max_y = min(max_y,h+piece[i-l][0])
                        break
            new_board = board
            game_over = False
            for i in range(0,width):
                add,height = piece[i]
                min_y = min(min_y,max_y-add-height)
                if max_y-add-height < 0:
                    game_over = True
                    break
                if height == 1:
                    new_board = new_board[:(max_y-add-height)*10+i+l] + "#" + new_board[(max_y-add-height)*10+i+l+1:]
                elif height == 2:
                    new_board = new_board[:(max_y-add-height)*10+i+l] + "#" + new_board[(max_y-add-height)*10+i+l+1:(max_y-add-height+1)*10+i+l] + "#" + new_board[(max_y-add-height+1)*10+i+l+1:]
                elif height == 3:
                    new_board = new_board[:(max_y-add-height)*10+i+l] + "#" + new_board[(max_y-add-height)*10+i+l+1:(max_y-add-height+1)*10+i+l] + "#" + new_board[(max_y-add-height+1)*10+i+l+1:(max_y-add-height+2)*10+i+l] + "#" + new_board[(max_y-add-height+2)*10+i+l+1:]
                elif height == 4:
                    new_board = new_board[:(max_y-add-height)*10+i+l] + "#" + new_board[(max_y-add-height)*10+i+l+1:(max_y-add-height+1)*10+i+l] + "#" + new_board[(max_y-add-height+1)*10+i+l+1:(max_y-add-height+2)*10+i+l] + "#" + new_board[(max_y-add-height+2)*10+i+l+1:(max_y-add-height+3)*10+i+l] + "#" + new_board[(max_y-add-height+3)*10+i+l+1:]
            if not game_over:
                for i in range(min_y,max_y):
                    row = new_board[i*10:(i+1)*10]
                    if row == full_row:
                        new_board = blank_row + new_board[:i*10] + new_board[(i+1)*10:]
                possible_boards.append(new_board)
            else:
                possible_boards.append("GAME OVER")
    return possible_boards

def place_piece(piece_num, l, board):
    piece = pieces[piece_num]
    width = len(piece)
    if width + l > 10:
        return("INVALID",0)
    max_y = 20
    min_y = 20
    for i in range(l,l+width):
        for h in range(0,max_y):
            if board[h*10+i]=="#":
                max_y = min(max_y,h+piece[i-l][0])
                break
    new_board = board
    game_over = False
    for i in range(0,width):
        add,height = piece[i]
        min_y = min(min_y,max_y-add-height)
        if max_y-add-height < 0:
            game_over = True
            break
        if height == 1:
            new_board = new_board[:(max_y-add-height)*10+i+l] + "#" + new_board[(max_y-add-height)*10+i+l+1:]
        elif height == 2:
            new_board = new_board[:(max_y-add-height)*10+i+l] + "#" + new_board[(max_y-add-height)*10+i+l+1:(max_y-add-height+1)*10+i+l] + "#" + new_board[(max_y-add-height+1)*10+i+l+1:]
        elif height == 3:
            new_board = new_board[:(max_y-add-height)*10+i+l] + "#" + new_board[(max_y-add-height)*10+i+l+1:(max_y-add-height+1)*10+i+l] + "#" + new_board[(max_y-add-height+1)*10+i+l+1:(max_y-add-height+2)*10+i+l] + "#" + new_board[(max_y-add-height+2)*10+i+l+1:]
        elif height == 4:
            new_board = new_board[:(max_y-add-height)*10+i+l] + "#" + new_board[(max_y-add-height)*10+i+l+1:(max_y-add-height+1)*10+i+l] + "#" + new_board[(max_y-add-height+1)*10+i+l+1:(max_y-add-height+2)*10+i+l] + "#" + new_board[(max_y-add-height+2)*10+i+l+1:(max_y-add-height+3)*10+i+l] + "#" + new_board[(max_y-add-height+3)*10+i+l+1:]
    if not game_over:
        num_lines = 0
        points_earned = 0
        for i in range(min_y,max_y):
            row = new_board[i*10:(i+1)*10]
            if row == full_row:
                num_lines+=1
                new_board = blank_row + new_board[:i*10] + new_board[(i+1)*10:]
            else:
                points_earned+=score_by_row[num_lines]
                num_lines = 0
        points_earned+=score_by_row[num_lines]
        return (new_board,points_earned)
    return ("GAME OVER",0)

def get_heuristic(board,strategy):
    score = 0
    max_ys = dict()
    for i in range(0,10):
        max_ys[i] = 19
    total_h = 0
    a,b,c,ae,be,ce = strategy #bumpiness,holes,height
    for w in range(0,10):
        for h in range(0,20):
            if board[w+h*10] == "#":
                max_ys[w] = h
                total_h += h
                break
    for h in range(0,20):
        for w in range(0,10):
            if board[h*10+w] == "#":
                continue
            if w != 0:
                if h >= max_ys[w-1]:
                    # score+=a*h**2 #could use this as strategy changing parameters (the h**2) , bumpiness
                    score+=(a*h)**ae
            if w != 9:
                if h >= max_ys[w+1]:
                    # score+=a*h**2 #bumpiness
                    score+=(a*h)**ae
            if h >= max_ys[w]:
                # score+=b*h**3     #hole holes
                score+=(b*h)**be
    score+=(total_h*c)**ce #want lower score
    return score

def make_new_board():
    board = ""
    for i in range(0,200):
        board+=" "
    return board

def fitness_function(strategy):
    game_scores = 0
    for i in range(num_trials):
        game_scores+=play_game(strategy)
    return game_scores/num_trials

def play_game(strategy):
    board = make_new_board()
    points = 0
    game_over = False
    while not game_over:
        possible_boards = []
        i = random.randint(0,len(pieces_list)-1)
        for piece in pieces_list[i]:
            for w in range(0,10):
                poss_board,poss_points = place_piece(piece, w, board)
                if poss_board != "GAME OVER" and poss_board != "INVALID":
                    poss_score = get_heuristic(poss_board, strategy)
                    possible_boards.append((poss_board,poss_score,poss_points))
        if len(possible_boards) == 0:
            game_over = True
        else:
            possible_boards = sorted(possible_boards,key = lambda x:x[1])
            # print(possible_boards[0][1])
            board = possible_boards[0][0]
            # display_board(board)
            points += possible_boards[0][2]
    # print(points)
    return points

def play_and_display_game(strategy):
    board = make_new_board()
    points = 0
    game_over = False
    while not game_over:
        possible_boards = []
        i = random.randint(0,len(pieces_list)-1)
        for piece in pieces_list[i]:
            for w in range(0,10):
                poss_board,poss_points = place_piece(piece, w, board)
                if poss_board != "GAME OVER" and poss_board != "INVALID":
                    poss_score = get_heuristic(poss_board, strategy)
                    possible_boards.append((poss_board,poss_score,poss_points))
        if len(possible_boards) == 0:
            game_over = True
        else:
            possible_boards = sorted(possible_boards,key = lambda x:x[1])
            # print(possible_boards[0][1])
            board = possible_boards[0][0]
            # display_board(board)
            points += possible_boards[0][2]
        print("Current Board:","\n")
        display_board(board)
        print("Current Score:",points,"\n")
        # time.sleep(0.5)
    print("Final score:",points)

def create_initial_pop():
    initial_pop = []
    for i in range(0,population_size):
        random_strategy = (random.random(),random.random(),random.random(),random.uniform(0,3),random.uniform(0,3),random.uniform(0,3))
        fitness_score = fitness_function(random_strategy)
        initial_pop.append((random_strategy,fitness_score))
    initial_pop = sorted(initial_pop,key = lambda x:x[1],reverse=True)
    return initial_pop

def genetic_algorithm():
    gen_list = create_initial_pop()
    print("initial:",gen_list[0])
    print()
    create_new_generation(gen_list,1)
    
def create_new_generation(gen_list,gen):
    new_gen_list = []
    new_gen_set = set()
    while len(new_gen_list) < population_size:
        tournaments = random.sample(gen_list,tournament_size*2)
        tournament_1 = tournaments[:tournament_size]
        tournament_2 = tournaments[tournament_size:]
        tournament_1 = sorted(tournament_1,key = lambda x:x[1],reverse=True)
        tournament_2 = sorted(tournament_2,key = lambda x:x[1],reverse=True)
        parent_1_index = 0
        parent_2_index = 0
        while parent_1_index < len(tournament_1):
            if(random.random() > tournament_win_prob):
                parent_1_index+=1
            else:
                break
        while parent_2_index < len(tournament_2):
            if(random.random() > tournament_win_prob):
                parent_2_index+=1
            else:
                break
        parent_1 = tournament_1[parent_1_index][0]
        parent_2 = tournament_2[parent_2_index][0]
        child_0 = 0
        child_1 = 0
        child_2 = 0
        child_3 = 0
        child_4 = 0
        child_5 = 0
        added = set()
        while len(added) < crossover_locations:
            random_location = random.randint(0,5)
            if random_location not in added:
                added.add(random_location)
                if random_location == 0:
                    child_0 = parent_1[0]
                elif random_location == 1:
                    child_1 = parent_1[1]
                elif random_location == 2:
                    child_2 = parent_1[2]
                if random_location == 3:
                    child_3 = parent_1[3]
                elif random_location == 4:
                    child_4 = parent_1[4]
                elif random_location == 5:
                    child_5 = parent_1[5]
        for i in range(0,6):
            if i in added:
                continue
            elif i == 0:
                child_0 = parent_2[0]
            elif i == 1:
                child_1 = parent_2[1]
            elif i == 2:
                child_2 = parent_2[2]
            elif i == 3:
                child_3 = parent_2[3]
            elif i == 4:
                child_4 = parent_2[4]
            elif i == 5:
                child_5 = parent_2[5]
        if (child_0,child_1,child_2,child_3,child_4,child_5) in new_gen_set:
            continue
        if random.random() <= mutation_rate:
            random_location = random.randint(0,5)
            random_add = random.random()/10
            if random.random() >= 0.5:
                random_add *= -1
            if random_location == 0:
                child_0 = abs(child_0+random_add)
            elif random_location == 1:
                child_1 = abs(child_1+random_add)
            elif random_location == 2:
                child_2 = abs(child_2+random_add)
            elif random_location == 3:
                child_3 = abs(child_3+random_add*3)
            elif random_location == 4:
                child_4 = abs(child_4+random_add*3)
            elif random_location == 5:
                child_5 = abs(child_5+random_add*3)
        child = (child_0,child_1,child_2,child_3,child_4,child_5)
        if child in new_gen_set:
            continue
        new_gen_list.append((child,fitness_function(child)))
        new_gen_set.add(child)
    new_gen_list = sorted(new_gen_list,key=lambda x:x[1],reverse=True)
    return new_gen_list
    # print("generation",gen,":",new_gen_list[0])
    # print()
    # create_new_generation(new_gen_list,gen+1)
# new_or_old = input("Type 'N' to start a new genetic process or 'S' to load a saved genetic process: ")
# if new_or_old == "N":
#     print("Creating new genetic process...")
#     gen_list = create_initial_pop()
#     gen = 1
#     print("Created sucessfully.")
#     print("Best Strategy:",gen_list[0][0])
#     print("Best Score:",gen_list[0][1])
#     total = 0
#     for i in range(0,len(gen_list)):
#         total+=gen_list[i][1]
#     print("Average Score:",total/len(gen_list))    
#     while(True):
#         print()
#         play_continue_save = input("Type 'P' to watch the best generation play, 'C' to continue the genetic process, or 'S' to save the current genetic process: ")
#         if play_continue_save == "P":
#             print("Playing...")
#             play_and_display_game(gen_list[0][0])
#             print("Game ended.")
#         elif play_continue_save == "C":
#             print("Continuing genetic process...")
#             gen_list = create_new_generation(gen_list,gen)
#             total = 0
#             print("Best Strategy:",gen_list[0][0])
#             print("Best Score:",gen_list[0][1])
#             for i in range(0,len(gen_list)):
#                 total+=gen_list[i][1]
#             print("Average Score:",total/len(gen_list))
#         elif play_continue_save == "S":
#             print("Saving current genetic process...")
#             with open("saved_tetris_genetic.txt","w") as f:
#                 original_stdout = sys.stdout
#                 sys.stdout = f
#                 print("GENERATION:",gen)
#                 for i in range(0,len(gen_list)):
#                     print("strategy " + str(i+1) + ":",gen_list[i])
#                 sys.stdout = original_stdout
#                 print("Saved succesfully.")
#                 exit()
# elif new_or_old == "S":
#     print("Loading saved genetic process...")
#     gen_list = []
#     with open("saved_tetris_genetic.txt","r") as f:
#         for line in f:
#             if line.count("GENERATION: ") > 0:
#                 gen = int(line[line.find(":")+1:])
#             else:
#                 line = line[line.find(":")+4:len(line)-1]
#                 s1 = float(line[:line.find(",")])
#                 line = line[line.find(",")+2:]
#                 s2 = float(line[:line.find(",")])
#                 line = line[line.find(",")+2:]
#                 s3 = float(line[:line.find(",")])
#                 line = line[line.find(",")+2:]
#                 s4 = float(line[:line.find(",")])
#                 line = line[line.find(",")+2:]
#                 s5 = float(line[:line.find(",")])
#                 line = line[line.find(",")+2:]
#                 s6 = float(line[:line.find(")")])
#                 line = line[line.find(")")+3:]
#                 strategy = (s1,s2,s3,s4,s5,s6)
#                 score = float(line[:line.find(")")])
#                 gen_list.append((strategy,score))
#     total = 0
#     print("Loaded sucessfully.")
#     print("Best Strategy:",gen_list[0][0])
#     print("Best Score:",gen_list[0][1])
#     for i in range(0,len(gen_list)):
#         total+=gen_list[i][1]
#     print("Average Score:",total/len(gen_list))
#     while(True):
#         print()
#         play_continue_save = input("Type 'P' to watch the best generation play, 'C' to continue the genetic process, or 'S' to save the current genetic process: ")
#         if play_continue_save == "P":
#             print("Playing...")
#             play_and_display_game(gen_list[0][0])
#             print("Game ended.")
#         elif play_continue_save == "C":
#             print("Continuing genetic process...")
#             gen_list = create_new_generation(gen_list,gen)
#             total = 0
#             print("Best Strategy:",gen_list[0][0])
#             print("Best Score:",gen_list[0][1])
#             for i in range(0,len(gen_list)):
#                 total+=gen_list[i][1]
#             print("Average Score:",total/len(gen_list))
#         elif play_continue_save == "S":
#             print("Saving current genetic process...")
#             with open("saved_tetris_genetic.txt","w") as f:
#                 original_stdout = sys.stdout
#                 sys.stdout = f
#                 print("GENERATION:",gen)
#                 total = 0
#                 for i in range(0,len(gen_list)):
#                     print("strategy " + str(i+1) + ":",gen_list[i])
#                     total += gen_list[i][1]
#                 sys.stdout = original_stdout
#                 print("Saved succesfully.")
#                 exit()
#         else:
#             max_score = 0
#             while(True):
#                 cur_score = play_game(gen_list[0][0])
#                 max_score = max(max_score,cur_score)
#                 print("Score:",cur_score)
#                 print("Max Score:",max_score)
#                 print()
#         print()

#  #highscore 310,360 

def button(request):
    return render(request,'homepage.hbs')

def new_button(request):
    # print("hi")
    print("Creating new genetic process...")
    gen_list = create_initial_pop()
    gen = 0
    print("Created sucessfully.")
    print("Best Strategy:",gen_list[0][0])
    print("Best Score:",gen_list[0][1])
    total = 0
    for i in range(0,len(gen_list)):
        total+=gen_list[i][1]
    print("Average Score:",total/len(gen_list))
    print("Saving current genetic process...")
    with open("saved_tetris_genetic.txt","w") as f:
        original_stdout = sys.stdout
        sys.stdout = f
        print("GENERATION:",gen)
        total = 0
        for i in range(0,len(gen_list)):
            print("strategy " + str(i+1) + ":",gen_list[i])
            total += gen_list[i][1]
        sys.stdout = original_stdout
        print("Saved succesfully.")
    return render(request,'homepage.hbs',{'generation':gen,'beststrategy':gen_list[0][0],'highscore':gen_list[0][1],'averagescore':total/len(gen_list)})
    # return render(request,'python-test.hbs',{'beststrategy':0,'highscore':1,'averagescore':2})

def continue_button(request):
    gen_list = []
    with open("saved_tetris_genetic.txt","r") as f:
        for line in f:
            if line.count("GENERATION: ") > 0:
                gen = int(line[line.find(":")+1:])
            else:
                line = line[line.find(":")+4:len(line)-1]
                s1 = float(line[:line.find(",")])
                line = line[line.find(",")+2:]
                s2 = float(line[:line.find(",")])
                line = line[line.find(",")+2:]
                s3 = float(line[:line.find(",")])
                line = line[line.find(",")+2:]
                s4 = float(line[:line.find(",")])
                line = line[line.find(",")+2:]
                s5 = float(line[:line.find(",")])
                line = line[line.find(",")+2:]
                s6 = float(line[:line.find(")")])
                line = line[line.find(")")+3:]
                strategy = (s1,s2,s3,s4,s5,s6)
                score = float(line[:line.find(")")])
                gen_list.append((strategy,score))
    total = 0
    gen+=1
    print("Loaded sucessfully.")
    print("Best Strategy:",gen_list[0][0])
    print("Best Score:",gen_list[0][1])
    for i in range(0,len(gen_list)):
        total+=gen_list[i][1]
    print("Average Score:",total/len(gen_list))
    print("Continuing genetic process...")
    gen_list = create_new_generation(gen_list,gen)
    total = 0
    print("Best Strategy:",gen_list[0][0])
    print("Best Score:",gen_list[0][1])
    for i in range(0,len(gen_list)):
        total+=gen_list[i][1]
    print("Average Score:",total/len(gen_list))
    print("Saving current genetic process...")
    with open("saved_tetris_genetic.txt","w") as f:
        original_stdout = sys.stdout
        sys.stdout = f
        print("GENERATION:",gen)
        total = 0
        for i in range(0,len(gen_list)):
            print("strategy " + str(i+1) + ":",gen_list[i])
            total += gen_list[i][1]
        sys.stdout = original_stdout
        print("Saved succesfully.")
    return render(request,'homepage.hbs',{'generation':gen,'beststrategy':gen_list[0][0],'highscore':gen_list[0][1],'averagescore':total/len(gen_list)})
    # return render(request,'python-test.hbs',{'beststrategy':0,'highscore':1,'averagescore':2})

def play_button(request):
    gen_list = []
    gen = 0
    with open("saved_tetris_genetic.txt","r") as f:
        for line in f:
            if line.count("GENERATION: ") > 0:
                gen = int(line[line.find(":")+1:])
            else:
                line = line[line.find(":")+4:len(line)-1]
                s1 = float(line[:line.find(",")])
                line = line[line.find(",")+2:]
                s2 = float(line[:line.find(",")])
                line = line[line.find(",")+2:]
                s3 = float(line[:line.find(",")])
                line = line[line.find(",")+2:]
                s4 = float(line[:line.find(",")])
                line = line[line.find(",")+2:]
                s5 = float(line[:line.find(",")])
                line = line[line.find(",")+2:]
                s6 = float(line[:line.find(")")])
                line = line[line.find(")")+3:]
                strategy = (s1,s2,s3,s4,s5,s6)
                score = float(line[:line.find(")")])
                gen_list.append((strategy,score))
    total = 0
    print("Loaded sucessfully.")
    print("Best Strategy:",gen_list[0][0])
    print("Best Score:",gen_list[0][1])
    for i in range(0,len(gen_list)):
        total+=gen_list[i][1]
    print("Average Score:",total/len(gen_list))
    print("Playing...")
    moves = []
    board = make_new_board()
    points = 0
    game_over = False
    while not game_over:
        possible_boards = []
        i = random.randint(0,len(pieces_list)-1)
        for piece in pieces_list[i]:
            for w in range(0,10):
                poss_board,poss_points = place_piece(piece, w, board)
                if poss_board != "GAME OVER" and poss_board != "INVALID":
                    poss_score = get_heuristic(poss_board, strategy)
                    possible_boards.append((poss_board,poss_score,poss_points))
        if len(possible_boards) == 0:
            game_over = True
        else:
            possible_boards = sorted(possible_boards,key = lambda x:x[1])
            # print(possible_boards[0][1])
            board = possible_boards[0][0]
            # display_board(board)
            points += possible_boards[0][2]
        # print("Current Board:","\n")
        moves.append((display_board(board),points))
        # print("Current Score:",points,"\n")
        # time.sleep(0.5)
    print("Final score:",points)
    # print(moves[0][0])
    return render(request,'homepage.hbs',{'moves':moves,'generation':gen,'score':points,'beststrategy':gen_list[0][0],'highscore':gen_list[0][1],'averagescore':total/len(gen_list)})