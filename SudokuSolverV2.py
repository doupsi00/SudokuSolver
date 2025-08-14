import heapq
import copy
from itertools import count

class SudokuSolverV2:
    def __init__(self, board):
        self.board = board

    def solve(self):
        # Quick sanity: initial board must not violate rules
        if not self.is_valid_board(self.board):
            return None

        temp = copy.deepcopy(self.board)
        heap = []
        tie = count()  # tie-breaker so heap never compares boards
        g0 = 0
        h0 = self.heuristic(self.board)
        heapq.heappush(heap, (g0 + h0, g0, next(tie), self.board))

        while heap:
            f, g, _, curr_board = heapq.heappop(heap)

            if self.is_goal(curr_board):
                # Full board; return only if consistent with givens and valid
                return curr_board if self.checker(temp, curr_board) else None

            pick = self.select_mrv_cell(curr_board)
            if pick is None:
                # No empty cells but goal failed (invalid placement) -> skip
                continue

            i, j, candidates = pick
            # If no candidates, this branch is a dead end (implicit prune)
            for num in candidates:
                new_board = copy.deepcopy(curr_board)
                new_board[i][j] = num
                # PRUNE: skip states that violate row/col/box constraints
                if not self.is_valid_board(new_board):
                    continue
                h = self.heuristic(new_board)
                heapq.heappush(heap, (g + 1 + h, g + 1, next(tie), new_board))
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
                    if num_options == 0:
                        # Immediate dead end
                        return (i, j, [])
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

        if best_cell is None:
            return None
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
        used = set(board[row])
        used.update(board[i][col] for i in range(9))
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                used.add(board[i][j])
        return [n for n in range(1, 10) if n not in used]

    def heuristic(self, board):
        # Sum of domain sizes for all empty cells
        total = 0
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    total += len(self.get_candidates(board, i, j))
        return total

    def is_goal(self, board):
        return all(all(cell != 0 for cell in row) for row in board)

    def is_valid_board(self, board):
        # Rows & cols (ignore zeros)
        for i in range(9):
            row_vals = [x for x in board[i] if x != 0]
            if len(row_vals) != len(set(row_vals)):
                return False
            col_vals = [board[r][i] for r in range(9) if board[r][i] != 0]
            if len(col_vals) != len(set(col_vals)):
                return False
        # 3x3 boxes
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                box = []
                for r in range(br, br + 3):
                    for c in range(bc, bc + 3):
                        v = board[r][c]
                        if v != 0:
                            box.append(v)
                if len(box) != len(set(box)):
                    return False
        return True

    # final checker — consistent with givens + full validity
    def checker(self, board, solved):
        row_used = [set() for _ in range(9)]
        col_used = [set() for _ in range(9)]
        box_used = [set() for _ in range(9)]
        for i in range(9):
            for j in range(9):
                curr = solved[i][j]
                if curr < 1 or curr > 9:
                    return False
                if curr in row_used[i] or curr in col_used[j] or curr in box_used[3*(i//3)+j//3]:
                    return False
                if board[i][j] != 0 and board[i][j] != solved[i][j]:
                    return False
                row_used[i].add(curr)
                col_used[j].add(curr)
                box_used[3*(i//3)+j//3].add(curr)
        return True


