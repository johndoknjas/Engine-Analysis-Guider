# IDEAS:
    
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

# For models.py, when setting the Stockfish instance up with a new position, the engine starts a new game
# and then goes to the position. So, this may mean no using the TT as going through the Node search tree.
# Also, SF wouldn't be able to recognize three folds, which could happen at around depth 6 or higher. However,
# this likely isn't a big deal as it will evaluate 0.00 anyway.
    # EDIT - Due to making moves based off the current FEN, SF will be able to use info about the previous
    # FEN to generate the new FEN. E.g., number of full moves that have happened in the game total, the number
    # of plies currently counting towards the 50 move rule. However, it still may not be able to do stuff like use
    # the TT or recognize 3 fold repetitions, as these things aren't embedded in an FEN. But experiment and see
    # if SF has some way to doing this anyway (after all, in chessbase SF can recognize three folds... although
    # maybe chessbase doesn't start a new game with the "ucinewgame" command whenever updating a position).
    




# CONTINUE HERE - Now that the official Stockfish 13 release is being used for the exe,
# there seems to no longer be the problem with the best move not match the first move
# of the top PV. Test further by outputting the lines in get_top_moves to ensure
# this is always the case. Also, test if the evaluation equals the evaluation of the
# top PV (it should). If this is all so, then great.

# It looks like the above is the case, as I've been using the official SF release for a while
# and it's all good. But try to figure out whether/why this was an issue before (checkout earlier commits
# and experiment). If it was due to using a different release (or a version in-between releases), then will 
# this be a problem for anyone using one of these versions of SF? Both for currently avaiable versions
# and versions that could be out in the future.
    # If it is in fact an issue, then maybe look into modifying get_top_moves() to accommodate this?
    # Also, if it's an issue for get_top_moves, then experiment with other functions in models.py to see
    # if there's any issues there as well. But even in this scenario there likely won't be any issue, since
    # the problem in the first place before was the top move's first move not matching the best move SF outputted.

from functools import cmp_to_key
from models import Stockfish

MAX_INTEGER = 1000000000
MIN_INTEGER = -1 * MAX_INTEGER

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
        self.check_PVs_sorted()
        # CONTINUE HERE - An optimization could be to check if this is a leaf node
        # (i.e., if node_depth == search_depth). If so, only get the first top move
        # (or instead just call get_evaluation). The reason is that the search
        # ends here due to this node being a leaf, so you don't need to waste time on multiple PVs.
        # All you need is the direct evaluation from Stockfish at this point.
        
        # self.PVs is a list whose elements are dictionaries (see what's returned
        # from get_top_moves in models.py).
        
        # CONTINUE HERE - also stop the search and declare this node a leaf node
        # if the evaluation is very big, where it's way past the goal evaluation. 
        # On the topic of this, you should get the goal evaluation from the user 
        # and pass it in to the constructor.
        
        if self.PVs == []:
            # There are no moves in this position, so set self.evaluation
            # to the evaluation stockfish directly gives in this position.
            # It will either be a mate or a stalemate.
            evaluation_dict = stockfish13.get_evaluation()
            assert(evaluation_dict["value"] == 0)
            if evaluation_dict["type"] == "mate":
                self.evaluation = MIN_INTEGER if self.white_to_move else MAX_INTEGER
            else:
                assert(evaluation_dict["type"] == "cp")
                self.evaluation = 0
        elif node_depth == search_depth:
            # At a leaf node in the tree.
            if self.PVs[0]["Centipawn"] != None:
                self.evaluation = self.PVs[0]["Centipawn"]
            elif (self.PVs[0]["Mate"] > 0):
                self.evaluation = MAX_INTEGER
            else:
                self.evaluation = MIN_INTEGER
        else:
            for current_PV in self.PVs:
                new_move = current_PV["Move"]
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
    
    def check_PVs_sorted(self):
        if len(self.PVs) <= 1:
            return
        for i in range(1, len(self.PVs)):
            if self.PVs[i]["Mate"] != None:
                assert self.PVs[i-1]["Mate"] != None
            elif self.PVs[i-1]["Mate"] == None:
                if self.white_to_move:
                    assert self.PVs[i-1]["Centipawn"] >= self.PVs[i]["Centipawn"]
                else:
                    assert self.PVs[i-1]["Centipawn"] <= self.PVs[i]["Centipawn"]

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
    
    # CONTINUE HERE - Look at the CONTINUE HERE note in set_position() of models.py. If there's
    # a way to make that work, then no need to do this function here. 
    # Note that this will ideally update stockfish with a new position, but you should still return the FEN
    # since it's useful to store in a Node. E.g., when backtracking on the tree from child --> parent, you'd
    # want to re-update Stockfish's position with the parent's FEN (in preparation for continuing to its
    # other children).
    
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