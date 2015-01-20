import OpenGL.GL as gl
import OpenGL.GLUT as glut
import OpenGL.GLU as glu


class JGLHelpers(object):
    def __init__(self):
        self._font = glut.GLUT_BITMAP_HELVETICA_12
        self.height = 1
        self.width = 1.
        self.line_height = 16

    def drawString(self, string_data):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()

        gl.glOrtho(0, self.width, 0, self.height, -1, 1)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glLoadIdentity()

        gl.glDisable(gl.GL_DEPTH_TEST)

        gl.glDisable(gl.GL_LIGHTING)
        gl.glColor3f(1, 0, 0)

        pos = 20
        gl.glRasterPos2i(10, self.height - pos)

        for ch in string_data:
            if ch == '\n':
                pos = pos + self.line_height
                gl.glRasterPos2i(10, self.height - pos)
            else:
                glut.glutBitmapCharacter(self._font, ord(ch))

        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
