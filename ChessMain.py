import pygame as p
from Chess import ChessEngine
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    # IMAGES['wp'] = p.image.load("Images/wp.png")
    # Duyệt qua từng phần tử trong ds pieces
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("DACS4-Chess")
    # p.display.set_icon(p.image.load('bK.png'))
    clock = p.time.Clock()
    screen.fill("white")
    gs = ChessEngine.GameState()
    # print(gs.board)
    loadImages()
    running = True
    sqSelected = ()   #không có ô vuông nào được chọn, theo dõi lần nhấp chuột cuối cùng của người dùng
    playerClicks = []  #theo dõi số lần nhấp chuột của người chơi
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            #trinh xu li chuot
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  #(x,y) vị trí của chuột
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                # Kiểm tra ô vuông được chọn cùng vị trí với ô vuong được nhấp
                if sqSelected == (row,col):
                    sqSelected = ()      #bỏ chọn
                    playerClicks = []    #xoá sạch click của người chơi
                else:
                    sqSelected = (row, col) # lưu trữ ví trí ô vuông mới được chọn
                    playerClicks.append(sqSelected)  # thêm giá trị của biến vào sqSelected vào ds playerClicks
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation(move.startRow, move.startCol))
                    gs.makeMove(move)
                    sqSelected = () # reset click người chơi
                    playerClicks = []


             #Xu li key
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #hoan tac khi nhan Z
                    gs.undoMove()

        drawGameState(screen, gs)
        # giới hạn khung hình trò chơi
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)

    drawPieces(screen, gs.board)


'''
Ve cac hinh vuông bàn cờ 
'''


def drawBoard(screen):
    colors = [p.Color((255,237, 204)), p.Color((240, 179, 126))]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            # tổng là chẵn -> màu trắng, lẻ -> màu xám đậm
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
vẽ các quân cờ trên bảng bằng GameState.board hiện tại
'''


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                #sử dụng blit để của đối tượng screen ể vẽ hình ảnh quân cờ lên màn hình
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
