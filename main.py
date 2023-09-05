from cmath import *
import pygame

def f(x):
    if x < 0.25:
        return x*8 - 1 + 1j
    elif x < 0.5:
        return 1 + (1-(x-0.25)*8) * 1j
    elif x < 0.75:
        return 1 - (x-0.5)*8 - 1j
    else:
        return -1 + ((x-0.75)*8-1) * 1j
    

# for desmos:
#    print(f"["+ ",".join([str((f(i/200).real, f(i/200).imag)) for i in range(0,200)]) +"]")

S = -30
E = 30

samples = 100
scaleFactor = 300

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

        reference = [(f(x/1000).real * scaleFactor + self.WIDTH/2, f(x/1000).imag * scaleFactor + self.HEIGHT/2) for x in range(1000)]

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.root.fill((0,0,0))

            linesStrip = [[self.WIDTH/2,self.HEIGHT/2]]
            for i, c in coefficients:
                delta = c * exp(2 * pi * i * t *  1j)
                linesStrip.append((((linesStrip[-1][0]/scaleFactor)+delta.real) * scaleFactor, ((linesStrip[-1][1]/scaleFactor)+delta.imag) * scaleFactor))

            trail.append(linesStrip[-1])

            if len(trail) > 150:
                del trail[0]

            pygame.draw.aalines(self.root, (0,0,255), True, reference)

            pygame.draw.aalines(self.root, (255,255,255), False, linesStrip)

            if len(trail) > 2:
                pygame.draw.aalines(self.root, (255,0,0), False, trail)

            pygame.display.update()
            self.clock.tick(self.FPS)
            t += 0.001
            t %= 1

    def __del__(self):
        pygame.quit()


if __name__ == "__main__":
    try:
        a = app()
        a.mainloop()
    except Exception as e:
        raise e

