####################
#ウィルス流行シミュレーション（のまねっこ）v0.8 by K.Sakurai 2020.4.29
#Using Python Mode for Processing 3
#
#紹介していただいた道越 秀吾さんのシミュレーションを
#Processing(Python mode)で真似しようとしたものです．元ネタURLは以下．
#https://rad-it21.com/サイエンス/michikoshi-shugo_20200331/
#
#Processing上ではnumpy.random.randn()がないので
#感染者マスからの接触数を正規分布で書けないのが気に食わない．
#どげんかしたければもうPythonで書いちゃうのがいい．
#
#☆これからやっていく
#セルの移動に対応する
#ステップ毎のS,I,Rを.csvに書き出せるようにする
#
#☆改善タスク
#配列内からランダムにn個を書き換えるところは処理を減らせる．
#感染処理部分を関数に書き出す
#他にもいろいろ軽くできそう
####################

import copy

#パラメータ入力
inf_rate = 0.1 #感染確率
rec_rate = 0.1 #回復確率
n_initial = 0.01 #初期感染者割合
n_contact = 4.8 #接触数
n_void = 0 #空隙率

wait_time = 0 #待ち時間

#箱庭と感染者数チェッカーの用意
cells = [[0 for i in range(100)] for j in range(100)] 

def setup():
    size(800, 800) #ウィンドウサイズは800x800（1セル8x8）
    background(255)

    initialize() #しょきか
   
    #最初の表示
    paint()
    
    #フレーム撮影する場合は下の1行のコメントアウトを外す その1
    #saveFrame("frames/######.png")

                        
def draw():
    
    global cells
    
    #次状態を記録するリストを用意し初期化（全体をSとして初期化する）
    cells_next = [[0 for i in range(100)] for j in range(100)] 
    
    #処理1：感染
    for i in range(100):
        for j in range(100):
            
            #そのセルがIなら，接触マスを指定して感染処理
            if cells[i][j] == 1:
                
                #周囲8マスのうちランダムで（接触数）だけ接触する．
                cont = touch()
                
                #接触マスに感染確率の割合でIを上書き
                if cont[0] == 1:
                    if random(0,1) <= inf_rate:
                        cells_next[i-1][j-1] = 1
                if cont[1] == 1:
                    if random(0,1) <= inf_rate:
                        cells_next[i-1][j] = 1
                if cont[2] == 1:
                    if random(0,1) <= inf_rate:
                        cells_next[i-1][(j+1)%100] = 1
                if cont[3] == 1:
                    if random(0,1) <= inf_rate:
                        cells_next[i][j-1] = 1
                if cont[4] == 1:
                    if random(0,1) <= inf_rate:
                        cells_next[i][(j+1)%100] = 1
                if cont[5] == 1:
                    if random(0,1) <= inf_rate:
                        cells_next[(i+1)%100][j-1] = 1
                if cont[6] == 1:
                    if random(0,1) <= inf_rate:
                        cells_next[(i+1)%100][j] = 1
                if cont[7] == 1:
                    if random(0,1) <= inf_rate:
                        cells_next[(i+1)%100][(j+1)%100] = 1
    
    #処理2：回復
    for i in range(100):
        for j in range(100):
            
            #現在の感染者は回復確率で回復
            if cells[i][j] == 1:
                if random(0,1) <= rec_rate:
                    cells_next[i][j] = 2
                else:
                    cells_next[i][j] = 1
    
    #処理3：回復者上書き
    for i in range(100):
        for j in range(100):
            
            #そのセルが回復者なら，感染処理後も回復者（感染してても上書き）
            if cells[i][j] == 2:
                cells_next[i][j] = 2
    
    #処理4：空隙上書き            
    for i in range(100):
        for j in range(100):
            #そのセルが空隙なら，感染処理後も空隙（感染してても上書き）
            if cells[i][j] == 3:
                cells_next[i][j] = 3

    
    #全処理が終わったらcells_nextをcellsに移す
    cells = copy.deepcopy(cells_next)
    del cells_next
    
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
    
    #フレーム撮影する場合は下の1行のコメントアウトを外す その2
    #saveFrame("frames/######.png")
    
    #最後にwait_timeだけ待つ
    delay(wait_time)



########## draw関数ここまで ##########    

#セルの状態を読み取り，塗る色を決める関数
def paint():
    global cells
    
    for i in range(100):
        for j in range(100):
            
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
    cells = [[0 for i in range(100)] for j in range(100)] 

    #空隙を用意（全セル数x空隙率だけ空隙セルを作成）
    index = 0
    while index < 10000 * n_void:
        hit = floor(random(0, 10000))
        if cells[floor(hit / 100)][hit % 100] == 0:
            cells[floor(hit / 100)][hit % 100] = 3
            index += 1
    
    #初期感染者を用意（全セル数x(1-空隙率)x初期感染者割合だけ感染者セルを作成）
    index = 0
    while index < 10000 * (1 - n_void) * n_initial:
        hit = floor(random(0, 10000))
        if cells[floor(hit / 100)][hit % 100] == 0:
            cells[floor(hit / 100)][hit % 100] = 1
            index += 1
    
    #最初はnextも同じものを用意
    cells_next = copy.deepcopy(cells)
    
    #境目の点をつける
    stroke(0)
    for i in range(99):
        for j in range(99):
            point(j*8+7, i*8+7)

    #以降，枠線はつけない
    noStroke()

#クリックしたらリスタート
def mousePressed():
    global cells
    noLoop()
    delay(100)
    initialize()
    loop()

#接触セル指定
def touch():
    index = n_contact
    touchs = [0, 0, 0, 0, 0, 0, 0, 0]
    while index >= 1:
        num = floor(random(0,8))
        if touchs[num] == 0:
            touchs[num] = 1
            index -= 1
            
    b = probability(index)
    while b == True:
        num = floor(random(0,8))
        if touchs[num] == 0:
            touchs[num] = 1
            b = False
    return touchs
        

#接触数の小数点処理(4.8ならば，80%が5人，20%が4人と接触するように）
def probability(num):
    if num >= random(0,1):
        return True
    else:
        return False
