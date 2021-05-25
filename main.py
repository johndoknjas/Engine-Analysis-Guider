from stockfish import Stockfish

stockfish = Stockfish(r"C:\Users\johnd\Documents\Fun Coding Projects\Stockfish Guider\stockfish-10-win\Windows\stockfish_10_x64.exe")

def main():
    print("Hi")
    print(stockfish.get_evaluation())
    print(stockfish.get_best_move())
    
if __name__ == '__main__':
    main()