## How to Run ??

Just Run the single python file changeHuristic.py after installing all the used packages.

## How agent  finds the best move to play ??
It uses Mini-Max   Algorithm with  Alpha–beta pruning to find the next move.

### how well does it play  ??
It depends on the depth of the search .My computer allowed only till depth 5  and it was doing pretty well on depth 5.
### How to make agent smarter??
Just increase the search depth by changing the mxDep variable.


## How Gui was Created ??
 ### Board 
 It is made of 64 (because size of the board is 8X8)  rectangles on canvas.
 
 ### Pieces
 Every piece is oval with an outer (to indticate  the possible moves for human player)  and a  text area ( to identify the king) 
 
 ## Used Libraries 
- numpy
- tkinter
- queue
- threading
- time 
- random
