import sys
import requests
import os
import pygame


class Map:
    def __init__(self, zoom):
        toponym_to_find = " ".join(sys.argv[1:])
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            pass
        json_response = response.json()

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        self.toponym_longitude, self.toponym_lattitude = toponym_coodrinates.split(" ")

        map_params = {
            "ll": ",".join([self.toponym_longitude, self.toponym_lattitude]),
            "l": "map",
            "pt": ",".join([self.toponym_longitude, self.toponym_lattitude, 'pm2rdm']),
            "z": str(zoom)
        }
        response = requests.get(map_api_server, params=map_params)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def mach_coor(self, zoom, pos='', mash="map"):
        toponym_to_find = ",".join([self.toponym_longitude, self.toponym_lattitude])
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            pass

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        if pos == 'left' and float(self.toponym_longitude) > -180:
            self.toponym_longitude = str(float(self.toponym_longitude) - 0.0005)
        elif pos == 'right' and float(self.toponym_longitude) < 180:
            self.toponym_longitude = str(float(self.toponym_longitude) + 0.0005)
        elif pos == 'down' and float(self.toponym_lattitude) > -90:
            self.toponym_lattitude = str(float(self.toponym_lattitude) - 0.0005)
        elif pos == 'up' and float(self.toponym_lattitude) < 90:
            self.toponym_lattitude = str(float(self.toponym_lattitude) + 0.0005)

        map_params = {
            "ll": ",".join([self.toponym_longitude, self.toponym_lattitude]),
            "l": str(mash),
            "z": str(zoom)
        }
        response = requests.get(map_api_server, params=map_params)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        return self.map_file



zoom = 16
pos = ''
pygame.init()
pygame.font.init()
mash = "map"
mp = Map(zoom)
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(mp.mach_coor(zoom)), (0, 0))
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 8 <= x <= 43 and 8 <= y <= 28:
                mash = "map"
            elif 8 <= x <= 43 and 55 <= y <= 75:
                mash = "sat"
            elif 8 <= x <= 43 and 102 <= y <= 122:
                mash = "sat,skl"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                zoom += 1
                if zoom >= 19:
                    zoom = 19
            elif event.key == pygame.K_PAGEDOWN:
                zoom -= 1
                if zoom <= 10:
                    zoom = 10
            elif event.key == pygame.K_DOWN:
                pos = 'down'
            elif event.key == pygame.K_UP:
                pos = 'up'
            elif event.key == pygame.K_RIGHT:
                pos = 'right'
            elif event.key == pygame.K_LEFT:
                pos = 'left'
    screen.blit(pygame.image.load(mp.mach_coor(zoom, pos, mash=mash)), (0, 0))
    pygame.draw.rect(screen, 'gray', (8, 8, 50, 20))
    font_type = pygame.font.Font(None, 17)
    text = font_type.render('схема', True, (255, 255, 255))
    screen.blit(text, (10, 11))
    pygame.draw.rect(screen, 'gray', (8, 55, 50, 20))
    font_type = pygame.font.Font(None, 17)
    text = font_type.render('спутник', True, (255, 255, 255))
    screen.blit(text, (10, 57))
    pygame.draw.rect(screen, 'gray', (8, 102, 50, 20))
    font_type = pygame.font.Font(None, 17)
    text = font_type.render('гибрид', True, (255, 255, 255))
    screen.blit(text, (10, 105))
    pos = ''
    pygame.display.flip()
pygame.quit()
os.remove(mp.mach_coor(zoom))