import sys
import requests
import os
import pygame


def mach_coor(json_response):

    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    toponym_size = toponym["boundedBy"]["Envelope"]['lowerCorner']
    toponym_size2 = toponym["boundedBy"]["Envelope"]['upperCorner']
    toponym_lowerCorner1, toponym_lowerCorner2 = toponym_size.split(" ")
    toponym_upperCorner1, toponym_upperCorner2 = toponym_size2.split(" ")

    spn1 = abs(float(toponym_lowerCorner1) - float(toponym_upperCorner1)) / 2.0
    spn2 = abs(float(toponym_lowerCorner2) - float(toponym_upperCorner2)) / 2.0
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([str(spn1), str(spn2)]),
        "l": "map"
    }
    return map_params

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
response = requests.get(map_api_server, params=mach_coor(json_response))


map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)


pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()
os.remove(map_file)