from cmath import *
import pygame

# square
# def f(x):
#     if x < 0.25:
#         return x*8 - 1 + 1j
#     elif x < 0.5:
#         return 1 + (1-(x-0.25)*8) * 1j
#     elif x < 0.75:
#         return 1 - (x-0.5)*8 - 1j
#     else:
#         return -1 + ((x-0.75)*8-1) * 1j

curve = []

with open("path.txt","r") as f:
     data = f.read().split(" ")

for i in range(len(data)):
    if data[i] == "M":
        curve.append(["M", float(data[i+1]) + float(data[i+2]) * 1j])

    elif data[i] == "C":
        curve.append(["C", float(data[i+1]) + float(data[i+2]) * 1j, float(data[i+3]) + float(data[i+4]) * 1j, float(data[i+5]) + float(data[i+6]) * 1j])


def f(x):
    r = x*(len(curve)-1)
    ind = int(r)+1
    r %= 1

    a = curve[ind-1][-1]
    b = curve[ind][1]
    c = curve[ind][2]
    d = curve[ind][3]

    #print(a,b,c,d, r)

    return -a*(r**3) + 3*b*(r**3) + d*(r**3) - 3*c*(r**3) + 3*a*(r**2) - 6*b*(r**2) + 3*c*(r**2) - 3*a*r + 3*b*r + a

# for desmos:
#    print(f"["+ ",".join([str((f(i/200).real, f(i/200).imag)) for i in range(0,200)]) +"]")

S = -100
E = 100

samples = 10000
scaleFactor = 3

coefficients = []

for i in range(S, E+1):
    avg = 0
    for j in range(samples):
        t = j/samples
        avg += f(t) * exp(-2*pi*1j*i*t)
    avg /= samples

    coefficients.append([i, avg])

coefficients = sorted(coefficients, key = lambda obj: -abs(obj[1]))

class app():

    WIDTH,HEIGHT = 1080, 1080
    FPS = 165

    def __init__(self):
        self.running = True

        self.root = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        self.clock = pygame.time.Clock()

    def mainloop(self):

        t = 0
        trail = []
        linesStrip = [[self.WIDTH/2,self.HEIGHT/2]]

        reference = [(f(x/samples).real , f(x/samples).imag) for x in range(samples)]

        camPos = [0,0]
        camZoom = 3

        locked = False

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_f:
                        locked = not locked

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                camPos[1] -= 3/camZoom
            if keys[pygame.K_s]:
                camPos[1] += 3/camZoom
            if keys[pygame.K_d]:
                camPos[0] += 3/camZoom
            if keys[pygame.K_a]:
                camPos[0] -= 3/camZoom

            if keys[pygame.K_e]:
                camZoom *= 1.01

            elif keys[pygame.K_q]:
                camZoom /= 1.01

            self.root.fill((0,0,0))

            linesStrip = [[0,0]]
            for i, c in coefficients:
                delta = c * exp(2 * pi * i * t *  1j)
                linesStrip.append((((linesStrip[-1][0])+delta.real), ((linesStrip[-1][1])+delta.imag)))

            trail.append(linesStrip[-1])

            if locked:
                camPos = list(linesStrip[-1])

            if len(trail) > 4000:
                del trail[0]

            pygame.draw.aalines(self.root, (0,0,255), True, [((pts[0]-camPos[0])*camZoom +self.WIDTH/2 , (pts[1]-camPos[1])*camZoom +self.HEIGHT/2) for pts in reference])

            pygame.draw.aalines(self.root, (255,255,255), False, [((pts[0]-camPos[0])*camZoom +self.WIDTH/2 , (pts[1]-camPos[1])*camZoom +self.HEIGHT/2) for pts in linesStrip])

            if len(trail) > 2:
                pygame.draw.aalines(self.root, (255,0,0), False, [((pts[0]-camPos[0])*camZoom +self.WIDTH/2 , (pts[1]-camPos[1])*camZoom +self.HEIGHT/2) for pts in trail])

            pygame.display.update()
            self.clock.tick(self.FPS)
            t += 0.00025
            t %= 1

    def __del__(self):
        pygame.quit()


if __name__ == "__main__":
    try:
        a = app()
        a.mainloop()
    except Exception as e:
        raise e
