import math
import random

from .layout import Layout
from . import renderables

class Window(Layout):

  def __init__(self, *args):
    super().__init__(*args)
    self.title = 'Window'
    self.titlePosition = 'center'
    self.border = True
    self.content = Layout(args[0] - 2, args[1] - 2, 1, 1)

  def initalize(self):
    super().initalize()
    self.content = Layout(self.height - 2, self.width - 2, 1, 1)

  def beforeRender(self):
    if self.border:
      renderables.Border()(self)
    renderables.TitleBar(self.title, self.titlePosition)(self)


class SineBox(Window):

  def __init__(self, name, *args, **kwargs):
    super().__init__(*args)
    self.name = name
    self.pixel = Layout(len(name) + 2, 3, 0, 0)
    self.pixel.renderables.extend([
        renderables.Border(),
        renderables.CenteredText(name)
    ])
    self.sineVal = 0
    self.hasRendered = False
    self.a = random.random() * 0.3
    self.b = random.random() * 0.3
    self.c = random.random() * 0.3
    self.d = random.random() * 0.3
    self.sineBarH = ProgressBar(self.height, 0, self.width - 2, 1, 1, 1)
    self.sineBarH.label = 'SineH: '
    self.components.append(self.sineBarH)

    self.sineBarW = ProgressBar(self.height, 0, self.width - 2, 1, 1, 2)
    self.sineBarW.label = 'SineW: '
    self.components.append(self.sineBarW)
    self.components.append(self.pixel)
    

  def onAttach(self, parent):
    if self.height >= parent.height:
      self.height = parent.height - self.anchorh - 1
      self.initalize()
    if self.width >= parent.width:
      self.width = parent.width - self.anchorw - 1
      self.initalize()

  def beforeRender(self):
    super().beforeRender()
    midH = int(int(self.height - 2) / 2)
    midW = int(int(self.width - (len(self.name) + 2)) / 2)
    self.pixel.anchorh = midH + (int(math.sin((self.sineVal + (self.a * self.sineVal)) * self.d) * midH))
    self.sineBarH.current_progress = self.pixel.anchorh
    self.pixel.anchorw = midW + (int(math.sin((self.sineVal + (self.b * self.sineVal)) * self.c) * midW))
    self.sineBarW.current_progress = self.pixel.anchorw
    # self.pixel.drawTo(self)


  def afterRender(self):
    self.pixel.undrawTo(self)
    # self.initalize()


class ProgressBar(Layout):

  def __init__(self, max, current, *args):
    super().__init__(*args)
    self.max = max
    self.current_progress = current
    self.progressfill = "╺"
    self.showInline = True
    self.label = ''
    self.inlineLabel = "[{bar.current_progress}/{bar.max}]"
  
  def beforeRender(self):
    self.initalize()
    progress = self.current_progress / self.max
    self.cursorPos = [0, 0]

    if self.label:
      self.write_string(self.label)

    self.write_string(self.progressfill * (int(progress * self.width) - len(self.label)))

    if self.showInline:
      inline = self.inlineLabel.format(bar=self)
      self.cursorPos = [0, int(((progress * self.width) / 2) + len(self.label))]
      self.write_string(inline)


class GameOfLife(Layout):

  def __init__(self, *args):
    super().__init__(*args)
    self.aliveBlock = 'o'
    self.deadBlock = ' '

  def populate(self):
    import random
    for x in range(len(self.shadowBuff)):
      for y in range(len(self.shadowBuff[1])):
        self.shadowBuff[x][y] = random.choice(
            [self.aliveBlock, self.deadBlock, self.deadBlock, self.deadBlock])
  
  def isDead(self, cell):
    return self.shadowBuff[cell[0]][cell[1]] == self.deadBlock

  def resurrect(self, cell):
    self.shadowBuff[cell[0]][cell[1]] = self.aliveBlock

  def kill(self, cell):
    self.shadowBuff[cell[0]][cell[1]] = self.deadBlock

  def countNeighbours(self, cell, shadowSnapshot):
    count = 0
    cx = cell[0]
    cy = cell[1]
    try:
      count += 1 if shadowSnapshot[cx + 1][cy] == self.aliveBlock else 0
    except:
      pass
    try:
      count += 1 if shadowSnapshot[cx - 1][cy] == self.aliveBlock else 0
    except:
      pass
    try:
      count += 1 if shadowSnapshot[cx][cy + 1] == self.aliveBlock else 0
    except:
      pass
    try:
      count += 1 if shadowSnapshot[cx][cy - 1] == self.aliveBlock else 0
    except:
      pass
    try:
      count += 1 if shadowSnapshot[cx + 1][cy + 1] == self.aliveBlock else 0
    except:
      pass
    try:
      count += 1 if shadowSnapshot[cx - 1][cy - 1] == self.aliveBlock else 0
    except:
      pass
    try:
      count += 1 if shadowSnapshot[cx - 1][cy + 1] == self.aliveBlock else 0
    except:
      pass
    try:
      count += 1 if shadowSnapshot[cx + 1][cy - 1] == self.aliveBlock else 0
    except:
      pass
    return count
    

  def simulateCell(self, cell, shadowSnapshot):
    neighbours = self.countNeighbours(cell, shadowSnapshot)
    if not self.isDead(cell):
      if neighbours > 3 or neighbours < 2:
        return self.kill(cell)
    else:
      if neighbours == 3:
        return self.resurrect(cell)
    
  
  def beforeRender(self): 
    shadow = [[y for y in x] for x in self.shadowBuff]
    for x in range(len(self.shadowBuff)):
      for y in range(len(self.shadowBuff[1])):
        self.simulateCell([x, y], shadow)
