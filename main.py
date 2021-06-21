# import package math, random dan pygame
import math
import random
import pygame
# mengimport module mixer dari package pygame
from pygame import mixer

# menginisialisasi pygame
pygame.init()

# membuat layar dengan lebar x = 800 dan panjang y = 600
layar = pygame.display.set_mode((800, 600))

# membuat latar_belakang game dari gambar latar_belakang.png
latar_belakang = pygame.image.load('latar_belakang.png')

# memuat musik game dari ackground.wav
mixer.music.load("suara_latar_belakang.wav")
# memuat suara game dengan loop -1
mixer.music.play(-1)

# mengeset keterangan judul game
pygame.display.set_caption("Penjelajah Angkasa")
# memuat ikon pada game dengan gambar ikon_game.png
ikon = pygame.image.load('ikon_game.png')
pygame.display.set_icon(ikon)

# memuat gambar_pemain dari pemain.png
gambar_pemain = pygame.image.load('pemain.png')
# mengatur lokasi pemain pada sumbu x 370 dan sumbu y 480
pemain_x = 370
pemain_y = 480
pemain_x_berganti = 0

# Membuat variable gambar_musuh berbentuk array
gambar_musuh = []
# Membuat variable musuh_sumbu_x berbentuk array
musuh_sumbu_x = []
# Membuat variable musuh sumbu y berbentuk array
musuh_sumbu_y = []

# Membuat variable musuh_sumbu_x_berganti berbentuk array
musuh_sumbu_x_berganti = []
# Membuat musuh_sumbu_y_berganti berbentuk array
musuh_sumbu_y_berganti = []
# Membuat variable jumlah_musuh bernilai 6
jumlah_musuh = 6


# membuat looping berdasarkan jumlah musuh
for i in range(jumlah_musuh):
    #memuat gambar musuh dari musuh.png
    gambar_musuh.append(pygame.image.load('musuh.png'))
    musuh_sumbu_x.append(random.randint(0, 736))
    musuh_sumbu_y.append(random.randint(50, 150))
    musuh_sumbu_x_berganti.append(4)
    musuh_sumbu_y_berganti.append(40)



# peluru
# membuat gambar_peluru dari peluru.png
gambar_peluru = pygame.image.load('peluru.png')
# membuat variable peluru_x dengan nilai 0
peluru_x = 0
# membuat variable peluruY dengan nilai 480
peluru_y = 480
# membuat variable peluru_x_berganti dengan nilai 0
peluru_x_berganti = 0
peluru_y_berganti = 10
keadaaan_peluru = "siap"


# membuat variable skor dengan nilai 0
skor = 0
# membuat variable jenishuruf dengan jenis freesansbold dengan nilai 32
jenishuruf = pygame.font.Font('freesansbold.ttf', 32)

text_x = 10
text_y = 10

# Game Berakhir
# membuat variable jenishurufselesai  dengan jenis freesansbold dengan nilai 64
akhir_jenishuruf = pygame.font.Font('freesansbold.ttf', 64)


def tampil_nilai(x, y):
    skor1 = jenishuruf.render("Skor : " + str(skor), True, (255, 255, 255))
    layar.blit(skor1, (x, y))

def text_game_akhir():
    text_akhir = akhir_jenishuruf.render("GAME OVER", True, (255, 255, 255))
    layar.blit(text_akhir, (200, 250))

def pemain(x, y):
    layar.blit(gambar_pemain, (x, y))


def musuh(x, y, i):
    layar.blit(gambar_musuh[i], (x, y))


def tembak_peluru(x, y):
    global keadaaan_peluru
    keadaaan_peluru = "tembak"
    layar.blit(gambar_peluru, (x + 16, y + 10))


def ada_tambrakan(musuh_sumbu_x, musuh_sumbu_y, peluru_x, peluru_y):
    jarak = math.sqrt(math.pow(musuh_sumbu_x - peluru_x, 2) + (math.pow(musuh_sumbu_y - peluru_y, 2)))
    if jarak < 27:
        return True
    else:
        return False


# Game Loop
game_berjalan = True
while game_berjalan:

    # RGB = Red, Green, Blue
    layar.fill((0, 0, 0))
    # Gambar latar belakang
    layar.blit(latar_belakang, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_berjalan = False

        # jika keystroke ditekan periksa apakah itu kanan atau kiri
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pemain_x_berganti = -5
            if event.key == pygame.K_RIGHT:
                pemain_x_berganti = 5
            if event.key == pygame.K_SPACE:
                if keadaaan_peluru is "siap":
                    suara_peluru = mixer.Sound("suara_peluru.wav")
                    suara_peluru.play()
                    # Get the current x cordinate of the spaceship
                    peluru_x = pemain_x
                    tembak_peluru(peluru_x, peluru_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pemain_x_berganti = 0

    pemain_x += pemain_x_berganti
    if pemain_x <= 0:
        pemain_x = 0
    elif pemain_x >= 736:
        pemain_x = 736

    # Pergerakan Musuh
    for i in range(jumlah_musuh):

        # Game Berakhir
        if musuh_sumbu_y[i] > 440:
            for j in range(jumlah_musuh):
                musuh_sumbu_y[j] = 2000
            text_game_akhir()
            break

        musuh_sumbu_x[i] += musuh_sumbu_x_berganti[i]
        if musuh_sumbu_x[i] <= 0:
            musuh_sumbu_x_berganti[i] = 4
            musuh_sumbu_y[i] += musuh_sumbu_y_berganti[i]
        elif musuh_sumbu_x[i] >= 736:
            musuh_sumbu_x_berganti[i] = -4
            musuh_sumbu_y[i] += musuh_sumbu_y_berganti[i]

        # Tabrakan
        tabrakan = ada_tambrakan(musuh_sumbu_x[i], musuh_sumbu_y[i], peluru_x, peluru_y)
        if tabrakan:
            suara_tembakan = mixer.Sound("ledakan.wav")
            suara_tembakan.play()
            peluru_y = 480
            keadaaan_peluru = "siap"
            skor += 1
            musuh_sumbu_x[i] = random.randint(0, 736)
            musuh_sumbu_y[i] = random.randint(50, 150)

        musuh(musuh_sumbu_x[i], musuh_sumbu_y[i], i)

    # Bullet Movement
    if peluru_y <= 0:
        peluru_y = 480
        keadaaan_peluru = "siap"

    if keadaaan_peluru is "tembak":
        tembak_peluru(peluru_x, peluru_y)
        peluru_y -= peluru_y_berganti

    pemain(pemain_x, pemain_y)
    tampil_nilai(text_x, text_y)
    pygame.display.update()