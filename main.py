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
    # Not sure if you'll have to do pip uninstall to make sure you use the code you will
    # clone for Python Stockfish (instead of using what pip install provides).

from stockfish import Stockfish

#stockfish = Stockfish(path = r"C:\Users\johnd\Documents\Fun Coding Projects\Stockfish Guider\stockfish-10-win\Windows\stockfish_10_x64.exe",
#                      depth = 20, parameters = {"MultiPV": 3, "Threads": 4})

stockfish13 = Stockfish(path = r"C:\Users\johnd\Documents\Fun Coding Projects\Stockfish Guider\stockfish13.exe",
                        depth = 24, parameters = {"Threads": 4})

stockfish13Mod = Stockfish(path = r"C:\Users\johnd\Documents\Fun Coding Projects\Stockfish Guider\stockfish13OutputModification.exe",
                           depth = 24, parameters = {"Threads": 4, "MultiPV": 2})

def main():
    print("Hi")
    stockfish13.set_fen_position("rnbqkbnr/pppp1ppp/8/4p3/4PP2/8/PPPP2PP/RNBQKBNR b KQkq - 0 2")
    stockfish13Mod.set_fen_position("rnbqkbnr/pppp1ppp/8/4p3/4PP2/8/PPPP2PP/RNBQKBNR b KQkq - 0 2")
    print("Stockfish 13:")
    print(stockfish13.get_evaluation())
    print(stockfish13.get_best_move())
    print("Stockfish 13 Mod:")
    print(stockfish13Mod.get_evaluation())
    print(stockfish13Mod.get_best_move()) # Outputs the second best move, as hoped.
    
if __name__ == '__main__':
    main()