import pygame
import neat
from random import randint

screenWidth = 1200
screenHeight = 600
gameMovement = -7.5
generation = 0
ground = pygame.image.load("ground.png")
ground = pygame.transform.scale(ground, (1200, 20))
groundXPos = 0
cactusLen = 0

class Dino:
    def __init__(self):
        self.velY = 0
        self.height = int(175/2)
        self.width = int(175/2)
        self.pos = [100, screenHeight - self.height]
        self.isJumping = False
        self.img = pygame.image.load("dino.png")
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
        self.alive = True
        self.points = 0

    def act(self, val):
        if val == 1:
            self.jump()

    def jump(self):
        if not self.isJumping:
            self.velY = 20
            self.isJumping = True

    def isAlive(self, obstacles):
        if not self.alive:
            return False
        playerBox = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        for cactus in obstacles:
            cactusBox = pygame.Rect(cactus.pos[0], cactus.pos[1], cactus.width, cactus.height)
            if playerBox.colliderect(cactusBox):
                self.alive = False
        return self.alive

    def getInfo(self, obstacles):
        obdist = obstacles[0].pos[0] - self.pos[0]
        if obdist < 0:
            if len(obstacles) == 1:
                obdist = 0
            else:
                obdist = obstacles[1].pos[0] - self.pos[0]
        return [obdist, obstacles[0].width, self.pos[0], self.pos[1], gameMovement]

    def getFitness(self):
        return self.points

    def draw(self, screen):
        if self.alive:
            self.pos[1] -= self.velY
            whiteHeight = 20
            whiteWidth = 20
            whiteStart = (self.pos[0] + (self.width / 2)) - whiteWidth - 7.5
            if not self.pos[1] < screenHeight - self.height:
                pygame.draw.rect(screen, (255, 255, 255), (whiteStart, self.pos[1] + self.height - whiteHeight, whiteWidth * 2, whiteHeight))
            screen.blit(self.img, self.pos)
            if self.velY > 0:
                self.velY -= 1
            if self.velY <= 0 and self.pos[1] < screenHeight - self.height:
                self.velY -= 1
            if self.pos[1] == screenHeight - self.height:
                self.velY = 0
                self.isJumping = False
        self.points += 1

class Cactus:
    def __init__(self):
        self.width = randint(2, 3) * 25
        self.height = 100
        self.pos = [screenWidth, screenHeight - self.height]
        self.img = pygame.image.load("cactus.png")
        self.img = pygame.transform.scale(self.img, (self.width, self.height))

    def isAlive(self):
        return not self.pos[0] + self.width < 0

    def draw(self, screen):
        self.pos[0] += gameMovement
        screen.blit(self.img, self.pos)

class Cloud:
    def __init__(self):
        self.width = 80
        self.height = 40
        self.img = pygame.image.load("cloud.png")
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
        self.pos = [screenWidth, randint(100, 200)]

    def onScreen(self):
        return self.pos[0] >= -1 * self.width

    def draw(self, screen):
        self.pos[0] += gameMovement
        screen.blit(self.img, self.pos)

def runGame(genomes, config):
    networks = []
    players = []

    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        networks.append(net)
        g.fitness = 0
        players.append(Dino())

    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    clock = pygame.time.Clock()
    obstacles = [Cactus()]
    clouds = [Cloud()]
    global generation
    generation += 1
    font = pygame.font.SysFont(None, 24)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        clock.tick(60)

        for i, player in enumerate(players):
            output = networks[i].activate(player.getInfo(obstacles))
            val = output.index(max(output))
            player.act(val)

        alive = 0
        for i, player in enumerate(players):
            if player.isAlive(obstacles):
                alive += 1
                genomes[i][1].fitness += player.getFitness()

        if alive == 0:
            global gameMovement
            gameMovement = -7.5
            global cactusLen
            cactusLen = 0
            break

        pygame.draw.rect(screen, (255, 255, 255), (0, 0, screenWidth, screenHeight))
        screen.blit(font.render('Generation: ' + str(generation), True, (0, 0, 0)), (20, 20))
        screen.blit(font.render('Population: ' + str(alive), True, (0, 0, 0)), (20, 40))
        screen.blit(font.render('Score: ' + str(players[0].points), True, (0, 0, 0)), (20, 60))
        screen.blit(font.render('Speed: ' + str(round(abs(gameMovement), 1)), True, (0, 0, 0)), (20, 80))

        global groundXPos
        screen.blit(ground, (groundXPos, screenHeight - 20))
        screen.blit(ground, (screenWidth + groundXPos, screenHeight - 20))
        groundXPos += gameMovement
        if(groundXPos <= -1200):
            groundXPos = 0

        obstacles = [cactus for cactus in obstacles if cactus.isAlive()]
        clouds = [cloud for cloud in clouds if cloud.onScreen()]

        if len(obstacles) != cactusLen:
            cactusLen = len(obstacles)
            gameMovement -= 0.1

        if len(obstacles) == 0:
            obstacles.append(Cactus())

        if len(clouds) == 0:
            clouds.append(Cloud())

        for cactus in obstacles:
            cactus.draw(screen)

        for cloud in clouds:
            cloud.draw(screen)

        if randint(1, 100) <= 2 and obstacles[len(obstacles) - 1].pos[0] <= (.75 - abs(gameMovement / 100)) * screenWidth:
            if abs(gameMovement) >= 12:
                if obstacles[len(obstacles) - 1].pos[0] <= (.75 - abs(gameMovement / 25)) * screenWidth:
                    obstacles.append(Cactus())
            else:
                obstacles.append(Cactus())

        if randint(1, 100) == 1:
            clouds.append(Cloud())

        for player in players:
            player.draw(screen)
        pygame.display.update()
    pygame.display.flip()

if __name__ == "__main__":
    config_path = "./config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.run(runGame, 1000)
