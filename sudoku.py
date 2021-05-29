# a sudoku solver
import random
from pprint import pprint


def find_next_empty_square(puzzle):

    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r, c

    return None, None


def is_valid(guess, row, col, puzzle):
    # check row
    if guess in puzzle[row]:
        return False

    # check column
    col_values = [puzzle[r][col] for r in range(9)]
    if guess in col_values:
        return False

    # check box
    box_row_start = (row // 3) * 3  # 2 // 3 = 0, 5 // 3 = 1
    box_col_start = (col // 3) * 3

    for r in range(box_row_start, box_row_start + 3):
        for c in range(box_col_start, box_col_start + 3):
            if puzzle[r][c] == guess:
                return False

    return True


def solve_sudoku(puzzle):
    # solving suduko using recursion and backtracking

    # step 1 find an empty square
    row, col = find_next_empty_square(puzzle)

    if row == None:
        return True

    # step 2 guess a number for that square
    # if it is valid place it in the puzzle
    for guess in range(1, 10):  # guess could only be 1-9
        if is_valid(guess, row, col, puzzle):
            puzzle[row][col] = guess

            # step 3 repeat step 1 & 2 until the sudoku gets solved
            if solve_sudoku(puzzle):
                return True

            #  step 4 if a sudoku is unsolvable in a certain path,
            #  reverse the changes made and continue to the other guess
            puzzle[row][col] = -1

    # step 5 if the sudoku is unsolvable using all paths return False
    return False


def invert_vertically(sudoku):
    return sudoku[::-1]


def invert_horizontally(sudoku):
    sudoku = list(sudoku)  # copy sudoku
    for i in range(9):
        sudoku[i] = sudoku[i][::-1]

    return sudoku


def rand_invert(sudoku):
    rand_invert = random.randint(1, 4)
    if rand_invert == 1:
        return sudoku
    elif rand_invert == 2:
        return invert_horizontally(sudoku)
    elif rand_invert == 3:
        return invert_vertically(sudoku)
    else:
        return invert_vertically(invert_horizontally(sudoku))


# solvable sudoku generator
def create_solvable_sudoku(num_givens=17):
    # because for one solution sudokus there should be atleast 17 visible squares
    # the generated sudoku can have multiple solutions

    num_givens = min(17, num_givens)  # number of squares that are visible

    # create an empty sudoku
    sudoku = [[-1 for j in range(9)] for i in range(9)]

    # fill the diagonal with valid values

    for i in range(9):
        rand = random.randint(1, 9)
        if is_valid(rand, i, i, sudoku):
            sudoku[i][i] = rand

    # solve the sudoku and invert it if needed
    solve_sudoku(sudoku)
    random_sudoku = rand_invert(sudoku)

    # choose the random givens that are visible for solving the sudoku
    sudoku_copy = list(random_sudoku)
    rand_givens = random.choices([i for i in range(81)], k=num_givens)
    for i in range(81):
        if i not in rand_givens:
            row = i // 9
            col = i % 9
            sudoku_copy[row][col] = -1

    return sudoku_copy


if __name__ == "__main__":
    sample_puzzle = [
        [3, 9, -1,   -1, 5, -1,   -1, -1, -1],
        [-1, -1, -1,   2, -1, -1,   -1, -1, 5],
        [-1, -1, -1,   7, 1, 9,   -1, 8, -1],

        [-1, 5, -1,   -1, 6, 8,   -1, -1, -1],
        [2, -1, 6,   -1, -1, 3,   -1, -1, -1],
        [-1, -1, -1,   -1, -1, -1,   -1, -1, 4],

        [5, -1, -1,   -1, -1, -1,   -1, -1, -1],
        [6, 7, -1,   1, -1, 5,   -1, 4, -1],
        [1, -1, 9,   -1, -1, -1,   2, -1, -1]
    ]

    print("Manually created puzzle")
    print("-----------------------------------")
    pprint(sample_puzzle)
    solve_sudoku(sample_puzzle)
    print()
    print("Manually created puzzle solved")
    print("-----------------------------------")
    pprint(sample_puzzle)
    print()

    puzzle = create_solvable_sudoku()
    print("Computer generated puzzle")
    print("-----------------------------------")
    pprint(puzzle)
    print()
    solve_sudoku(puzzle)
    print("Computer generated puzzle solved")
    print("-----------------------------------")
    pprint(puzzle)
