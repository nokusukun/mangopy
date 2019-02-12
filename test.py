from src import driver as RenderDriver, layout, renderables, components

def countComponents(component, count=0):
  c = len(component.components)
  if c == 0:
    return count
  
  for comp in component.components:
    count += countComponents(comp, c)
  return count


def test():
  import time
  import arrow
  import random
  import math

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

    boxes = []
    for i in range(0, MainLayout.width - 50, 50):
      sineBox = components.SineBox(f'Box {i}', 50, 30, 1 + i, random.randint(1, MainLayout.height- 30))
      sineBox.attachTo(MainLayout)
      boxes.append(sineBox)


    # sineBox = components.SineBox('Sean is a bitch', 50, 30, 1, 1)
    # sineBox.attachTo(MainLayout)
    # sineBox2 = components.SineBox('Sean is a turboslut', 50, 30, 65, 1)
    # sineBox2.attachTo(MainLayout)
    # sineBox3 = components.SineBox('Sean is a cumguzzler', 60, 15, 25, 5)
    # sineBox3.attachTo(MainLayout)

    start_time = arrow.utcnow().timestamp
    for i in range(500000):
      MainLayout.renderables[1] = renderables.TitleBar(
          f'[Render Driver Test] Component Count: {countComponents(MainLayout)}', 'left')

      seconds = (arrow.utcnow().timestamp - start_time) + 1
      statusWindow.renderables = [
          renderables.Text(f'SineH: {boxes[0].pixel.anchorh:<10}', horizontalOffset=1, verticalOffset=1),
          renderables.Text(f'SineW: {boxes[0].pixel.anchorw:<10}', horizontalOffset=2, verticalOffset=1),
          renderables.Text(f'Iteration: {i}', horizontalOffset=3, verticalOffset=1),
          renderables.Text(f'Seconds Running: {int(seconds)}s', horizontalOffset=4, verticalOffset=1),
          renderables.Text(f'Avg Framerate: {int((i + 1) / seconds)} FPS', horizontalOffset=5, verticalOffset=1),
          renderables.Text(f'MainLayout Components: {len(MainLayout.components)}', horizontalOffset=6, verticalOffset=1),
          renderables.Text(f'Window RNCount: {len(statusWindow.renderables)}', horizontalOffset=7, verticalOffset=1),
      ]

      for box in boxes:
        box.sineVal = i

      # sineBox.title = f'Left Box Index {MainLayout.components.index(sineBox)}' 
      # sineBox.sineVal = i
      # sineBox2.title = f'Right Box Index {MainLayout.components.index(sineBox2)}'
      # sineBox2.sineVal = i
      # sineBox3.title = f'Center Box Index {MainLayout.components.index(sineBox3)}'
      # sineBox3.sineVal = i
      if not i % 100:
        random.shuffle(MainLayout.components)
      renderables.MoveToTop(MainLayout, statusWindow)
      MainLayout.draw()


def gameOfLife():
  import time
  import arrow
  import random
  import math

  with RenderDriver.ConsoleDriver(ignoreOverflow=False) as driver:
    MainLayout = layout.Layout(driver.width, driver.height, 0, 0)
    MainLayout.parent = driver
    MainLayout.renderables.extend([
        renderables.Border(),
        renderables.TitleBar('Render Driver Test', 'left'),
    ])

    statusWindow = components.Window(40, 9)
    renderables.PositionFor(
        MainLayout, horizontal='top', vertical='right', horizontalOffset=1, verticalOffset=-1)(statusWindow)
    statusWindow.title = 'Game of Life'
    statusWindow.attachTo(MainLayout)

    gol = components.GameOfLife(MainLayout.width - 2, MainLayout.height - 2, 1,1)
    gol.attachTo(MainLayout)
    gol.populate()
    populations = [0]

    start_time = arrow.utcnow().timestamp
    renderables.MoveToTop(MainLayout, statusWindow)
    statusWindow.renderables = [
        renderables.Text(f'Initial Seed', horizontalOffset=1, verticalOffset=1),
        renderables.Text(f'[Press Enter to Start]', horizontalOffset=2, verticalOffset=1),
    ]
    MainLayout.draw()

    input()
    for i in range(500000):

      MainLayout.renderables[1] = renderables.TitleBar(
          f'[Render Driver Test] Component Count: {len(MainLayout.components)}', 'left')

      golCells = sum([sum(1 for y in x if y == gol.aliveBlock) for x in gol.shadowBuff])

      populations.append(golCells)
      if len(populations) > 50:
        populations = populations[1:]
      seconds = (arrow.utcnow().timestamp - start_time) + 1
      statusWindow.renderables = [
          renderables.Text(f'Iteration: {i}', horizontalOffset=1, verticalOffset=1),
          renderables.Text(f'Seconds Running: {int(seconds)}s', horizontalOffset=2, verticalOffset=1),
          renderables.Text(f'Avg Framerate: {int((i + 1) / seconds)} FPS', horizontalOffset=3, verticalOffset=1),
          renderables.Text(f'MainLayout Components: {countComponents(MainLayout)}', horizontalOffset=4, verticalOffset=1),
          renderables.Text(f'Alive Cells: {golCells:<10}', horizontalOffset=5, verticalOffset=1),
      ]

      MainLayout.draw()
      if len(set(populations)) < 10 and len(populations) > 20:
        statusWindow.renderables = [
            renderables.Text(f'Iteration: {i}', horizontalOffset=1, verticalOffset=1),
            renderables.Text(f'Seconds Running: {int(seconds)}s', horizontalOffset=2, verticalOffset=1),
            renderables.Text(f'Avg Framerate: {int((i + 1) / seconds)} FPS', horizontalOffset=3, verticalOffset=1),
            renderables.Text(f'MainLayout Components: {len(MainLayout.components)}', horizontalOffset=4, verticalOffset=1),
            renderables.Text(f'Alive Cells: {golCells:<10}', horizontalOffset=5, verticalOffset=1),
            renderables.Text(f'Simulation ended.', horizontalOffset=6, verticalOffset=1),
            renderables.Text(f'Life is on a standstill.', horizontalOffset=7, verticalOffset=1),
            renderables.Text(f'Press Enter to Exit', vertical='right', horizontalOffset=8, verticalOffset=-3),
        ]
        renderables.PositionFor(
          MainLayout, horizontal='center', vertical='center')(statusWindow)
        break
    
    MainLayout.draw()
    input()

if __name__ == "__main__":
  #test()
  gameOfLife()
