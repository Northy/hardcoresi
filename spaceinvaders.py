import sys, pygame, random, configparser
from timeit import default_timer as timer

pygame.init()

inimigos = []
bordasinimigos=[]
pontosinimigos=[]
balainimigoatirando = []
bordabalainimigo = []
lasttemp=99
lasttemp2=99
pontos=0

config = configparser.ConfigParser()
config.read("config.ini")

colunas = int(config.get('settings','colunas'))
linhas = int(config.get('settings','linhas'))

#Função de ajuste de resolução
def ajuste_res(px,o) :
    w = pygame.display.Info().current_w
    h = pygame.display.Info().current_h
    if w==1920 : return px
    if px<0 : return px+2
    if px<=20 : return px-2
    if px<=99 : return int(px*0.75)
    if o=="w" :
        x = int((w*px)/1920)
        return x
    if o=="h" :
        x = int((h*px)/1080)
        return x

#Carregar o fundo
tela = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption('Hardcore space invaders')
fundo = pygame.image.load("resources/fundo.png").convert()
fundo = pygame.transform.scale(fundo, (pygame.display.Info().current_w, pygame.display.Info().current_h))
bordafundo = fundo.get_rect()
tela.blit(fundo, bordafundo)
pygame.display.flip()

fundomenu = pygame.image.load("resources/menu.png").convert()
fundomenu = pygame.transform.scale(fundomenu, (pygame.display.Info().current_w, pygame.display.Info().current_h))
bordafundomenu = fundomenu.get_rect()

#Certo
certo = pygame.image.load("resources/certo.png").convert_alpha()
certo = pygame.transform.scale(certo,(ajuste_res(50,"w"),ajuste_res(50,"h")))

#Carregar o jogador
jogador = pygame.image.load("resources/nave.png").convert()
jogador = pygame.transform.scale(jogador, (ajuste_res(65,"w"),ajuste_res(50,"h")))
bordajogador = jogador.get_rect()

#Criar um novo jogo
def novojogo() :
    global vidas; global pontos; global nivel; global vinimigob; global balaatirando; global move; global jogadormorreu; global nivelcompleto; global breakar; global vbalainimigo
    vidas = 3
    pontos=0
    nivel=1
    vinimigob = False
    balaatirando = False
    move=0
    jogadormorreu = False
    nivelcompleto = False
    gerarinimigos(nivel)
    breakar = False
    vbalainimigo = 4

#Importar as fontes
pygame.font.init()
arial = pygame.font.SysFont('Arial', ajuste_res(70,"w"))
textopontos = arial.render("Pontos: ", True, (255,255,255))
textonivel = arial.render("Nível: ", True, (255,255,255))

#Inicializar a música
som = config.getboolean('settings','som')
musica = config.getboolean('settings','musica')
pygame.mixer.init()
background = pygame.mixer.Sound("resources/musica.ogg")
tiro = pygame.mixer.Sound("resources/tiro.ogg")
tiro.set_volume(float(config.get('settings','volume')))
if musica : background.play(-1)
background.set_volume(float(config.get('settings','volume')))

ultimo_click = timer()

