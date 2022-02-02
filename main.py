import sys
import requests
import os
import pygame


class Map:
    def __init__(self, zoom):
        toponym_to_find = "Москва"
        self.adress = toponym_to_find
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

    def mach_coor(self, zoom, posi=None, mash="map", place=''):
        global found, pt, begin, place2, count
        if begin:
            toponym_to_find = "Москва"
            geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": toponym_to_find,
                "format": "json"}
            response = requests.get(geocoder_api_server, params=geocoder_params)
            if not response:
                pass
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            self.toponym_longitude, self.toponym_lattitude = toponym_coodrinates.split(" ")
        elif place == '':
            toponym_to_find = ",".join([self.toponym_longitude, self.toponym_lattitude])
            geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": toponym_to_find,
                "format": "json"}
            response = requests.get(geocoder_api_server, params=geocoder_params)
            if not response:
                pass
        else:
            toponym_to_find = place
            geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": toponym_to_find,
                "format": "json"}
            response = requests.get(geocoder_api_server, params=geocoder_params)
            if not response:
                pass
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            ad = toponym["metaDataProperty"]["GeocoderMetaData"]["text"].split(',')
            ad2 = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"][2]["name"]
            try:
                self.postal_code = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
            except KeyError:
                self.postal_code = '      '
            count = 2
            if PC:
                place2 = f"{ad[0]}, {ad2}, {', '.join(ad[1:])} {self.postal_code}"
            else:
                place2 = f"{ad[0]}, {ad2}, {', '.join(ad[1:])}"
            self.toponym_longitude, self.toponym_lattitude = toponym_coodrinates.split(" ")
            found = False
            pt = "{0},pm2dgl".format(",".join([self.toponym_longitude, self.toponym_lattitude]))
        if PC:
            if place2 != '' and self.postal_code not in place2:
                place2 += ' ' + str(self.postal_code)
        if not PC:
            if place2 != '' and self.postal_code in place2:
                place2 = place2[:-6]
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
                "z": str(zoom),
                "pt": pt
            }

        response = requests.get(map_api_server, params=map_params)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        begin = False
        return self.map_file


zoom = 16
place = ''
place2 = ''
pos = ''
pt = ''
begin = False
found = False
need_input = False
PC = False
count = 0
pygame.init()
input_rect = pygame.Rect(8, 400, 300, 35)
border_rect = pygame.Rect(7, 399, 302, 37)
input_rect2 = pygame.Rect(8, 6, 580, 25)
border_rect2 = pygame.Rect(7, 5, 582, 27)
color = [(107, 142, 35), 'gray', 'gray']
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
            if 311 <= x <= 381 and 400 <= y <= 435 and place != '':
                need_input = False
                found = True
            if 8 <= x <= 308 and 405 <= y <= 435:
                need_input = True
            if 385 <= x <= 455 and 410 <= y <= 445:
                pt = ''
                place = ''
                place2 = ''
                begin = True
            if 461 <= x <= 541 and 400 <= y <= 435:
                if not PC:
                    PC = True
                else:
                    PC = False
            if 518 <= x <= 578 and 400 <= y <= 435:
                PC = False
            if 8 <= x <= 58 and 50 <= y <= 70:
                mash = "map"
                color[0], color[1], color[2] = (107, 142, 35), 'gray', 'gray'
            elif 8 <= x <= 58 and 90 <= y <= 110:
                mash = "sat"
                color[0], color[1], color[2] = 'gray', (107, 142, 35), 'gray'
            elif 8 <= x <= 58 and 130 <= y <= 150:
                mash = "sat,skl"
                color[0], color[1], color[2] = 'gray', 'gray', (107, 142, 35)
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
            if need_input:
                if event.key == pygame.K_BACKSPACE:
                    place = place[:-1]
                else:
                    place += event.unicode
    if not found:
        screen.blit(pygame.image.load(mp.mach_coor(zoom, posi=pos, mash=mash)), (0, 0))
    else:
        screen.blit(pygame.image.load(mp.mach_coor(zoom, posi=pos, mash=mash, place=place)), (0, 0))
    pygame.draw.rect(screen, color[0], (8, 50, 50, 20))
    font_type = pygame.font.Font(None, 17)
    text = font_type.render('схема', True, (255, 255, 255))
    screen.blit(text, (10, 53))
    pygame.draw.rect(screen, color[1], (8, 90, 50, 20))
    font_type = pygame.font.Font(None, 17)
    text = font_type.render('спутник', True, (255, 255, 255))
    screen.blit(text, (10, 93))
    pygame.draw.rect(screen, color[2], (8, 130, 50, 20))
    font_type = pygame.font.Font(None, 17)
    text = font_type.render('гибрид', True, (255, 255, 255))
    screen.blit(text, (10, 133))
    pygame.draw.rect(screen, (255, 215, 0), (311, 400, 70, 35))
    font_type = pygame.font.Font(None, 23)
    text = font_type.render('искать', True, (0, 0, 0))
    screen.blit(text, (318, 408))
    pygame.draw.rect(screen, (128, 128, 0), border_rect)
    pygame.draw.rect(screen, (255, 255, 255), input_rect)
    font_type = pygame.font.Font(None, 20)
    text = font_type.render(str(place), True, (0, 0, 0))
    screen.blit(text, (15, 409))
    pygame.draw.rect(screen, "gray", (385, 400, 70, 35))
    font_type = pygame.font.Font(None, 23)
    text = font_type.render('сброс', True, (0, 0, 0))
    screen.blit(text, (395, 410))
    pygame.draw.rect(screen, (128, 128, 0), border_rect2)
    pygame.draw.rect(screen, (255, 255, 255), input_rect2)
    font_type = pygame.font.Font(None, 15)
    text = font_type.render(str(place2), True, (0, 0, 0))
    screen.blit(text, (10, 13))
    pygame.draw.rect(screen, (32, 178, 170), (461, 400, 80, 35))
    font_type = pygame.font.Font(None, 20)
    text = font_type.render('PC/NO PC', True, (0, 0, 0))
    screen.blit(text, (471, 410))
    pos = ''
    pygame.display.flip()
pygame.quit()
os.remove(mp.mach_coor(zoom))