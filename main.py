## TODO:

# Modify the stockfish code in search.cpp to do sync_cout << "secondbestmove " << ...
# for the second best move. Could also do this for the third best. Make sure to check that
# there are at least 2-3 moves.
    # For the exe you end up using (generated after modifying the stockfish code),
    # include the entire stockfish repository in this project. Your modifications to the code
    # should be made available, if including the exe in the project.

# Clone the python stockfish and add code that deals with getting the second and third best
# moves, identifying them based off the third "secondbestmove" and "thirdbestmove". Since
# you'll be modifying the code, the python stockfish stuff will be added to this project,
# and can be used that way (instead of having to be used with the pip install currently).
    # Note that to get the second best move, MultiPV must be at least 2. To get the third best, MultiPV must
    # be at least 3. Etc.    
    
    # Not sure if you'll have to do pip uninstall to make sure you use the code you will
    # clone for Python Stockfish (instead of using what pip install provides).
    
## IDEAS:
    
# The amount of time to let Stockfish think on a normal position in the calculation
# tree (e.g., depth 28) should differ from the amount of time it thinks when in a final
# / leaf position (at least when in this position the evaluation is close to the borderline
# of what is acceptable). When Stockfish is just calculating in a normal position, all it's
# doing is figuring out whether the evaluation is very big (so to stop there), or to find
# the likely best moves to continue on with being guided through the search tree. So having
# a completely accurate evaluation isn't as important as it is in a final/leaf position
# of the search tree, since that evaluation is used for minimax.
    
# If a move from the opponent (somewhere in the search tree) gives the goal evaluation, or
# at least a fair amount better than it, no need to continue searching there. The app can just
# print the evlauation, and then I can check it out myself in my own analysis. The main thing for
# the app to do is analyse lines that seriously challenge the goal evaluation.
    
# The user can specify the normal depth to search to, and the depth to search to when at a leaf node.
    
# Use an SQL database to store engine evaluations in positions. This can allow the app to
# stop running at some point, and then run again later on (the search and evaluation of those
# positions will be near instant, since it will just use the DB).
    
# The user can also input the threshold to not analyse a move if it's below the goal evaluation
# by some amount.
    
# Since the app mainly looks at moves from the player that is not dramatically above the
# goal evaluation, and movesf from the opponent that aren't at the evlauation or within it,
# the branching factor shouldn't be too bad? The app doesn't need to definitvely prove that a
# line gives the goal evaluation. It should analyse similar to how you do - looking at the main lines,
# not analysing a line that is most likely irrelevant.
    
# If the app reaches the gaol evaluation at some point in the search, decide whether it should stop there
# or continue searching further (to ensure the gaol evaluation holds). This could be a parameter
# the user also specifies.
    
# If the app can't find a line giving the gaol evaluation, it should give line(s) that is the
# best it can do. Still may be useful.
    
# A good test for the app would be for it to try to find a line giving a goal evaluation in some line
# that you have trouble with. E.g., the ...Bg4 classical line where Black meets f4 with ...Ned7 instead of ...Bxe2.
# For that, the user would set the depth parameter to be pretty high, since the goal is to fine some ~0.40 evaluation
# that holds going quite deeply.
    
from models import Stockfish

#stockfish = Stockfish(path = r"C:\Users\johnd\Documents\Fun Coding Projects\Stockfish Guider\stockfish-10-win\Windows\stockfish_10_x64.exe",
#                      depth = 20, parameters = {"MultiPV": 3, "Threads": 4})

stockfish13 = Stockfish(path = r"C:\Users\johnd\Documents\Fun Coding Projects\Stockfish Guider\stockfish13.exe",
                        depth = 24, parameters = {"Threads": 4})

stockfish13Mod = Stockfish(path = r"C:\Users\johnd\Documents\Fun Coding Projects\Stockfish Guider\stockfish13OutputModification.exe",
                           depth = 24, parameters = {"Threads": 4, "MultiPV": 3})

class Node:
    
    def __init__(self, white_to_move, parent_node, PVs):
        self.children = None
        self.evaluation = None
        self.white_to_move = white_to_move
        self.parent_node = parent_node
        self.PVs = PVs
    # PVs will be a dictionary with key-dictionary pairs (see what's returned
    # from get_top_moves in models.py).
    
    def add_child_node(self, child_node):
        self.children.append(child_node)
        if (self.evaluation == None or
            (self.white_to_move and child_node.evaluation > self.evaluation) or
            (self.black_to_move and child_node.evaluation < self.evaluation)):
              self.evaluation = child_node.evaluation

def main():
    
    #print (stockfish13Mod.get_top_moves(0))
    #print (stockfish13Mod.get_top_moves(1))
    
    print("Top 2 moves:\n")
    print (stockfish13Mod.get_top_moves(2))
    print("\n\nTop 3 moves:\n")
    print (stockfish13Mod.get_top_moves(3))
    print ("\n\n")
    """
    print("Hi")
    stockfish13.set_fen_position("rnbqkbnr/pppp1ppp/8/4p3/4PP2/8/PPPP2PP/RNBQKBNR b KQkq - 0 2")
    stockfish13Mod.set_fen_position("rnbqkbnr/pppp1ppp/8/4p3/4PP2/8/PPPP2PP/RNBQKBNR b KQkq - 0 2")
    print("Stockfish 13:")
    print(stockfish13.get_evaluation())
    print(stockfish13.get_best_move())
    print("Stockfish 13 Mod:")
    print(stockfish13Mod.get_evaluation())
    print(stockfish13Mod.get_best_move()) # Outputs the second best move, as hoped.
    """
if __name__ == '__main__':
    main()