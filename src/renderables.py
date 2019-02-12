
def TitleBar(title, position):
  def renderTitleBar(layout):
    safeWidth = layout.width - 2
    if position == 'left':
      layout.cursorPos = [0, 2]
    elif position == 'center':
      layout.cursorPos = [0, int(layout.width / 2) - int((len(title) + 2) / 2)]
    elif position == 'right':
      layout.cursorPos = [0, layout.width - (len(title) + 2)]
    layout.write_string(f'[{title}]')

  return renderTitleBar

def Text(text, **kwargs):
  def renderText(layout):
    offsetH = kwargs.get('horizontalOffset', 0)
    offsetV = kwargs.get('verticalOffset', 0)
    positionV = kwargs.get('vertical', 'left')
    positionH = kwargs.get('horizontal', 'top')
    horizon = {
      'top': 0 + offsetH,
      'center': int(layout.height / 2) + offsetH,
      'bottom': (layout.height - 1) + offsetH
    }
    vertical = {
      'left': 0 + offsetV,
      'center': (int(layout.width / 2) - int(len(text) / 2)) + offsetV,
      'right': layout.width - len(text) + offsetV,
    }
    layout.cursorPos = [horizon[positionH], vertical[positionV]]
    layout.write_string(text)
  return renderText


def CenteredText(text, offset=0):
  def renderCenteredText(layout):
    Text(text, horizontal='center', vertical='center', horizontalOffset=offset)(layout)

  return renderCenteredText

def Border():
  def renderBorder(layout):
    for i in range(0, layout.width):
      try:
        layout.shadowBuff[0][i] = '─'
        layout.shadowBuff[-1][i] = '─'
      except:
        raise Exception(f'W{layout.width}:{i} H{layout.height}')

    for i in range(0, layout.height):
      layout.shadowBuff[i][0] = '│'
      layout.shadowBuff[i][-1] = '│'
    
    layout.shadowBuff[0][0] = '┌'
    layout.shadowBuff[0][-1] = '┐'
    layout.shadowBuff[-1][0] = '└'
    layout.shadowBuff[-1][-1] = '┘'
  return renderBorder


def BorderDouble():
  def renderBorder(layout):
    for i in range(0, layout.width):
      layout.shadowBuff[0][i] = '═'
      layout.shadowBuff[-1][i] = '═'

    for i in range(0, layout.height):
      layout.shadowBuff[i][0] = '║'
      layout.shadowBuff[i][-1] = '║'

    layout.shadowBuff[0][0] = '╔'
    layout.shadowBuff[0][-1] = '╗'
    layout.shadowBuff[-1][0] = '╚'
    layout.shadowBuff[-1][-1] = '╝'
  return renderBorder


def BorderThick():
  def renderBorder(layout):
    for i in range(0, layout.width):
      layout.shadowBuff[0][i] = '█'
      layout.shadowBuff[-1][i] = '█'

    for i in range(0, layout.height):
      layout.shadowBuff[i][0] = '█'
      layout.shadowBuff[i][-1] = '█'

    layout.shadowBuff[0][0] = '█'
    layout.shadowBuff[0][-1] = '█'
    layout.shadowBuff[-1][0] = '█'
    layout.shadowBuff[-1][-1] = '█'
  return renderBorder

def CenterTo(parent):
  def modifyCenterToParent(layout):
    layout.anchorw = int(parent.width / 2) - int(layout.width / 2)
    layout.anchorh = int(parent.height / 2) - int(layout.height / 2)
  return modifyCenterToParent

def RenderTo(parent):
  def renderToParent(child):
    child.drawTo(parent)
  return renderToParent

def PositionFor(parent, **kwargs):
  def positionLayout(layout):
    offsetH = kwargs.get('horizontalOffset', 0)
    offsetV = kwargs.get('verticalOffset', 0)
    positionV = kwargs.get('vertical', 'left')
    positionH = kwargs.get('horizontal', 'top')
    horizon = {
      'top': 0 + offsetH,
      'center': int(int(parent.height / 2) - int(layout.height / 2)) + offsetH,
      'bottom': int(parent.height - layout.height) + offsetH
    }
    vertical = {
      'left': 0 + offsetV,
      'center': (int(parent.width / 2) - int(layout.width / 2)) + offsetV,
      'right': parent.width - layout.width + offsetV,
    }
    layout.anchorh = horizon[positionH]
    layout.anchorw = vertical[positionV]
  return positionLayout


def MoveToTop(parent, child):
  index = parent.components.index(child)
  parent.components.append(parent.components.pop(index))
