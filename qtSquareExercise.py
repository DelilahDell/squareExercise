from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt
import sys
import asyncio
import threading
import time

class RenderObject:
  def __init__(self):
    pass
  def draw(self):
    pass

class GameWindow(QWidget):
  def __init__(self, game):
    self.game = game
    self.windowSize = Vector2(300, 300)
    super().__init__()
    self.initUI()
  def initUI(self):
    self.setGeometry(
      self.windowSize.x,
      self.windowSize.y,
      300,
      300
    )
    self.setWindowTitle("Game")
    self.show()
  def paintEvent(self, event):
    qp = QPainter()
    qp.begin(self)
    for gameObject in self.game.scene.gameObjects:
      gameObject.draw(qp)
    qp.end()
  def keyPressEvent(self, event):
    self.game.gameInput.keyPress(event.key())
  def keyReleaseEvent(self, event):
    self.game.gameInput.keyRelease(event.key())
  def closeEvent(self, event):
    self.game.running = False

class Input:
  def __init__(self, game):
    self.game = game
    self.pressedKeys = []
    self.observers = []
  def isKeyPressed(self, key):
    return key in self.pressedKeys
  def keyPress(self, key):
    if not key in self.pressedKeys:
      self.pressedKeys.append(key)
  def keyRelease(self, key):
    if key in self.pressedKeys:
      self.pressedKeys.remove(key)

class GameObject:
  def __init__(self, game):
    self.game = game
    self.position = Vector2(20, 20)
    self.velocity = .25
  def update(self):
    if self.game.gameInput.isKeyPressed(Qt.Key_W):
      self.position.y -= self.velocity * self.game.clock.delta_time
    if self.game.gameInput.isKeyPressed(Qt.Key_A):
      self.position.x -= self.velocity * self.game.clock.delta_time
    if self.game.gameInput.isKeyPressed(Qt.Key_S):
      self.position.y += self.velocity * self.game.clock.delta_time
    if self.game.gameInput.isKeyPressed(Qt.Key_D):
      self.position.x += self.velocity * self.game.clock.delta_time

  def draw(self, painter):
    painter.setBrush(Qt.blue)
    painter.drawRect(
      self.position.x,
      self.position.y, 
      100,
      100
    )
  def fixedUpdate(self):
    pass

class Vector2:
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Scene:
  def __init__(self, game):
    self.gameObjects = []
    self.game = game

class Clock:
  def __init__(self, game):
    self.game = game
    self.start_time = -1
    self.previous_time = -1
    self.next_update_time = -1
    self.previous_update = -1
    self.delta_time = 0.0
    self.fps = 40.0
    self.spf = 1.0 / self.fps
  def current_time(self):
    return int(round(time.time() * 1000))
  def start(self):
    self.start_time = self.current_time()
    self.next_update_time = self.start_time + (self.spf * 1000.0)
    self.previous_update = self.start_time
  def update(self):
    now = self.current_time()
    if (now < self.next_update_time):
      self.delta_time = now - self.previous_time
      self.previous_time = now
      return False
    frame_diff = (now - self.next_update_time) / 1000.0
    num_skipped_frames = int(frame_diff / (self.spf * 1000))
    self.next_update_time += (1 + num_skipped_frames) * (self.spf * 1000.0)
    self.previous_update = now
    self.delta_time = now - self.previous_time
    self.previous_time = now
    return True

class Game:
  def __init__(self):
    self.gameInput = Input(self)
    self.scene = Scene(self)
    self.running = True
    self.window = GameWindow(self)
    self.clock = Clock(self)
  def start(self):
    self.clock.start()
    t = threading.Thread(target=self.update)
    self.scene.gameObjects.append(GameObject(self))
    t.start()
  def update(self):
    while self.running:
      for gameObject in self.scene.gameObjects:
        gameObject.update()
      if self.clock.update():
        gameObject.fixedUpdate()
        self.window.update()

def main():
  app = QApplication(sys.argv)
  game = Game()
  game.start()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
