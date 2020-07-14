import pygame


class PygameRenderer:
    def __init__(self):
        pygame.init()
        self._running = True
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode([360, 640])

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
        return self._running

    def render(self, frame):
        image = pygame.image.frombuffer(frame.tostring(), (360, 640), "RGB")
        self._screen.blit(image, (0, 0))
        pygame.display.update()
        self._clock.tick()
        pygame.display.set_caption('Endless Fake ({} FPS)'.format(self._clock.get_fps()))

    def shutdown(self):
        pygame.quit()
