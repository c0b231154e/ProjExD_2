import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650

DELTA = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, 5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def game_over(screen: pg.Surface) -> None:
    black_img = pg.Surface((1100, 650), pg.SRCALPHA)
    black_img.fill((0,0,0,128))
    screen.blit(black_img,(0, 0))

    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over",True, (255, 255, 255))
    screen.blit(txt, [400, 300])

    cry_img = pg.image.load("fig/8.png")
    screen.blit(cry_img, [350, 300]) 
    screen.blit(cry_img, [710, 300])

    pg.display.update()
    time.sleep(5)
    """
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
   for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
        bb_img.set_colorkey((0, 0, 0))
    return bb_imgs, bb_accs
    """
def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたrctが画面内か外かを判定
    引数はこうかとんか爆弾のrect
    画面内:true、画面外:false
    """
    yoko, tate = True, True
    if rct.left < 0 or rct.right > WIDTH:
        yoko = False
    if rct.top < 0 or rct.bottom > HEIGHT:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20,20)) #爆弾サーフェイス
    pg.draw.circle(bb_img,(255, 0, 0),(10,10),10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx,vy = +5,+5 #爆弾の速度ベクトル

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        #ゲームオーバー        
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            pg.display.update()
            return
            
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key,tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        bb_rct.move_ip(vx,vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横にはみ出てる
            vx *= -1
        if not tate:  # 縦にはみ出てる
            vy *= -1

        bb_imgs, bb_accs = init_bb_imgs()
        """
        avx = vx * bb_accs[min(tmr//500, 9)]
        avy = vy * bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.move_ip(vx, vy)
        """
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img,bb_rct)
        pg.display.update()

        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
