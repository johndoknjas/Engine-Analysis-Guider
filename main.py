from stockfish import Stockfish

stockfish = Stockfish(path = r"C:\Users\johnd\Documents\Fun Coding Projects\Stockfish Guider\stockfish-10-win\Windows\stockfish_10_x64.exe",
                      depth = 28, parameters = {"MultiPV": 1, "Threads": 4})

def main():
    print("Hi")
    #stockfish.set_fen_position("4rrk1/pp1nqpbp/3p2p1/2nPP3/2p2P2/P1N1BQPP/1PB3K1/3R1R2 b - - 0 20")
    print(stockfish.get_evaluation())
    print(stockfish.get_best_move())
    
if __name__ == '__main__':
    main()