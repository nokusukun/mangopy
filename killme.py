from PIL import Image
from PIL import GifImagePlugin
from colorama import Fore
import copy

from src import driver as RenderDriver, layout, renderables, components



def test(gif):
  import time
  import arrow
  import random
  import math
  print('Opening File')
  sequence = Image.open(gif)

  with RenderDriver.ConsoleDriver(ignoreOverflow=True) as driver:
    MainLayout = layout.Layout(driver.width, driver.height, 0, 0)
    MainLayout.parent = driver
    MainLayout.renderables.extend([
        renderables.Border(),
        renderables.TitleBar('Render Driver Test', 'left'),
    ])

    statusWindow = components.Window(40, 9)
    renderables.PositionFor(
        MainLayout, horizontal='top', vertical='right', horizontalOffset=1, verticalOffset=-1)(statusWindow)
    statusWindow.title = 'Renderer Stats'
    statusWindow.attachTo(MainLayout)

    Player = components.Window(MainLayout.width - 4,  MainLayout.height - 4)
    Player.title = 'Sequence Renderer'
    renderables.PositionFor(MainLayout, horizontal='center', vertical='center')(Player)
    Player.attachTo(MainLayout)
    size = Player.width - 2, Player.height - 2

    def resolvePixel(pixelValue):
      pixelMap = [
        Fore.BLACK,
        Fore.BLUE,
        Fore.CYAN,
        Fore.GREEN,
        Fore.MAGENTA,
        Fore.RED,
        Fore.YELLOW,
        Fore.WHITE
      ]
      x = pixelMap[pixelValue] + '#' + Fore.RESET
      return x
      #return '█' if pixelValue > 213 else '▓' if pixelValue > 170 else '▒' if pixelValue > 128 else '░' if pixelValue > 64 else ' '
      #return '#' if pixelValue > 200 else ':' if pixelValue > 128 else "⠂" if pixelValue > 64 else " "
      #return '⣿' if pixelValue > 224 else '⢷' if pixelValue > 190 else '⢕' if pixelValue > 160 else '⢌' if pixelValue > 128 else '⡁' if pixelValue > 64 else '⠂' if pixelValue > 32 else ' '

    rendered_frames = [copy.deepcopy(Player.shadowBuff) for x in range(sequence.n_frames)]
    for i in range(sequence.n_frames):
      statusWindow.renderables = [
          renderables.Text(f'Resolution: {size}',
                           horizontalOffset=2, verticalOffset=1),
          renderables.Text(f'Status: Rendering',
                           horizontalOffset=3, verticalOffset=1),
          renderables.Text(
              f'Progress: {i}/{sequence.n_frames}', horizontalOffset=4, verticalOffset=1),
      ]
      renderables.MoveToTop(MainLayout, statusWindow)
      MainLayout.draw()

      sequence.seek(i)
      frame = sequence.convert('L').resize(size, Image.ANTIALIAS)
      frame = frame.quantize(colors=8)
      for width in range(0, frame.width):
        for height in range(0, frame.height):
          rendered_frames[i][height + 1][width + 1] = resolvePixel(frame.getpixel((width, height)))


    start_time = arrow.utcnow().timestamp
    for i in range(500000):

      seconds = (arrow.utcnow().timestamp - start_time) + 1
      statusWindow.renderables = [
          renderables.Text(f'Resolution: {size}',
                           horizontalOffset=2, verticalOffset=1),
          renderables.Text(f'Iteration: {i}',
                           horizontalOffset=3, verticalOffset=1),
          renderables.Text(
              f'Seconds Running: {int(seconds)}s', horizontalOffset=4, verticalOffset=1),
          renderables.Text(
              f'Avg Framerate: {int((i + 1) / seconds)} FPS', horizontalOffset=5, verticalOffset=1),
          renderables.Text(
              f'MainLayout Components: {len(MainLayout.components)}', horizontalOffset=6, verticalOffset=1),
          renderables.Text(
              f'Window RNCount: {len(statusWindow.renderables)}', horizontalOffset=7, verticalOffset=1),
      ]

      #sequence.seek()
      #frame = sequence.convert('L')
      #frame = frame.resize(size)
      #print(frame.width, frame.height)
      #frame.thumbnail(size, Image.ANTIALIAS)
      Player.shadowBuff = rendered_frames[i % sequence.n_frames]
      #input()

      renderables.MoveToTop(MainLayout, statusWindow)
      MainLayout.draw()



if __name__ == '__main__':
  test('nichiop.gif')