#Menu
def menu(status, podesair) :
    global som; global musica; global ultimo_click
    arial = pygame.font.SysFont('Arial', ajuste_res(99,"w"))
    textostatus = arial.render(status, True, (0,0,0))
    while True :
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: sys.exit()
            if evento.type == pygame.KEYDOWN :
                if evento.key == pygame.K_ESCAPE and podesair : return
                elif evento.key == pygame.K_SPACE and podesair : return
                elif evento.key == pygame.K_SPACE and not(podesair) : novojogo(); return
        mouse = pygame.mouse.get_pos()
        x=mouse[0]; y=mouse[1]
        click = pygame.mouse.get_pressed()
        tempo = timer()-ultimo_click
        if click[0]==1 and tempo>0.2 :
            if x>=ajuste_res(730,"w") and x<=ajuste_res(1180,"w") and y>=ajuste_res(580,"h") and y<=ajuste_res(655,"h") :
                novojogo()
                return
            elif x>=ajuste_res(1020,"w") and x<=ajuste_res(1080,"w") and y>=ajuste_res(790,"h") and y<=ajuste_res(850,"h") :
                if som :
                    som=False
                    ultimo_click = timer()
                elif not(som) :
                    som=True
                    ultimo_click = timer()
            elif x>=ajuste_res(1060,"w") and x<=ajuste_res(1120,"w") and y>=ajuste_res(690,"h") and y<=ajuste_res(850,"h") :
                if musica :
                    background.stop()
                    musica=False
                    ultimo_click = timer()
                elif not(musica) :
                    background.play(-1)
                    musica=True
                    ultimo_click = timer()
            elif x>=ajuste_res(850,"w") and x<=ajuste_res(1050,"w") and y>=ajuste_res(880,"h") and y<=ajuste_res(960,"h") :
                config.set('settings','som',str(som))
                config.set('settings','musica',str(musica))
                config.write(open('config.ini','w+'))
                print("Você fez", pontos, "pontos! Parabéns")
                sys.exit()
        tela.blit(fundomenu, bordafundomenu)
        tela.blit(textostatus,(ajuste_res(700,"w"),ajuste_res(450,"h")))
        if musica :
            tela.blit(certo,[ajuste_res(1063,"w"),ajuste_res(695,"h")])
        if som :
            tela.blit(certo,[ajuste_res(1028,"w"),ajuste_res(800,"h")])
        pygame.display.flip()

#criar os inimigos
def gerarinimigos(nivel) :
    global velocidadeinimigos; global nivelcompleto; global jogadormorreu; global numerodescidas; global pontosstart; global pontos; global balainimigoatirando; global balaatirando
    global vinimigob; global ultimo_inimigob; global bordainimigob
    ultimo_inimigob = timer()
    vinimigob=False
    bordainimigob.x = 500
    bordainimigob.y = 100
    balaatirando=False
    inimigos.clear(); bordasinimigos.clear(); pontosinimigos.clear(); bordabalainimigo.clear(); balainimigoatirando.clear()
    horizontaltemp=ajuste_res(500,"w")
    numerodescidas = 0
    velocidadeinimigos = ajuste_res(4+(nivel*3),"w")
    for i in range(3) :
        bordabalainimigo.append(balainimigo.get_rect())
        balainimigoatirando.append(False)
    for i in range(colunas) :
        inimigos.append([])
        bordasinimigos.append([])
        pontosinimigos.append([])
    for coluna in range(colunas) :
        verticaltemp = 100
        for linha in range(linhas) :
            if (verticaltemp-100)//50 == 0 :
                inimigos[coluna].append(pygame.image.load("resources/disco voador2.png").convert_alpha())
                pontosinimigos[coluna].append(40)
            elif (verticaltemp-100)//50 == 1 or (verticaltemp-100)//50 == 2 :
                inimigos[coluna].append(pygame.image.load("resources/disco voador.png").convert_alpha())
                pontosinimigos[coluna].append(20)
            else :
                inimigos[coluna].append(pygame.image.load("resources/disco voador3.png").convert_alpha())
                pontosinimigos[coluna].append(10)
            inimigos[coluna][linha] = pygame.transform.scale(inimigos[coluna][linha], (ajuste_res(65,"w"),ajuste_res(50,"h")))
            bordasinimigos[coluna].append(inimigos[coluna][linha].get_rect())
            bordasinimigos[coluna][linha] = bordasinimigos[coluna][linha].move([horizontaltemp,verticaltemp])
            tela.blit(inimigos[coluna][linha], bordasinimigos[coluna][linha])
            verticaltemp+=ajuste_res(55,"h")
        horizontaltemp+=ajuste_res(80,"w")
    if jogadormorreu :
        pontos = pontosstart
    else :
        pontosstart = pontos
    jogadormorreu = False
    nivelcompleto = False
    bordajogador.x = pygame.display.Info().current_w/2
    bordajogador.y = pygame.display.Info().current_h-ajuste_res(150,"h")

#Criar inimigo especial
inimigob = pygame.image.load("resources/disco voadorbonus.png").convert_alpha()
inimigob = pygame.transform.scale(inimigob, (ajuste_res(80,"w"),ajuste_res(40,"h")))
bordainimigob = inimigob.get_rect()

#Carregar a bala
bala = pygame.image.load("resources/bala.png").convert_alpha()
bala = pygame.transform.scale(bala, (ajuste_res(30,"w"),ajuste_res(60,"h")))
bordabala = bala.get_rect()

