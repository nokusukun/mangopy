import numpy as np

class Layout:
  """
  Layout(width, height, *anchorWidth, *anchorHeight, *fill)
    Parameters
      width int: layout width
      height int: layout height
      achrowWidth int: layout width position from the parent
        optional, default: 0
      anchorHeight int: layout height position from the parent
        optional, default: 0
  """
  def __init__(self, w, h, anchorw = 0, anchorh = 0, fill = ' '):
    self.__dict__.update({
      'width': w,
      'height': h,
      'anchorw': anchorw,
      'anchorh': anchorh,
      'fill': fill,
    })
    self.initalize()
    self.ignoreOverflow = True
    self.underData = None
    self.parent = None
    self.isAttached = False

  def initalize(self):
    self.cursorPos = [0, 0]
    self.shadowBuff = [[self.fill for x in range(
        self.width)] for y in range(self.height)]
    self.renderables = []
    self.components = []

  def _is_overflow(self, y, x):
    if y >= self.height or x >= self.width:
      return True
    return False

  def write_char(self, data, direction='x', diffpos=None, CJK=False):
    direction = 0 if direction == "x" else 1
    pos = self.cursorPos if diffpos is None else diffpos

    if direction == 1 and diffpos is None:
      if self._is_overflow(*pos):
        self.cursorPos = [0, pos[1] + 1]
      else:
        self.cursorPos = [pos[0] + 1, pos[1]]

    elif direction == 0 and diffpos is None:
      if self._is_overflow(*pos):
        self.cursorPos = [pos[0] + 1, 0]
      else:
        self.cursorPos = [pos[0], pos[1] + 1]

    try:
      self.shadowBuff[pos[0]][pos[1]] = data
      if CJK and direction == 0:
        self.write_char('')
    except:
      if not self.ignoreOverflow:
        raise Exception(f'Attempting to write outside of buffer. {pos} -> {[self.conHeight - 1, self.conWidth - 1]}')

  def write_string(self, data, direction='x', CJK=False):
    for char in data:
      self.write_char(char, direction, None, CJK)


  def attachTo(self, parent):
    parent.components.append(self)
    getattr(self, 'onAttach', lambda x: True)(parent)
    self.isAttached = True


  def drawTo(self, driver):
    if hasattr(self, 'beforeRender') and not self.isAttached:
      self.beforeRender()
    for rendable in self.renderables:
      rendable(self)
    for component in self.components:
      getattr(component, 'beforeRender', lambda: True)()
      component.drawTo(self)

    try: 
      anchorHeight, anchorWidth = self.anchorh, self.anchorw
      buffer = np.asarray(self.shadowBuff)
      parentBuffer = np.asarray(driver.shadowBuff)
      self.underData = parentBuffer[anchorHeight:anchorHeight +
                                    buffer.shape[0], anchorWidth:anchorWidth + buffer.shape[1]].tolist()
      parentBuffer[anchorHeight:anchorHeight + buffer.shape[0], anchorWidth:anchorWidth + buffer.shape[1]] = buffer

      driver.shadowBuff = parentBuffer.tolist()
    except ValueError:
      print(f'')
      raise Exception(f'Layout misfit: Parent{driver.width, driver.height}:S{np.asarray(driver.shadowBuff).shape} layout is smaller than Child{self.width, self.height}:S{np.asarray(self.shadowBuff).shape}.\nAnchors: {self.anchorh, self.anchorw}')


  def draw(self):
    if self.parent:
      self.drawTo(self.parent)
      self.parent.draw()
      if hasattr(self, 'afterRender'):
        self.afterRender()
      for rendable in self.renderables:
        rendable(self)
      for component in self.components:
        getattr(component, 'afterRender', lambda: True)()

      

  def undrawTo(self, driver):
    if self.underData is not None:
      anchorHeight, anchorWidth = self.anchorh, self.anchorw
      buffer = np.asarray(self.underData)
      parentBuffer = np.asarray(driver.shadowBuff)
      parentBuffer[anchorHeight:anchorHeight + buffer.shape[0],
                   anchorWidth: anchorWidth + buffer.shape[1]] = buffer
      driver.shadowBuff = parentBuffer.tolist()
