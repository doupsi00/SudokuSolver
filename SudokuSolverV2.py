import heapq
import copy
import time

class SudokuSolverV2:
    def __init__(self, board):
        self.board = board

    def solve(self):
        heap = []
        initial_state = (self.heuristic(self.board), 0, self.board)
        heapq.heappush(heap, initial_state)

        while heap:
            f, g, curr_board = heapq.heappop(heap)
            if self.is_goal(curr_board):
                return curr_board

            i, j, candidates = self.select_mrv_cell(curr_board)
            for num in candidates:
                new_board = copy.deepcopy(curr_board)
                new_board[i][j] = num
                h = self.heuristic(new_board)
                heapq.heappush(heap, (g + 1 + h, g + 1, new_board))
        return None

    def select_mrv_cell(self, board):
        min_options = 10
        best_cell = None
        best_neighbors = -1
        best_candidates = []

        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    candidates = self.get_candidates(board, i, j)
                    num_options = len(candidates)

                    if num_options < min_options:
                        min_options = num_options
                        best_cell = (i, j)
                        best_candidates = candidates
                        best_neighbors = self.count_unfilled_neighbors(board, i, j)
                    elif num_options == min_options:
                        neighbors = self.count_unfilled_neighbors(board, i, j)
                        if neighbors > best_neighbors:
                            best_cell = (i, j)
                            best_candidates = candidates
                            best_neighbors = neighbors
        return (*best_cell, best_candidates)

    def count_unfilled_neighbors(self, board, row, col):
        count = 0
        for k in range(9):
            if board[row][k] == 0 and k != col:
                count += 1
            if board[k][col] == 0 and k != row:
                count += 1
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == 0 and (i, j) != (row, col):
                    count += 1
        return count

    def get_candidates(self, board, row, col):
        used = set()
        used.update(board[row])
        used.update(board[i][col] for i in range(9))
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                used.add(board[i][j])
        return [n for n in range(1, 10) if n not in used]

    def heuristic(self, board):
        # Sum of the number of legal values for all empty cells
        total = 0
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    total += len(self.get_candidates(board, i, j))
        return total

    def is_goal(self, board):
        return all(all(cell != 0 for cell in row) for row in board)

# function to check validity of solution
def checker(board, solved):
    row_used = [set() for i in range(9)]
    col_used = [set() for i in range(9)]
    box_used = [set() for i in range(9)]
    for i in range(9):
        for j in range(9):
            curr = solved[i][j]
            if curr in row_used[i]:
                print(f"Repeat in row {i}")
                return False
            if curr in col_used[j]:
                print(f"Repeat in col {j}")
                return False
            if curr in box_used[3*(i//3)+j//3]:
                print(f"Repeat in box {3*(i//3)+j//3}")
                return False
            if board[i][j] != 0 and board[i][j] != solved[i][j]:
                print(f"Diff value in [{i},{j}]")
                return False
            row_used[i].add(curr)
            col_used[j].add(curr)
            box_used[3*(i//3)+j//3].add(curr)
    return True

board = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
]


board2 = copy.deepcopy(board)

curr = time.time()
sudoku = SudokuSolverV2(board)
solved = sudoku.solve()
print(time.time()-curr)
print(checker(board2, solved))
print(solved)

