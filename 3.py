# coding: utf-8
import sys
import pygame
from pygame.locals import *

def init_window():
    pygame.init()
    pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Conway\'s Game of Life')


def draw_background(scr, img=None):
    if img:
        scr.blit(img, (0, 0))
    else:
        bg = pygame.Surface(scr.get_size())
        bg.fill((128, 128, 128))
        scr.blit(bg, (0, 0))




#-----------------------------------------------
# ����� ����� ������ ��� ������
# ��������� ����� �� �����. �������: 1-����� ������ 0-�������
# ����� ����� ��������
# M[0..1][x][y] - ��� ����. ��� ���������� ���������� ������� � ������� ����������
# current_layer ��������� ������� ����
# x_max, y_max ������� ����
# ������ ���� - ����� � ������ ������� �������, ������� � ������ ����


class Map:
    def __init__(self, f_name, cell_width):

        self.cell_width = cell_width
        self.current_layer = 0 # ������� ����
        self.cell_changed = 0 # ������� ����� ����������
        # �������� ����� �� �����
        in_f=open(f_name,'r')
        s=in_f.readline().rstrip()
        (w,h) = map(int, s.split(','))
        self.M = [0,0] # ��� ����
        self.M[0] = [ [0]*h for i in range(w) ] # ������ ���� ������ ���������� ���������
        self.M[1] = [ [0]*h for i in range(w) ] # ������ ������� ��������� - ����� ��� ��������

        s=in_f.readline()
        i=0
        while len(s)>0:
            for j in range(len(s)):
                if s[j]=='1': # �����
                    self.M[self.current_layer][j][i] = 1

            # ������ ���� ������ �� �����
            s=in_f.readline()
            i+=1
        in_f.close()

    def is_changed(self):
        return self.cell_changed


    # �������� ����� ���������
    def recalc(self):
        self.current_layer = (self.current_layer+1)%2
        self.cell_changed = 0
        for i in range(len(self.M[self.current_layer])):
            for j in range(len(self.M[self.current_layer][i])):
                self.cell_calculate(i,j)

    # ������ ����� ������ � ������� ����
    # ������, ��� ������ ����
    def cell_calculate(self, x, y):
        prev = (self.current_layer+1)%2
        x_max = len(self.M[self.current_layer])
        y_max = len(self.M[self.current_layer][x])
        cnt = self.M[prev][x-1][y-1] + self.M[prev][x-1][y] + self.M[prev][x-1][(y+1)%y_max] + \
              self.M[prev][x][y-1] + self.M[prev][x][(y+1)%y_max] + \
              self.M[prev][(x+1)%x_max][y-1] + self.M[prev][(x+1)%x_max][y] + self.M[prev][(x+1)%x_max][(y+1)%y_max]
        if self.M[prev][x][y]: # ����� ������
            if 2<= cnt <= 3: # �������� ����
                self.M[self.current_layer][x][y] = 1
            else:
                self.M[self.current_layer][x][y] = 0
                self.cell_changed += 1
        else: # ������� ������
            if cnt == 3: # ������ �����
                self.M[self.current_layer][x][y] = 1
                self.cell_changed += 1
            else: # �� ������
                self.M[self.current_layer][x][y] = 0
    
    
    # ��������� �����
    def draw(self, scr):
        for i in range(len(self.M[self.current_layer])):
            for j in range(len(self.M[self.current_layer][i])):
                live=self.M[self.current_layer][i][j]
                if live: # FIXME �������� �����
                    pygame.draw.circle(scr, RED, [self.cell_width*i+self.cell_width//2,self.cell_width*j+self.cell_width//2], self.cell_width//2)
#                else: # ������ �� �����
#                    pygame.draw.circle(scr, BLUE, [self.cell_width*i+self.cell_width//2,self.cell_width*j+self.cell_width//2], self.cell_width//2)

#-----------------------------------------------
def process_events(events):
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit(0)
#-----------------------------------------------

def message_box(screen, message):
    # ����� ��������� � ������ �� ������
    fontobject = pygame.font.Font(None,18)
    pygame.draw.rect(screen, (0,255,0),
                   ((screen.get_width()/2) - 200,
                    (screen.get_height()) - 40,
                    400,40), 0)
    pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width()/2) - 202,
                    (screen.get_height()) - 42,
                    404,44), 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width()/2) - 100, (screen.get_height()) - 20))

    pygame.display.flip()


#-----------------------------------------------
if __name__ == '__main__':
    if len(sys.argv) <2:
        print('usage:', sys.argv[0], ' init-file')
        sys.exit()
    f_name = sys.argv[1]

    init_window()
    cell_size = 10 # ������� �������� �������� ���� ������
    RED = (255,0,0) # ������� ����
    BLUE = (0,0,255) # �����
    map = Map(f_name, cell_size) # ����� Map �������� ��� ��������� �� ����� f_name

    background = None #pygame.image.load("./resources/background.png")
    screen = pygame.display.get_surface()
    map.draw(screen)


    while 1: # ����� �������� ����
        process_events(pygame.event.get())
        pygame.time.delay(100)
        draw_background(screen, background)
        map.recalc() # ����������� ��� ������
        map.draw(screen) # � ������� �� �����
        pygame.display.update()

#        if not map.is_changed(): # ���� �������
#            message_box(screen,'NO CHANGES!!!')
#            pygame.time.delay(3000)
#            break

