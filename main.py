from functools import cmp_to_key
from models import Stockfish

MAX_INTEGER = 1000000000
MIN_INTEGER = -1 * MAX_INTEGER

#stockfish = Stockfish(path = r"C:\Users\johnd\Documents\Fun Coding Projects\Stockfish Guider\stockfish-10-win\Windows\stockfish_10_x64.exe",
#                      depth = 20, parameters = {"MultiPV": 3, "Threads": 4})

stockfish13 = None

# CONTINUE HERE - looks like the app is working. So now it's time to optimize things, and of course
# do some more tests with the output tree. Go to the various CONTINUE HERE tags in the program
# for things to do, and also browse the IDEAS section above. Maybe even check Issues on GitHub
# in case you wrote anything unique there.

# CONTINUE HERE - Play around with testing more positions with the app, and examine the output tree.
# Try to check if it works with positoins where both sides can mate, or positions where one
# side has multiple ways to mate, etc. Seems good with what I've tested so far. Still a little
# slow though (2-3x slower than what I'd expect sometimes, although maybe my calculations for expectations
# are flawed).

class Node:
    
    def __init__(self, parent_node, FEN, search_depth, node_depth, node_move, white_to_move):
        global stockfish13
        
        # Note that FEN is the FEN of the parent, and node_move still has to be
        # made on the FEN. The only exception to this is if this is the initialization
        # of the root node, in which case the FEN is the root node's FEN and
        # node_move equals None.
        
        # Meanwhile, the the other constructor arguments are all up to date with what
        # this Node's fields should be, and they will be set equal to them below.
        
        if node_depth > search_depth:
            raise ValueError("node_depth > search_depth")
        
        self.children = [] # CONTINUE HERE - consider maybe changing to a dictionary?
        self.evaluation = None
        self.white_to_move = white_to_move
        self.parent_node = parent_node
        self.search_depth = search_depth
        self.node_depth = node_depth
        self.node_move = node_move
        
        stockfish13.set_fen_position(FEN, self.node_depth == 0)
        if self.node_move is not None:
            stockfish13.make_moves_from_current_position([self.node_move])
        parameters = stockfish13.get_parameters()
        self.FEN = stockfish13.get_fen_position()
        self.is_leaf_node = (self.node_depth == self.search_depth)
        self.PVs = stockfish13.get_top_moves(1 if self.is_leaf_node else int(parameters["MultiPV"]))
        self.check_PVs_sorted()
        
        # self.PVs is a list whose elements are dictionaries (see what's returned
        # from get_top_moves in models.py).
        
        # CONTINUE HERE - also stop the search and declare this node a leaf node
        # if the evaluation is very big, where it's way past the goal evaluation. 
        # On the topic of this, you should get the goal evaluation from the user 
        # and pass it in to the constructor.
        
        if not self.PVs:
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
        elif self.is_leaf_node:
            if self.PVs[0]["Centipawn"] is not None:
                self.evaluation = self.PVs[0]["Centipawn"]
            elif (self.PVs[0]["Mate"] > 0):
                self.evaluation = MAX_INTEGER
            else:
                self.evaluation = MIN_INTEGER
        else:
            for current_PV in self.PVs:
                new_move = current_PV["Move"]
                child_node = Node(self, self.FEN, self.search_depth, self.node_depth + 1, 
                                  new_move, not(self.white_to_move))
                stockfish13.set_fen_position(self.FEN, False)                 
                # Note that the self arg above will be the parent_node param
                # for the child_node.
                
                # The False arg says to not send the "ucinewgame" token to stockfish; the most important
                # effect of this is that it preserves the TT. This may help a little, even though it's going
                # from child --> parent. You could try benchmarking tests experimenting with this
                # arg being False and True, to see which is faster.
                
                # I asked in the SF discord and basically the "ucinewgame" token should only be used
                # when starting a new game from scratch, or a position that's completely different (even then
                # I don't think is HAS to be used). So for going to a similar position, it makes sense (and is safe) 
                # to not call it. But again, benchmarking should be done to see if it actually helps.
                
                self.children.append(child_node)
                self.children = sorted(self.children, key=cmp_to_key(self.compare_nodes))
                if (self.evaluation is None or
                    (self.white_to_move and child_node.evaluation > self.evaluation) or
                    (not(self.white_to_move) and child_node.evaluation < self.evaluation)):
                        self.evaluation = child_node.evaluation

    def compare_nodes(self, first, second):
        if first.evaluation is None or second.evaluation is None:
            raise ValueError("first.evaluation or second.evaluation has no value.")
        return (second.evaluation - first.evaluation) * (1 if self.white_to_move else -1)
    
    def check_PVs_sorted(self):
        if len(self.PVs) <= 1:
            return
        for i in range(1, len(self.PVs)):
            first_var = self.PVs[i-1]
            second_var = self.PVs[i]
            assert first_var["Mate"] is None or first_var["Mate"] != 0
            assert second_var["Mate"] is None or second_var["Mate"] != 0
            if first_var["Mate"] is None:
                if second_var["Mate"] is None:
                    assert (first_var["Centipawn"] == second_var["Centipawn"] or
                            (self.white_to_move and first_var["Centipawn"] > second_var["Centipawn"]) or
                            (not(self.white_to_move) and first_var["Centipawn"] < second_var["Centipawn"]))
                else:                    
                    assert (second_var["Mate"] < 0) == self.white_to_move
            else:
                # first_var["Mate"] isn't None
                if second_var["Mate"] is None:
                    if (first_var["Mate"] > 0) != self.white_to_move:
                        print(first_var["Mate"])
                        print("white to move" if self.white_to_move else "black to move")
                    assert (first_var["Mate"] > 0) == self.white_to_move
                else:
                    # second_var["Mate"] isn't None
                    if first_var["Mate"] == second_var["Mate"]:
                        continue
                    elif self.white_to_move:
                        assert not(first_var["Mate"] < 0 and second_var["Mate"] > 0)
                        assert ((first_var["Mate"] > 0 and second_var["Mate"] < 0) or
                                second_var["Mate"] > first_var["Mate"])
                    else:
                        # Black to move
                        assert not(first_var["Mate"] > 0 and second_var["Mate"] < 0)
                        assert ((first_var["Mate"] < 0 and second_var["Mate"] > 0) or
                                second_var["Mate"] < first_var["Mate"])

