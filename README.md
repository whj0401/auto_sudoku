# auto_sudoku

input sudoku in string
and return the solution

though this version cannot recursively solve problem, it can solve most sudoku problem quickly.

It's easy to implement a recursive-solution(RS), enum type TRY is used for RS.
Just save the current status of Sudoku, and copy a new Sudoku Object, setting cell in CONFIRM or TRY status to STATIC,
then run work() function of new Sudoku.

I'll implement RS as soon as I can
