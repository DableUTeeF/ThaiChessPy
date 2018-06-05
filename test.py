import ThaiChessPy as chess

board = chess.Board()
Nf2 = chess.Move.from_uci("g1e8")
# for mov in board.legal_moves:
#     a = str(mov)
#     print(mov)
print(board)
