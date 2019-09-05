from PIL import Image
import os
import re
import cv2
import math
import numpy as np

def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

def replace(string, char):
    pattern = char + '{2,}'
    string = re.sub(pattern, ',', string)
    return string

def rotate(origin, point, angle):
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

########--------Wczytanie danych--------#########



#myCmd = os.popen('nmcli dev wifi > ~/PycharmProjects/Help_App/new_WiFi2.txt').read()
#print(myCmd)
freq = 2400
fo = open("wifi.txt", "r")
item = fo.readlines()

signal_str = []
for x in range(len(item)):
    # Driver code
    if x == 0:
        continue
    string = item[x]
    char = ' '
    new_str = replace(string, char)
    tab = new_str.split(',')
    #print(tab[5])
    signal_str.append(tab[5])
    #print(signal_str)

########--------Obliczenie odleglosci od routera--------#########


radius_list = []
for y in range(len(signal_str)):
    print('Moc routera wynosi : ', signal_str[y] + '%')
    signal = int(signal_str[y])

    r_dist = math.pow( 10, ((27.55 - (20 * math.log10( freq )) +  signal)/20))
    print('Promien wynosi :', r_dist)

    #if signal >= 90 :
    #    radius = 2
    #elif signal >= 80:
    #    radius = 4
    #elif signal >= 70:
    #    radius = 6
    #elif signal >= 60:
    #    radius = 8
    #elif signal >= 50:
    #    radius = 10
    #elif signal >= 40:
    #    radius = 12
    #elif signal >= 30:
    #    radius = 14
    #elif signal >= 20:
    #    radius = 16
    #elif signal >= 10:
    #    radius = 18
    #elif signal >= 0:
    #    radius = 20
    #print('Promien wynosi : ', radius, 'm')


    radius_list.append(r_dist)
    #radius_list.append(radius)
# #print(radius_list)



########--------Wczytenie obrazu--------########



basewidth = 500
img2 = Image.open('plan_skladu_przyklad.png')
print(img2.size[0])
wpercent = (basewidth/float(img2.size[0]))
print(wpercent)
hsize = int((float(img2.size[1])*float(wpercent)))
print(img2.size[1])
img2 = img2.resize((basewidth,hsize), Image.ANTIALIAS)
img2.save('sompic.png')
img3 = Image.open('sompic.png')
#img3.show()

image = cv2.imread('sompic.png')



########--------Rysowanie na obrazie--------########



router_position = [[6, 263],[115, 6],[400,28],[400,329],
                   [(int(basewidth/2)),(int(hsize/2))],[27,28]]
print(radius_list)

for x in range(len(radius_list)):
    radius = int( radius_list[x] )
    y = 0
    cv2.circle(image, (router_position[x][y],router_position[x][y+1]), radius, (0,0,255), 1)



########--------Sprawdzenie odleglosci pomiedzy routerami--------########


for x in range(len(radius_list)):
    for y in range(len(radius_list)):
        if x == y:
            continue

        z = 0
        x1 = router_position[x][z]
        y1 = router_position[x][z+1]
        x2 = router_position[y][z]
        y2 = router_position[y][z+1]
        router_dist = calculateDistance(x1, y1, x2, y2)
        radius_sum = ( radius_list[x] + radius_list[y] )
        #router_dist =  (router_position[x] - router_position[y])
        if router_dist > radius_sum:
            print("Brak punktow wspolnych", x, y, "Dystans:", router_dist, "Promienie:", radius_sum)
        elif router_dist == radius_sum:
            print("Jest jeden punkt wspolny", x, y, "Dystans:", router_dist,"Promienie:", radius_sum)
            u1 = x2 - x1
            u2 = y2 - y1
            scale = np.true_divie(radius_list[x], router_dist)
            u11 = u1 * scale
            u22 = u2 * scale
            xp = x1 + u11
            yp = y1 + u22
            cv2.circle(image, (int(xp), int(yp)), 1, (255, 0, 0), -1)
        elif router_dist < radius_sum:
            print("Wiecej niz jeden punkt wspolny", x, y, "Dystans:", router_dist, "Promienie:", radius_sum)
            dAB = router_dist
            dAC = radius_list[x]
            dBC = radius_list[y]
            angle = np.arctan2(y2-y1,x2-x1)
            xp = np.true_divide(dAB ** 2 + dAC ** 2 - dBC ** 2, 2 * dAB)
            d1 = dAB + dAC + dBC
            d2 = abs(dAB + dAC - dBC)
            d3 = abs(dAB - dAC + dBC)
            d4 = abs(-dAB + dAC + dBC)
            yp = np.true_divide(math.sqrt(d1 * d2 * d3 * d4), 2 * dAB)
            xpp, ypp = rotate((0,0), (xp,yp), angle)
            xppp, yppp1= xpp + x1, ypp + y1
            print("Wspolrzedne: " + "( " + str(xppp) + ", " + str(yppp1) + " )")
            cv2.circle(image, (int(xppp), int(yppp1)), 1, (255, 0, 0), -1)

#circle(image (X,Y of Router), radius, (color of dot), thickness)

cv2.imshow('Test image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#print(basewidth, wpercent, hsize, img2.size[0], img2.size[1])

