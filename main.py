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
    
    




# CONTINUE HERE - Now that the official Stockfish 13 release is being used for the exe,
# there seems to no longer be the problem with the best move not match the first move
# of the top PV. Test further by outputting the lines in get_top_moves to ensure
# this is always the case. Also, test if the evaluation equals the evaluation of the
# top PV (it should). If this is all so, then great.    

from functools import cmp_to_key
from models import Stockfish

#stockfish = Stockfish(path = r"C:\Users\johnd\Documents\Fun Coding Projects\Stockfish Guider\stockfish-10-win\Windows\stockfish_10_x64.exe",
#                      depth = 20, parameters = {"MultiPV": 3, "Threads": 4})

stockfish13 = None

class Node:
    
    def __init__(self, parent_node, FEN, search_depth, node_depth, last_move):
        global stockfish13
        
        if node_depth > search_depth:
            raise ValueError("node_depth > search_depth")
        
        self.children = [] # CONTINUE HERE - consider maybe changing to a dictionary?
        self.evaluation = None
        self.white_to_move = is_whites_turn(FEN)
        self.parent_node = parent_node
        self.FEN = FEN
        self.search_depth = search_depth
        self.node_depth = node_depth
        self.last_move = last_move
        
        # CONTINUE HERE - use stockfish instance to get dict of dicts.
        # Then create each child node and add it to the self.children list,
        # and then get each of them to search. Or don't.
        
        stockfish13.set_fen_position(FEN)
        parameters = stockfish13.get_parameters()
        self.PVs = stockfish13.get_top_moves(int(parameters["MultiPV"]))
        
        # self.PVs is a dictionary with key-dictionary pairs (see what's returned
        # from get_top_moves in models.py).
        
        # CONTINUE HERE - also stop the search and declare this node a leaf node
        # if the evaluation is very big, where it's way past the goal evaluation. 
        # On the topic of this, you should get the goal evaluation from the user 
        # and pass it in to the constructor.
        
        # CONTINUE HERE - Also account for cases where self.PVs is None, due to
        # there being no moves in the position. Will have to get the evaluation some
        # other way.
        
        if node_depth == search_depth:
            # At a leaf node in the tree.
            self.evaluation = self.PVs["1"]["Centipawn"]
            # CONTINUE HERE - Think about whether this is the best way to get the
            # evaluation (i.e., the eval of the top PV). Another option is getting
            # the direct evaluation of the current position... don't know which is
            # better.
            # Check if it even makes any difference... shouldn't the evaluation of 
            # a position be equal to the evaluation of its top PV?
        else:
            current_PV_num = 1
            while (self.PVs.get(str(current_PV_num), None) != None):
                new_move = self.PVs.get(str(current_PV_num))["First move"]
                new_FEN = make_move(self.FEN, new_move)
                child_node = Node(self, new_FEN, search_depth, node_depth + 1, new_move)
                # Note that the self arg above will be the parent_node param
                # for the child_node.
                self.children.append(child_node)
                self.children = sorted(self.children, key=cmp_to_key(self.compare_nodes))
                if (self.evaluation == None or
                    (self.white_to_move and child_node.evaluation > self.evaluation) or
                    (not(self.white_to_move) and child_node.evaluation < self.evaluation)):
                        self.evaluation = child_node.evaluation
                current_PV_num += 1
    
    # CONTINUE HERE - After writing make_move, the above code should be
    # able to guide stockfish ahead. In main, the root node is now
    # able to print an evaluation it gets after all the guiding.
    # But in order to ensure that stockfish is being guided properly, and output
    # of the variations (with the evaluations of the leaf nodes as annotations)
    # will need to be provided.
    # After doing some more testing with this, and perhaps writing a function to
    # do the aforementioned printing of variations, continue by working on the
    # CONTINUE HERE spots above for improving some details.
    
    def compare_nodes(self, first, second):
        if first.evaluation == None or second.evaluation == None:
            raise ValueError("first.evaluation or second.evaluation has no value.")
        return (second.evaluation - first.evaluation) * (1 if self.white_to_move else -1)

