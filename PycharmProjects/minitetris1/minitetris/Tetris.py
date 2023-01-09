import pygame, sys, time
from pygame.locals import *
from Board import *

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)
MAIN_VIOLET = (153, 153, 255)

class Tetris:

    #생성자
    def __init__(self):
        self.screen = pygame.display.set_mode((350, 450))
        self.clock = pygame.time.Clock()
        self.board = Board(self.screen)
        self.music_on_off = True
        self.check_reset = True
    # 각 키를 누를때 실행되는  method
    def handle_key(self, event_key):
        if event_key == K_DOWN or event_key == K_s:
            self.board.drop_piece()
        elif event_key == K_LEFT or event_key == K_a:
            self.board.move_piece(dx=-1, dy=0)
        elif event_key == K_RIGHT or event_key == K_d:
            self.board.move_piece(dx=1, dy=0)
        elif event_key == K_UP or event_key == K_w:
            self.board.rotate_piece()
        elif event_key == K_SPACE:
            self.board.full_drop_piece()
        elif event_key == K_q:
            self.board.ultimate()
        elif event_key == K_m: # 소리 설정
            self.music_on_off = not self.music_on_off
            if self.music_on_off:
                pygame.mixer.music.play(-1, 0.0)
            else:
                pygame.mixer.music.stop()
    #최고점
    def HighScore(self):
        try:
            f = open('assets/save.txt', 'r') #save.txt에 점수 기록, 파일 읽기
            l = f.read()
            f.close()
            if int(l) < self.board.score:
                h_s = self.board.score
                f = open('assets/save.txt', 'w')
                f.write(str(self.board.score))
                f.close()
            else:
                h_s = l
            self.board.HS(str(h_s))
        except:
            f = open('assets/save.txt', 'w') #파일에 쓰기
            f.write(str(self.board.score))
            f.close()
            self.board.HS(str(self.board.score))

    #실행하기
    def run(self):
        pygame.init()
        icon = pygame.image.load('assets/images/icon.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Tetris')
        pygame.time.set_timer(pygame.USEREVENT, 500)
        start_sound = pygame.mixer.Sound('assets/sounds/Start.wav')
        start_sound.play()
        bgm = pygame.mixer.music.load('assets/sounds/bgm.mp3')
        while True:
            if self.check_reset:
                self.board.newGame()
                self.check_reset = False
                pygame.mixer.music.play(-1, 0.0)
            if self.board.game_over():
                self.screen.fill(BLACK)
                pygame.mixer.music.stop()
                self.board.GameOver()
                self.HighScore()
                self.check_reset = True
                self.board.init_board()
            for event in pygame.event.get():
                # 게임 진행 중 - event는 키보드 누를때,특정 동작 수행할때 방생
                if event.type == QUIT: #종료 이벤트가 발생한 경우
                    pygame.quit() #모든 호출 종료
                    sys.exit() #게임을 종료한다.
                elif event.type == KEYUP and event.key == K_p: #일시 정지 버튼 누르면
                    self.screen.fill(BLACK)
                    pygame.mixer.music.stop()
                    self.board.pause()
                    pygame.mixer.music.play(-1, 0.0)
                elif event.type == KEYDOWN: #키보드를 누르면
                    self.handle_key(event.key) #handle메소드 실행
                elif event.type == pygame.USEREVENT:
                    self.board.drop_piece()
                elif event.type == VIDEORESIZE:
                    info = pygame.display.Info()
                    resize = event.h / self.board.display_height

                    if event.w != self.board.display_width:
                        pygame.display.set_mode((self.board.display_width, self.board.display_height), RESIZABLE)

                    if resize != 1:
                        self.vdresize(resize, event.h)
                        if info.current_w == (1855):
                            pygame.display.set_mode((info.current_w, info.current_h), RESIZABLE).fill(MAIN_VIOLET)
            # self.screen.fill(BLACK)
            self.board.draw()
            pygame.display.update()
            self.clock.tick(30)

if __name__ == "__main__":
    Tetris().run()
