import numpy as np
import copy

def select_move(cur_state, remain_time):
    valid_moves = cur_state.get_valid_moves
#    if cur_state.game_result(cur_state.blocks[valid_moves[0].index_local_board]) != None:
#        return np.random.choice(valid_moves)
    if len(valid_moves) == 81 or len(valid_moves) == 9:
        return np.random.choice(valid_moves)
    if len(valid_moves) != 0:
        #return minimax_ab(cur_state, valid_moves)
        move, value = minimax(cur_state, 1, 2, 1)
        return move
    return None


def minimax(cur_state, depth, max_depth, turn):
    # print(depth)
    # if len(cur_state.get_valid_moves) == 0:
    #     return None, 0
    if depth == max_depth:
        valid_moves1 = cur_state.get_valid_moves
        best_value = static_evaluation2(cur_state, valid_moves1[0], turn)
        best_move = valid_moves1[0]
        # print('bestvalue2', best_move.value)

        for i in range(1, len(valid_moves1)):
            value = static_evaluation2(cur_state, valid_moves1[i], turn)
            # print('turn ', turn)
            if turn == -1:
                if best_value >= value:
                    best_move = valid_moves1[i]
            else:
                if best_value <= value:
                    best_move = valid_moves1[i]
        return best_move, best_value

    
    else:
        valid_moves = cur_state.get_valid_moves
        new_state = copy.deepcopy(cur_state)
        new_state.act_move(valid_moves[0])
        best_move, best_value = minimax(new_state, depth + 1, max_depth, turn*-1)
        # print('bestvalue0', best_move.value)
        res_move = valid_moves[0]
        for i in range(1, len(valid_moves)):
            new_state = copy.deepcopy(cur_state)
            new_state.act_move(valid_moves[i])
            move, value = minimax(new_state, depth + 1, max_depth, turn*-1)
            if turn == -1:
                if best_value >= value:
                    res_move = valid_moves[i]
                    best_move = move
            else:
                if best_value <= value:
                    res_move = valid_moves[i]
                    best_move = move
        # print('turn', turn)
        # print('len', len(valid_moves))

        return res_move, 0
            

def static_evaluation2(cur_state, move, turn):
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

    if p == turn:
        return res
    else: 
        return -res