def output_tree(node):    
    print("node evaluation: " + str(node.evaluation))
    if node.children:
        print("Child nodes:")
        counter = 1
        for child_node in node.children:
            print(str(counter) + ". Node move: " + child_node.node_move + ". Evaluation: " + str(child_node.evaluation))
            counter += 1
        print("To inspect a node in the above list, enter its corresponding number:")
    if node.parent_node is not None:
        print("Or, enter P to return to the parent node.")
    print("Or, enter Q to quit.")
    while True:
        user_input = input()
        if user_input == "q" or user_input == "Q":
            break
        elif user_input == "p" or user_input == "P":
            if node.parent_node is not None:
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
    assert FEN.count(' w ') + FEN.count(' b ') == 1
    return ' w ' in FEN

def main():
    global stockfish13
    
    FEN = input("Enter the FEN for the position: ")
    search_depth = int(input("Enter the max depth to search in the tree: "))
    multiPV_num = int(input("Enter the MultiPV number: "))
    stockfish_depth = int(input("Enter the search depth for SF: "))
    
    stockfish13 = Stockfish(path = r"C:\Users\johnd\Documents\Coding Projects\stockfish_13_win_x64_bmi2.exe",
                            depth = stockfish_depth, parameters = {"Threads": 4, "MultiPV": multiPV_num})
    # CONTINUE HERE - Have some way for the user to enter a path on their own. If they don't enter a path
    # (e.g., if you're the user), then it could default to the path you have here.
    
    root_node = Node(None, FEN, search_depth, 0, None, is_whites_turn(FEN))
    print(root_node.white_to_move)
    print(root_node.evaluation)
    
    user_input = input("To see the search tree, enter tree: ")
    if user_input == "tree":
        output_tree(root_node)

if __name__ == '__main__':
    main()

