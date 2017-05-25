import pygame
from pygame.math import Vector2

class Player():
  """
  Because there's only one square, I've called it 'Player'.
  It would be a good idea to abstract this away further and call it 
  GameObject
  """
  def __init__(self, color, position, game):
    self.color = color
    self.position = position
    self.game = game
  def draw(self):
    """
    Draw to the screen. Still needs a bit of work to be less "custom"
    inside of this method.
    """
    self.game.pygame.draw.rect(
      self.game.display, 
      self.color,
      [self.position.x, self.position.y, 70, 70]
    )
  def onEvent(self, event):
    """
    Handle key press events!
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            self.position.x -= 10
        if event.key == pygame.K_d:
            self.position.x += 10
        if event.key == pygame.K_w:
            self.position.y -= 10
        if event.key == pygame.K_s:
            self.position.y += 10
  def update(self):
    """
    Currently doesn't need any additional logic. We can change this 
    in the future :)
    """
    pass

class Game():
  """
  The game class is responsible for:
  1. ticking (telling each game object to update itself)
  2. drawing (telling each game object to draw itself)
  3. events  (telling each game object when an event has occurred) 

  """

  def __init__(self, pygame):
    """
    Initialize the game object. Set up the display, clock, and
    give it a reference to the overall pygame object. This allows
    you to call pygame only once, and have game objects only use 
    pygame when completely necessary.
    """
    self.pygame = pygame
    self.pygame.init()
    self.display = self.pygame.display.set_mode((500,500))
    self.pygame.display.set_caption('SquareExcercise')
    self.clock = pygame.time.Clock()
    self.players = []
    self.exit = False

  def draw(self):
    """
    Draw the background, and loop through all game objects to draw
    them on the screen
    """
    gold = (212, 175, 55)
    self.display.fill(gold, rect=None, special_flags=0)
    for player in self.players:
      player.draw()
    pygame.display.update()

  def handleEvents(self):
    """
    If any events occur, notify all game objects what happened. If there are
    a lot of game objects, optimize this so that events are only called on
    objects that matter
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.exit = True
        for player in self.players:
          player.onEvent(event)    

  def tick(self):
    """
    Whenever the game updates, call this method and let all game objects
    handle their events and update themselves
    """
    self.handleEvents()
    for player in players:
      player.update()
    self.draw()
    self.clock.tick(60)

  def start(self):
    """
    The game starts here! Initialize all players and append them to the
    level.
    """
    gameExit = False

    silver = (192, 192, 192)
    position = Vector2(220, 220)
    player = Player(silver, position, self)
    self.players.append(player)

    while not self.exit:
      self.tick()

    pygame.quit()

# Main method: Here's where the actual magic starts
def main():
  # Create the game object
  game = Game(pygame)

  # Separate the start of the game from the instantiation. This allows
  # you to create a method:
  # 
  # game.load()
  #
  # if loading game assets before the game starts is necessary
  game.start()

  # Upon game completion quit
  quit()

# START HERE! This only executes if you call the Python script from the
# command line. If you import the python file from somewhere else, this
# won't get called (i.e. using import squareExercise won't run this
# code below)
if __name__ == '__main__':
  main()          # I typically separate my main method to keep things clean
