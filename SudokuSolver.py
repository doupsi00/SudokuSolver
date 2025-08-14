import copy
import time

class SudokuSolver:
    def __init__(self, board):
        self.board = board
        self.possiblePerRow = [set([1,2,3,4,5,6,7,8,9]) for i in range(9)]
        self.possiblePerCol = [set([1,2,3,4,5,6,7,8,9]) for i in range(9)]
        self.possiblePerBox = [set([1,2,3,4,5,6,7,8,9]) for i in range(9)]
        for i in range(9):
            for j in range(9):
                if board[i][j]!=0:
                    if board[i][j] in self.possiblePerRow[i]:
                        self.possiblePerRow[i].discard(board[i][j])
                    if board[i][j] in self.possiblePerCol[j]:
                        self.possiblePerCol[j].discard(board[i][j])
                    if board[i][j] in self.possiblePerBox[3*(i//3)+j//3]:
                        self.possiblePerBox[3*(i//3)+j//3].discard(board[i][j])

    def solve(self):
        temp = copy.deepcopy(self.board)
        self.backtrack()
        if self.checker(temp, self.board): return self.board  # board is updated in place

    def backtrack(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    box_idx = 3 * (i // 3) + (j // 3)
                    # Find intersection of all constraints
                    candidates = (
                            self.possiblePerRow[i] &
                            self.possiblePerCol[j] &
                            self.possiblePerBox[box_idx]
                    )
                    for num in candidates:
                        # Place num
                        self.board[i][j] = num
                        self.possiblePerRow[i].remove(num)
                        self.possiblePerCol[j].remove(num)
                        self.possiblePerBox[box_idx].remove(num)

                        if self.backtrack():
                            return True

                        # Undo placement (backtrack)
                        self.board[i][j] = 0
                        self.possiblePerRow[i].add(num)
                        self.possiblePerCol[j].add(num)
                        self.possiblePerBox[box_idx].add(num)

                    return False
        return True

    # function to check validity of solution
    def checker(self, board, solved):
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
sudoku = SudokuSolver(board)
solved = sudoku.solve()
print(time.time()-curr)
print(checker(board2, solved))
for i in range(9):
    print(solved[i])
