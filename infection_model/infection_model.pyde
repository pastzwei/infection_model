####################
#ウィルス流行シミュレーション（のまねっこ）v0.95 by K.Sakurai 2020.4.29
#Using Python Mode for Processing 3
#
#紹介していただいた道越 秀吾さんのシミュレーションを
#Processing(Python mode)で真似しようとしたものです．元ネタURLは以下．
#https://rad-it21.com/サイエンス/michikoshi-shugo_20200331/
#
#※繰り返し処理は，状態が変化しなくなったら自動的に停止します．
#※画面内をクリックすると，状態をリセットして再実行します．
#
#☆これからやっていく
#セルの移動に対応する
#ステップ毎のS,I,Rを画面表示し，.csvに書き出せるようにする
####################

import copy
import random

#パラメータ入力
n_siz = 100 #モデルのサイズ（32以上できれいに正方形．大きすぎると重くなるよ）
inf_rate = 0.1 #感染確率
rec_rate = 0.1 #回復確率
n_initial = 0.01 #初期感染者割合
n_contact_average = 4.8 #接触数平均
n_contact_sigma = 1.0 # 接触数標準偏差
n_void = 0 #空隙率

wait_time = 0 #待ち時間

#箱庭と感染者数チェッカーの用意
cells = [[0 for i in range(n_siz)] for j in range(n_siz)] 

def setup():
    size(n_siz * 8, n_siz * 8 + 120) #ウィンドウサイズは800x800（1セル8x8）
    background(255)
    myFont = createFont("メイリオ", 48)
    textFont(myFont)

    initialize()
    
    #フレーム撮影する場合は下の1行のコメントアウトを外す その1
    #saveFrame("frames/######.png")
                        
def draw():
    
    global cells
    
    #次状態を記録するリストを用意し初期化（全体をSとして初期化する）
    cells_next = [[0 for i in range(n_siz)] for j in range(n_siz)] 
    
    #処理1：感染
    for i in range(n_siz):
        for j in range(n_siz):
            
            #そのセルがIなら，接触マスを指定して感染処理
            if cells[i][j] == 1:
                
                #周囲8マスのうちランダムで（接触数）だけ接触する．
                cont = touch()
                
                #接触マスに感染確率の割合でIを上書き
                if cont[0] == 1:
                    if random.random() <= inf_rate:
                        cells_next[i-1][j-1] = 1
                if cont[1] == 1:
                    if random.random() <= inf_rate:
                        cells_next[i-1][j] = 1
                if cont[2] == 1:
                    if random.random() <= inf_rate:
                        cells_next[i-1][(j+1)%n_siz] = 1
                if cont[3] == 1:
                    if random.random() <= inf_rate:
                        cells_next[i][j-1] = 1
                if cont[4] == 1:
                    if random.random() <= inf_rate:
                        cells_next[i][(j+1)%n_siz] = 1
                if cont[5] == 1:
                    if random.random() <= inf_rate:
                        cells_next[(i+1)%n_siz][j-1] = 1
                if cont[6] == 1:
                    if random.random() <= inf_rate:
                        cells_next[(i+1)%n_siz][j] = 1
                if cont[7] == 1:
                    if random.random() <= inf_rate:
                        cells_next[(i+1)%n_siz][(j+1)%n_siz] = 1
    
    #処理2：回復
    for i in range(n_siz):
        for j in range(n_siz):
            
            #現在の感染者は回復確率で回復
            if cells[i][j] == 1:
                if random.random() <= rec_rate:
                    cells_next[i][j] = 2
                else:
                    cells_next[i][j] = 1
    
    #処理3：回復者上書き
    for i in range(n_siz):
        for j in range(n_siz):
            #そのセルが回復者なら，感染処理後も回復者（感染してても上書き）
            if cells[i][j] == 2:
                cells_next[i][j] = 2
    
    #処理4：空隙上書き            
    for i in range(n_siz):
        for j in range(n_siz):
            #そのセルが空隙なら，感染処理後も空隙（感染してても上書き）
            if cells[i][j] == 3:
                cells_next[i][j] = 3

    
    #全処理が終わったらcells_nextをcellsに移す
    cells = copy.deepcopy(cells_next)
    
    #SIRそれぞれの総数をカウント
    S_now = sum(v.count(0) for v in cells)
    I_now = sum(v.count(1) for v in cells)
    R_now = sum(v.count(2) for v in cells)
    
    #感染者が0ならばループ解除
    if I_now == 0:
        noLoop()
        println("stopped")
    
    #表示を更新
    paint()
    
    fill(192)
    rect(0, n_siz*8, n_siz*8, 60)
    fill(0)
    text("S:" + str(S_now) + " I:" + str(I_now) + " R:" + str(R_now), 8, n_siz*8 + 48)
    
    #フレーム撮影する場合は下の1行のコメントアウトを外す その2
    #saveFrame("frames/######.png")
    
    #最後にwait_timeだけ待つ
    delay(wait_time)



########## draw関数ここまで ##########    

#セルの状態を読み取り，塗る色を決める関数
def paint():
    global cells
    
    for i in range(n_siz):
        for j in range(n_siz):
            
            #セルの色を指定
            if cells[i][j] == 0:    #0は感受性保持者S（白）
                fill(255)
            elif cells[i][j] == 1:    #1は感染者I（赤）
                fill(255, 0, 0)
            elif cells[i][j] == 2:    #2は免疫保持者R（緑）
                fill(0, 255, 0)
            elif cells[i][j] == 3:    #3は空隙（黒）
                fill(0)
            else:               #それ以外はわからん（灰：出たらバグ）
                fill(128)
                
            #セルを塗る
            rect(8*j, 8*i, 7, 7)
        
#初期設定
def initialize():
    global cells
    
    #箱庭リセット
    cells = [[0 for i in range(n_siz)] for j in range(n_siz)] 

    #空隙を用意（全セル数x空隙率だけ空隙セルを作成）
    k = int(round(n_siz * n_siz * n_void))
    hits = random.sample(range(n_siz * n_siz - 1), k)
    for hit in hits:
        cells[hit / n_siz][hit % n_siz] = 3

    
    #初期感染者を用意（全セル数x(1-空隙率)x初期感染者割合だけ感染者セルを作成）
    k = int(round(n_siz * n_siz * (1 - n_void) * n_initial))
    hits = random.sample(range(n_siz * n_siz - 1), k)
    for hit in hits:
        cells[hit / n_siz][hit % n_siz] = 1
    
    #境目の点をつける
    stroke(0)
    for i in range(n_siz - 1):
        for j in range(n_siz - 1):
            point(j*8+7, i*8+7)

    noStroke()
    
    paint()
    
    #最初の表示
    fill(192)        
    rect(0, n_siz*8, n_siz*8, 120)
    fill(0)
    text("I:" + str(inf_rate) + " R:" + str(rec_rate) + " Init:" + str(n_initial) + " Void:" + str(n_void), 8, n_siz*8 + 108)

#クリックしたらリセットしてリスタート
def mousePressed():
    global cells
    noLoop()
    delay(100)
    initialize()
    loop()

#接触セル指定
def touch():
    touchs = [0, 0, 0, 0, 0, 0, 0, 0]
    k = int(round(random.gauss(n_contact_average, n_contact_sigma)))
    if k > 8:
        k = 8
    elif k < 0:
        k = 0
    touch = random.sample(range(8), k)
    for i in touch:
        touchs[i] = 1

    return touchs
