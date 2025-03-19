# Quoridor logic in Python

## Install

```
pip install pyquoridor
```

## Usage
```python
from pyquoridor.board import Board
from pyquoridor.utils import print_board

board = Board()

# Place fences
board.place_fence(row=0, col=0, orientation='h')
board.place_fence(row=7, col=0, orientation='h')
board.place_fence(row=3, col=2, orientation='v')
board.place_fence(row=1, col=0, orientation='v')

# Move pawn
board.move_pawn(player='white', target_row=1, target_col=4)

# Show board
print_board(board)

"""
   ··· ··· ··· ··· ··· ··· ··· ··· ···
8 :   :   :   :   : b :   :   :   :   :
   ---*--- ··· ··· ··· ··· ··· ··· ···
7 :   :   :   :   :   :   :   :   :   :
   ··· ··· ··· ··· ··· ··· ··· ··· ···
6 :   :   :   :   :   :   :   :   :   :
   ··· ··· ··· ··· ··· ··· ··· ··· ···
5 :   :   :   :   :   :   :   :   :   :
   ··· ··· ··· ··· ··· ··· ··· ··· ···
4 :   :   :   |   :   :   :   :   :   :
   ··· ··· ···*··· ··· ··· ··· ··· ···
3 :   :   :   |   :   :   :   :   :   :
   ··· ··· ··· ··· ··· ··· ··· ··· ···
2 :   |   :   :   :   :   :   :   :   :
   ···*··· ··· ··· ··· ··· ··· ··· ···
1 :   |   :   :   : w :   :   :   :   :
   ---*--- ··· ··· ··· ··· ··· ··· ···
0 :   :   :   :   :   :   :   :   :   :
   ··· ··· ··· ··· ··· ··· ··· ··· ···
    0   1   2   3   4   5   6   7   8 
"""

```

## Exceptions for invalid moves

The logic raises exceptions for:
* Invalid pawn moves, including out-of-board and illegal jumping events (`exceptions.InvalidMove`)
* Invalid fence placements, including out-of-board fences, overlapping fences, and fences that block unique pawn paths (`exceptions.InvalidFence`)
* Moves after game is over (`exceptions.GameOver`)
