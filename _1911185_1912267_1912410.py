import numpy as np


def select_move(cur_state, remain_time):
    valid_moves = cur_state.get_valid_moves
    if cur_state.game_result(cur_state.blocks[valid_moves[0].index_local_board]) != None:
        return np.random.choice(valid_moves)
#     if len(valid_moves) == 81 or len(valid_moves) == 9:
#         return np.random.choice(valid_moves)
    if len(valid_moves) != 0:
        return minimax_ab(cur_state, valid_moves)
    return None

def minimax_ab(cur_state, valid_moves):
    if len(valid_moves)==1:
        return valid_moves[0]
    values=[]
    player=valid_moves[0].value
    for move in valid_moves:
        temp = static_evaluation(cur_state, move)
        values.append(temp)
        if temp == 10 * player:
            return move
    best_value=max(values) if player == 1 else min(values)
    best_index=values.index(best_value)
    print(best_value)

def static_evaluation(cur_state, move):
    cur_board = cur_state.blocks[move.index_local_board]
    player=move.value
    x=move.x
    y=move.y
    move_value=0
    p=move.value #player value
    o=p*-1 #opponent value
    #check row, column, topleft and topright diagonal line
    row_sum_p=0
    row_sum_o=0
    col_sum_p=0
    col_sum_o=0
    if x==y:
        left_fail=0
        left_sum_p=0
        left_sum_o=0
    else:
        left_fail=1
    if x==y:
        right_fail=0
        right_sum_p=0
        right_sum_o=0
    else:
        right_fail=1
    for j in range (3):
        if cur_board[x][j]== p:
            row_sum_p+=1
        if cur_board[x][j]== o:
            row_sum_o+=1
        if cur_board[j][y]== p:
            col_sum_p+=1
        if cur_board[j][y]== o:
            col_sum_o+=1
        if left_fail==0:
            if cur_board[j][j]== p:
                left_sum_p+=1
            if cur_board[j][j]== o:
                left_sum_o+=1
        if right_fail==0:
            if cur_board[j][2-j]== p:
                right_sum_p+=1
            if cur_board[j][2-j]== o:
                right_sum_o+=1
    # immediate win move
    if col_sum_p==2 or row_sum_p==2:
        move_value=10*p
        return move_value
    if left_fail==0:
        if left_sum_p==2:
            move_value=10*p
            return move_value
    if right_fail==0:
        if right_sum_p==2:
            move_value=10*p
            return move_value
    # prevent-opponent-win move
    if col_sum_o==2 or row_sum_o==2:
        move_value=9*p
        return move_value
    if left_fail==0:
        if left_sum_o==2:
            move_value=9*p
            return move_value
    if right_fail==0:
        if right_sum_o==2:
            move_value=9*p
            return move_value
    # chose-center move
    if x==1 and y==1:
        move_value+=2*p
    # normal move
    if col_sum_o == 0:
        move_value+=p
    if row_sum_o == 0:
        move_value+=p
    if left_fail==0:
        if left_sum_o==0:
            move_value+=p
    if right_fail==0:
        if right_sum_o==0:
            move_value+=p
    return move_value



def static_evaluation2(cur_state, move):
    cur_board = cur_state.blocks[move.index_local_board] # Bảng hiện tại
    x = move.x
    y = move.y
    p = move.value #player value
    o = p* -1
    res = 0
    array_o = [0, 0, 0, 0, 0, 0, 0, 0]
    array_p = [0, 0, 0, 0, 0, 0, 0, 0]

    if cur_state.game_result(cur_board) != 0:
        
        for i in range (3):
            for j in range (3):
                if cur_board[i][j] == o:
                    array_o[i] += 1
                    array_o[j + 3] += 1
                    if i == j:
                        array_o[6] += 1
                    if i + j == 2:
                        array_o[7] += 1

                if cur_board[i][j] == p:
                    array_p[i] += 1
                    array_p[j + 3] += 1
                    if i == j:
                        array_p[6] += 1
                    if i + j == 2:
                        array_p[7] += 1

        if array_o[x] == 1 and array_p[x] == 0:
            res += 1
        elif array_o[x] == 2:
            res += 3
        if array_o[y + 3] == 1 and array_p[y + 3] == 0:
            res += 1
        elif array_o[y + 3] == 2:
            res += 3
        if x == y:
            if array_o[6] == 1 and array_p[6] == 0:
                res += 1
            elif array_o[6] == 2:
                res += 3
        if x + y == 2:
            if array_o[7] == 1 and array_p[7] == 0:
                res += 1
            elif array_o[7] == 2:
                res += 3

        if array_o[x] == 0 and array_p[x] == 1:
            res += 1
        elif array_p[x] == 2:
            res += 5
        if array_o[y + 3] == 0 and array_p[y + 3] == 1:
            res += 1
        elif array_p[y + 3] == 2:
            res += 5
        if x == y:
            if array_o[6] == 0 and array_p[6] == 1:
                res += 1
            elif array_p[6] == 2:
                res += 5
        if x + y == 2:
            if array_o[7] == 0 and array_p[7] == 1:
                res += 1
            elif array_p[7] == 2:
                res += 3

        if 3 * x + y == 4:
            res -= 3
            # print(res)
    else: 
        if cur_state.game_result(cur_state.blocks[3 * x + y]) != 0:
            res += 10

    if p == 1:
        return res
    else: return -res
