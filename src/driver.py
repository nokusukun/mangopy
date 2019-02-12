import sys
import copy

from .utils import con_dimension, cursor

class ConsoleDriver:

  def __init__(self, **kwargs):
    self.specialCharacterMode = kwargs.get('specialCharacterMode', False)
    self.ignoreOverflow = kwargs.get('ignoreOverflow', False)
    self.historyLength = kwargs.get('historyLength', 10)
    self.history = []
    self._generate_layout()

  def __enter__(self):
    cursor.hide_cursor()
    cursor.clear()
    return self
  
  def __exit__(self, * args):
    cursor.show_cursor()
    pass

  def _generate_layout(self):
    self.conWidth, self.conHeight = con_dimension.get_terminal_size()  # Y = Width, X = Height
    self.shadowBuff = [[' ' for x in range(self.conWidth - 1 if self.specialCharacterMode else self.conWidth)] for y in range(self.conHeight)]
    self.renderedBuffer = copy.deepcopy(self.shadowBuff)
    self.cursorPos = [0, 0]
  
  @property
  def width(self):
    return self.conWidth

  @property
  def height(self):
    return self.conHeight

  def _con_write(self, data):
    sys.stdout.write(data)

  
  def _con_move(self, y, x):
    return "\033[%d;%dH" % (y, x)


  def _is_overflow(self, y, x):
    if y >= self.conHeight or x >= self.conWidth:
      return True
    return False


  def optimizedDraw(self):
    # a = [[1,2,3], 
    #      [4,5,6], 
    #      [7,8,9]]
    # b = [[1, ,3], 
    #      [4, ,6], 
    #      [7, , ]]
    # [(i,j) for i, row in enumerate(a) for j, x in enumerate(row) if b[i][j] != x]
    # [(0, 1), (1, 1), (2, 1), (2, 2)]
    changeMap = [self._con_move(i, j) + self.shadowBuff[i][j] for i, row in enumerate(self.renderedBuffer)
                 for j, x in enumerate(self.shadowBuff) if self.renderedBuffer[i][j] != x]
    print(changeMap)
    return "".join(changeMap)


  def draw(self):
    self._con_write(self._con_move(0, 0))
    self._con_write(self.transform_shadow(self.renderedBuffer))
    #self._con_write(self.optimizedDraw())
    self.renderedBuffer = copy.deepcopy(self.shadowBuff)
    

  def write_char(self, data, direction='x', diffpos=None, CJK = False):
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

  def transform_shadow(self, shadow):
    return "\n".join( "".join(x for x in y) for y in shadow)