balainimigo = pygame.image.load("resources/bala inimigos.png").convert_alpha()
balainimigo = pygame.transform.scale(balainimigo, (ajuste_res(30,"w"),ajuste_res(60,"h")))

ultimo_tiro = timer()
ultimo_inimigob = timer()

menu("HARDCORE SI",False)

while True:
    #Checar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: sys.exit()
        if evento.type == pygame.KEYDOWN :
            if evento.key == pygame.K_ESCAPE : menu("HARDCORE SI",True)
    pressionado = pygame.key.get_pressed()
    if pressionado[pygame.K_LEFT] :
        if not (bordajogador.left < ajuste_res(500,"w")) : bordajogador = bordajogador.move([-3,0])
    if pressionado[pygame.K_RIGHT] :
        if not (bordajogador.right>pygame.display.Info().current_w-ajuste_res(500,"w")) : bordajogador = bordajogador.move([3,0])
    if pressionado[pygame.K_UP] :
        if not(balaatirando) :
            if (tempoatual-ultimo_tiro) > 0.4 :
                if som : tiro.play(1)
                balaatirando=True
                bordabala.x = bordajogador.x+18
                bordabala.y = bordajogador.y-50
    #Testar se é necessário gerar um novo nível
    if nivelcompleto or jogadormorreu :
        if nivelcompleto and nivel>int(config.get('settings','niveis')) :
            menu("VOCÊ GANHOU", False)
            continue
        if jogadormorreu and vidas==0 :
            menu("PERDEU KKKK", False)
        gerarinimigos(nivel)

    if numerodescidas == 3 and velocidadeinimigos == ajuste_res(4+(nivel*3),"w") :
        velocidadeinimigos+=1
    elif numerodescidas==7 and velocidadeinimigos == ajuste_res(5+(nivel*3),"w") :
        velocidadeinimigos+=1
    elif numerodescidas==9 and velocidadeinimigos == ajuste_res(6+(nivel*3),"w") :
        velocidadeinimigos+=1
    elif numerodescidas==11 and velocidadeinimigos == ajuste_res(7+(nivel*3),"w") :
        velocidadeinimigos+=1

    tempoatual = timer()

    #Inimigo Bonus
    if numerodescidas > 1 and (tempoatual-ultimo_inimigob)>10:
        if random.randint(0,1000) == 44 :
            vinimigob = True
            ultimo_inimigob = timer()
    #Bala do inimigo
    for i in range(len(bordabalainimigo)) :
        if not(balainimigoatirando[i]) :
            balainimigoatirando[i] = True
            for z in range(5) :
                temp = random.randint(0,len(bordasinimigos)-1)
                if (temp!=lasttemp-1 and temp!=lasttemp+1 and temp!=lasttemp and temp!=lasttemp2-1 and temp!=lasttemp2+1 and temp!=lasttemp2) or len(bordasinimigos)<5 :
                    break
            bordabalainimigo[i].x = bordasinimigos[temp][-1].x
            bordabalainimigo[i].y = bordasinimigos[temp][-1].y
            lasttemp = temp
            lasttemp2 = lasttemp

    #Checar bala
    if balaatirando :
        bordabala.move_ip([0,ajuste_res(-10,"h")])
        if bordabala.top<=100 :
            bordabala.move_ip([-500,-500])
            balaatirando=False
            ultimo_tiro = timer()
    for i in range(len(bordabalainimigo)) :
        if balainimigoatirando[i] :
            bordabalainimigo[i].move_ip([0,vbalainimigo])
            if bordabalainimigo[i].bottom>=pygame.display.Info().current_h-ajuste_res(100,"h") :
                balainimigoatirando[i] = False
                if len(bordasinimigos)==6 and len(bordabalainimigo)==3 :
                    del bordabalainimigo[i]
                    del balainimigoatirando[i]
                    break
                elif len(bordasinimigos)==2 and len(bordabalainimigo)==2 :
                    del bordabalainimigo[i]
                    del balainimigoatirando[i]
                    break
            elif bordabalainimigo[i].colliderect(bordajogador) :
                vidas-=1
                jogadormorreu = True

        #Colisão com inimigos
        for coluna in range(len(inimigos)) :
            for linha in range(len(inimigos[coluna])) :
                if bordabala.colliderect(bordasinimigos[coluna][-1]) and balaatirando:
                    pontos+=pontosinimigos[coluna][-1]
                    if len(bordasinimigos[coluna]) == 1 :
                        del inimigos[coluna]
                        del bordasinimigos[coluna]
                        del pontosinimigos[coluna]
                        balaatirando=False
                        ultimo_tiro = timer()
                        breakar = True
                        if len(inimigos)==0 :
                            nivel+=1
                            vidas+=1
                            vbalainimigo+=1
                            nivelcompleto = True
                        break
                    else :
                        del inimigos[coluna][-1]
                        del bordasinimigos[coluna][-1]
                        del pontosinimigos[coluna][-1]
                        balaatirando=False
                        ultimo_tiro = timer()
                        breakar = True
                        break
            if breakar :
                break
        if vinimigob :
            if bordabala.colliderect(bordainimigob) :
                vinimigob = False
                bordainimigob.x = ajuste_res(500,"w")
                bordainimigob.y = 100
                pontost = random.randint(30,60)
                if pontost>=30 and pontost<=35 : pontos+=30
                elif pontost>35 and pontost<=45 : pontos+=40
                elif pontost>45 and pontost<=55 : pontos+=50
                else : pontos+=40

    if nivelcompleto : continue

    #Mover os inimigos
    if move == 80 :
        for coluna in range(len(inimigos)) :
            for linha in range(len(inimigos[coluna])) :
                bordasinimigos[coluna][linha] = bordasinimigos[coluna][linha].move(velocidadeinimigos,0)
        move=0
    if vinimigob :
        bordainimigob.move_ip(1,0)

    #Checar Bordas
    if bordasinimigos[0][0].left < ajuste_res(500,"w") or bordasinimigos[-1][-1].right > pygame.display.Info().current_w-ajuste_res(500,"w"):
        numerodescidas += 1
        velocidadeinimigos = -velocidadeinimigos
        for coluna in range(len(inimigos)) :
            for linha in range(len(inimigos[coluna])) :
                bordasinimigos[coluna][linha] = bordasinimigos[coluna][linha].move([velocidadeinimigos,25])
    if bordainimigob.left < ajuste_res(500,"w") or bordainimigob.right>pygame.display.Info().current_w-ajuste_res(500,"w") :
        vinimigob = False
        bordainimigob.x = ajuste_res(500,"w")
        bordainimigob.y = 100
    maiorn = 0
    maiorc = 0
    for coluna in range(len(bordasinimigos)) :
        if len(bordasinimigos[coluna]) > maiorn :
            maiorn = len(bordasinimigos[coluna])
            maiorc = coluna
    if bordasinimigos[maiorc][-1].y >= bordajogador.y :
        vidas-=1
        jogadormorreu = True

    move+=1

    #Atualizar a tela
    tela.blit(fundo, bordafundo)
    numeropontos = arial.render(str(pontos), True, (255,255,255))
    numeronivel = arial.render(str(nivel), True, (255,255,255))
    tela.blit(textopontos,(ajuste_res(1100,"w"),ajuste_res(12,"h")))
    tela.blit(numeropontos,(ajuste_res(1300,"w"),ajuste_res(12,"h")))
    tela.blit(textonivel, (ajuste_res(470,"w"),ajuste_res(12,"h")))
    tela.blit(numeronivel, (ajuste_res(645,"w"),ajuste_res(12,"h")))
    temp=ajuste_res(500,"w")
    for i in range(vidas) :
        tela.blit(jogador,[temp, pygame.display.Info().current_h-ajuste_res(62,"h")])
        temp+=ajuste_res(100,"w")
    for coluna in range(len(inimigos)) :
        for linha in range(len(inimigos[coluna])) :
            tela.blit(inimigos[coluna][linha], bordasinimigos[coluna][linha])
    tela.blit(jogador,bordajogador)
    if balaatirando : tela.blit(bala,bordabala)
    for i in range(len(bordabalainimigo)) :
        if balainimigoatirando[i] :
            tela.blit(balainimigo, bordabalainimigo[i])
    if vinimigob : tela.blit(inimigob,bordainimigob)
    pygame.display.flip()

    breakar = False
