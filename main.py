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

# Note that two positions with the same piece and pawn arrangements can have different FENs, as a
    # result of using the function in models.py. E.g., f3d4 b8c6 b1c3 f7f5 versus f3d4 f7f5 b1c3 b8c6.
    # If there's a White pawn on e5, then in one of the FENs the f6-square will be recorded as a square
    # that en passant can happen on. Also: b1c3 g8f6 c3b1 f6g8. This will have a different FEN than the position
    # it started in two moves ago, since the fullmove counter value will be increased by 2. Or
    # g1f3 g8f6 d2d4 versus d2d4 g8f6 g1f3. These will result in different FENs due to different halfmove clock
    # values for them. Also moving an uncastled king to a square, and then back, will result in a differnt FEN, 
    # since no castling rights (or moving one of the rooks to a square and back, since no castling rights to that
    # side of the board).
    # All of this is good, since the new FEN of a position should be based off data from the parent Node's FEN.
    # After all, you are searching/guiding the engine ahead in a calculation tree. But for looking an FEN up in an 
    # SQL database or dictionary/hash table, you shouldn't care about the fullmove values or halfmove clock or fullmove counter 
    # values. These don't affect the position itself (the fullmove counter is irrelevant, and the halfmove counter 
    # is only relevant if nearing the 50 move rule, and even here the engine would probably give 0.00 anyway), and 
    # so it's fine to use an already derived evaluation in the DB / dictionary / hash table for a position with the same 
    # piece/pawn placement. However, if an FEN differs in castling rights, or if one has a certain square for 
    # en passant (or they have different en passant squares), then the DB / dictionary should not be used, as it's 
    # a unique position.

# Could display an ongoing estimate of how much the program is completed, every 10 seconds or something
# Calculate by seeing how many nodes have been evaluated in total, and how many still have to be
# evaluated (multiPV ^ depth, which can be stored in some global variable). If you get to a node that has an 
# evaluation that makes you stop the search there (e.g., too far from the goal evaluation), then 
# figure out the number of descendant nodes it has that have essentially been trimmed, and 
# subtract that from the global variable that stored the multiPV ^ depth figure. Alternatively, you could
# add the number of descendent nodes that have been trimmed to the figure storing the number of nodes
# already calculated, and then divide that by the multiPV ^ depth figure.
    # Also when in a node, but only a few of its child(ren) are considered (less than the multiPV value),
    # once again this involves branches being trimmed.
    
# Once/if you create a GUI, you can display this ongoing estimate in the form of a continuously updated
# progress bar (maybe updated every few seconds - shouldn't have much/any impact on the SF engine thinking?).
# In the GUI you can also display a chess board showing the current position being calculated.
    # For the GUI, try not to have a separate thread running for it while the SF enging is calculating in
    # the Node search tree. Whenever a new Node is created, then call a function that updates the GUI
    # with the progress bar stuff and the position being calculated. Since there should be no user input
    # allowed in the GUI at this time, no thread should be needed. Only time input could possibly be allowed in
    # the GUI is before SF calculates through the search tree (e.g., for getting preliminary parameter data
    # from the user, but even here the command line may be better).
    




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
        
        stockfish13.set_fen_position(FEN, node_depth == 0)
        if self.node_move is not None:
            stockfish13.make_moves_from_current_position([self.node_move])
        parameters = stockfish13.get_parameters()
        self.FEN = stockfish13.get_fen_position()
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
        
        if not self.PVs:
            # There are no moves in this position, so set self.evaluation
            # to the evaluation stockfish directly gives in this position.
            # It will either be a mate or a stalemate.
            evaluation_dict = stockfish13.get_evaluation() # CONTINUE HERE - modify
            # get_evaluation() to temporarily set the multiPV value to 1. Or, just make sure
            # multiPV is set to 1 by default, and when get_top_moves() is called, it gets set to some
            # number n, but then reset to 1 (making it always = 1 when get_evaluation() is called).
        
            # Another (better?) option is just calling get_top_moves(1) instead of get_evaluation(),
            # although you will have to modify
            # the immediate behavior in the scope of this if statement (return value will be a list containing
            # a single dictionary - I think then you will just use the Mate / Centipawn value of the move,
            # which will be the top move in this position).
            assert(evaluation_dict["value"] == 0)
            if evaluation_dict["type"] == "mate":
                self.evaluation = MIN_INTEGER if self.white_to_move else MAX_INTEGER
            else:
                assert(evaluation_dict["type"] == "cp")
                self.evaluation = 0
        elif node_depth == search_depth:
            # At a leaf node in the tree.
            if self.PVs[0]["Centipawn"] is not None:
                self.evaluation = self.PVs[0]["Centipawn"]
            elif (self.PVs[0]["Mate"] > 0):
                self.evaluation = MAX_INTEGER
            else:
                self.evaluation = MIN_INTEGER
        else:
            for current_PV in self.PVs:
                # CONTINUE HERE:
                # After going from each child back to parent in this loop, make sure to
                # reset Stockfish's position with set_FEN_position(and with False param).
                new_move = current_PV["Move"]
                child_node = Node(self, self.FEN, search_depth, node_depth + 1, 
                                  new_move, not(self.white_to_move))
                stockfish13.set_fen_position(self.FEN, False)                 
                # Note that the self arg above will be the parent_node param
                # for the child_node.
                
                # The False arg says to not sent the "ucinewgame" token to stockfish; the most important
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
        if first.evaluation is None or second.evaluation is None:
            raise ValueError("first.evaluation or second.evaluation has no value.")
        return (second.evaluation - first.evaluation) * (1 if self.white_to_move else -1)
    
    def check_PVs_sorted(self):
        # CONTINUE HERE - Done rewriting this function, now test that
        # the program works with the test position. After that, just optimization stuff
        # which the comments describe. Also delete some obsolete comments that you've already
        # implemented today.
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
    # CONTINUE HERE - Nothing to do in this function for now. But after writing the make_move function,
    # run the program and call this function to check the tree. So far it looks good, with the make_move
    # simply flipping whose turn it is in the FEN (but not making any actual moves). The root node's
    # evaluation is based off the top moves for both sides, which is good.
    
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
    
    stockfish13 = Stockfish(path = r"C:\Users\johnd\Documents\Fun Coding Projects\Stockfish Guider\stockfish_13_win_x64_bmi2.exe",
                            depth = stockfish_depth, parameters = {"Threads": 4, "MultiPV": multiPV_num})
    # CONTINUE HERE - Have some way for the user to enter a path on their own. If they don't enter a path
    # (e.g., if you're the user), then it could default to the path you have here.
    
    root_node = Node(None, FEN, search_depth, 0, None, is_whites_turn(FEN))
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