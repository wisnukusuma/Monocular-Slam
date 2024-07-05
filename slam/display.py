import pygame
from pygame.locals import DOUBLEBUF
import numpy as np

class Display2D(object):
  def __init__(self, W, H):
    pygame.init()
    self.screen = pygame.display.set_mode((W, H), DOUBLEBUF)
    self.surface = pygame.Surface(self.screen.get_size()).convert()

  def paint(self, img):
    # junk
    for event in pygame.event.get():
      pass

    # draw
    #pygame.surfarray.blit_array(self.surface, img.swapaxes(0,1)[:, :, [2,1,0]])

    # RGB, not BGR (might have to switch in twitchslam)
    pygame.surfarray.blit_array(self.surface, img.swapaxes(0,1)[:, :, [0,1,2]])
    self.screen.blit(self.surface, (0,0))

    # blit
    pygame.display.flip()


class DisplayPose2D(object):
  def __init__(self):
    self.screen = pygame.display.set_mode((1000, 1000))

  def paint(self,mapp):
    poses = []
    if len(mapp.frames) > 2:
      for f in mapp.frames:
        # invert pose for display only
        poses.append((np.linalg.inv(f.pose)[0][3]*10,(np.linalg.inv(f.pose)[1][3]*10)+400))
      # print(poses)
      pygame.draw.lines(self.screen, pygame.Color("green"), False, poses)
      pygame.display.flip()

from multiprocessing import Process, Queue
import pangolin
import OpenGL.GL as gl
import numpy as np

class Display3D(object):
  def __init__(self):
    self.state = None
    self.q = Queue()
    self.vp = Process(target=self.viewer_thread, args=(self.q,))
    self.vp.daemon = True
    self.vp.start()

  def viewer_thread(self, q):
    self.viewer_init(1024, 768)
    while 1:
      self.viewer_refresh(q)

  def viewer_init(self, w, h):
    pangolin.CreateWindowAndBind('Map Viewer', w, h)
    gl.glEnable(gl.GL_DEPTH_TEST)

    self.scam = pangolin.OpenGlRenderState(
      pangolin.ProjectionMatrix(w, h, 420, 420, w//2, h//2, 0.2, 10000),
      pangolin.ModelViewLookAt(0, -10, -8,
                               0, 0, 0,
                               0, -1, 0))
    self.handler = pangolin.Handler3D(self.scam)

    # Create Interactive View in window
    self.dcam = pangolin.CreateDisplay()
    self.dcam.SetBounds(pangolin.Attach(0.0), pangolin.Attach(1.0), pangolin.Attach.Pix(180), pangolin.Attach(1.0), -w/h)
    self.dcam.SetHandler(self.handler)
    # hack to avoid small Pangolin, no idea why it's *2
    self.dcam.Resize(pangolin.Viewport(0,0,w*2,h*2))
    self.dcam.Activate()


  def viewer_refresh(self, q):
    while not q.empty():
      self.state = q.get()

    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glClearColor(0.0, 0.0, 0.0, 1.0)
    self.dcam.Activate(self.scam)
    
    if self.state is not None:
    #   # print(self.state[1].shape[0])
      if self.state[0].shape[0] >= 2:
        # draw poses
        gl.glColor3f(0.0, 1.0, 0.0)
        # self.draw_cameras(self.state[0][:-1])
        pangolin.DrawCameras(self.state[0][:-1])
        # pangolin.DrawCurrentCamera(self.state[0][:-1])

      if self.state[0].shape[0] >= 1:
        # draw current pose as yellow
        gl.glColor3f(1.0, 1.0, 0.0)
        # self.draw_cameras(self.state[0][-1:])
        pangolin.DrawCameras(self.state[0][-1:])
        # pangolin.DrawCurrentCamera(self.state[0][-1:])

      if self.state[1].shape[0] != 0:
        # draw keypoints
        # print(np.shape(self.state[1]))
        gl.glPointSize(5)
        # gl.glColor3f(1.0, 0.0, 0.0)
        # for pos in self.state[1]:
          # print(pos[0],pos[1],pos[2])
        # pangolin.glDrawPoints(self.state[1])
          # gl.glVertex3f(pos[0],pos[1],pos[2])
        pangolin.DrawPoints(self.state[1], self.state[2])
    pangolin.FinishFrame()

  def paint(self, mapp):
    if self.q is None:
      return

    poses, pts, colors = [], [], []
    for f in mapp.frames:
      # invert pose for display only
      poses.append(np.linalg.inv(f.pose))
    for p in mapp.points:
      pts.append(p.pt)
      colors.append(p.color)
    self.q.put((np.array(poses), np.array(pts), np.array(colors)/256.0))