def make_move(old_FEN, move):
    # CONTINUE HERE - return the FEN that results from making move on old_FEN.
    # It looks like models.py doesn't have a function to handle this.
    
    # Among other things, you will have to flip whose move it is. Also, to be
    # on the safe side, don't modify old_FEN (not sure whether it is immutable).
    
    # Idea: create a 2-D vector storing chars representing the pieces (e.g., P and p for white and black pawns).
    # Also, for the move being made, ensure that it matches the side whose turn it is to move.
    
    # After completing this function, then you can truly use the output tree
    # to test if the tree is correct. Since now it will flip whose move it is
    # on each new node, as well as update the position with a move.
    
    # PLACEHOLDER:
    return (old_FEN.replace(' w ', ' b ', 1) if is_whites_turn(old_FEN) else old_FEN.replace(' b ', ' w ', 1))

def output_tree(node):
    # CONTINUE HERE - Nothing to do in this function for now. But after writing the make_move function,
    # run the program and call this function to check the tree. So far it looks good, with the make_move
    # simply flipping whose turn it is in the FEN (but not making any actual moves). The root node's
    # evaluation is based off the top moves for both sides, which is good.
    
    print("node evaluation: " + str(node.evaluation))
    if (node.children != []):
        print("Child nodes:")
        counter = 1
        for child_node in node.children:
            print(str(counter) + ". Node move: " + child_node.last_move + ". Evaluation: " + str(child_node.evaluation))
            counter += 1
        print("To inspect a node in the above list, enter its corresponding number:")
    if (node.parent_node != None):
        print("Or, enter P to return to the parent node.")
    print("Or, enter Q to quit.")
    while True:
        user_input = input()
        if user_input == "q" or user_input == "Q":
            break
        elif user_input == "p" or user_input == "P":
            if (node.parent_node != None):
                output_tree(node.parent_node)
                break
            else:
                print("This node is the root node, please try again:")
        elif (user_input.isdigit()):
            user_input_num_form = int(user_input)
            if user_input_num_form <= len(node.children) and user_input_num_form > 0:
                output_tree(node.children[user_input_num_form - 1])
                break
            else:
                print("The number you entered is out of bounds, please try again:")
        else:
            print("You did not enter P, Q, or a valid number, please try again:")

def is_whites_turn(FEN):
    for i in range(len(FEN)):
        if i < len(FEN) - 2 and FEN[i] == ' ' and FEN[i+2] == ' ':
            if FEN[i+1] == 'w':
                return True
            elif FEN[i+1] == 'b':
                return False
    raise ValueError("The FEN param for is_whites_turn does not say whose turn it is.")
    
def main():
    global stockfish13
    
    FEN = input("Enter the FEN for the position: ")
    search_depth = int(input("Enter the max depth to search in the tree: "))
    multiPV_num = int(input("Enter the MultiPV number: "))
    stockfish_depth = int(input("Enter the search depth for SF: "))
    
    stockfish13 = Stockfish(path = r"C:\Users\johnd\Documents\Fun Coding Projects\Stockfish Guider\stockfish_13_win_x64_bmi2.exe",
                            depth = stockfish_depth, parameters = {"Threads": 4, "MultiPV": multiPV_num})
    
    root_node = Node(None, FEN, search_depth, 0, None)
    # CONTINUE HERE - after all the calculations are done, output the data for
    # the root node. Could also traverse the whole tree and generate notation
    # that can be copied into chessbase (where the data for each position is
    # ideally in the form of annotation).
    print(root_node.white_to_move)
    print(root_node.evaluation)
    
    user_input = input("To see the search tree, enter tree: ")
    if user_input == "tree":
        output_tree(root_node)
    
    """
    print("Top 2 moves:\n")
    print (stockfish13Mod.get_top_moves(2))
    print("\n\nTop 3 moves:\n")
    print (stockfish13Mod.get_top_moves(3))
    print ("\n\n")
    
    
    
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