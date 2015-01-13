import OpenGL.GL as gl
import OpenGL.GLUT as glut
import OpenGL.GLU as glu

class Tank(object):
    shapes = ['Cylinder', 'Box']

    def __init__(
        self,
        height_mm,
        outside_radius_mm,
        inside_radius_mm,
        shape,
    ):
        self.height_mm = height_mm
        self.outside_radius_mm = outside_radius_mm
        self.inside_radius_mm = inside_radius_mm
        if shape in self.shapes:
            self.shape = shape
        else:
            raise Exception("Unacceptable Shape Must be: %s" % ",".join(self.shapes))


class DrawTank(object):
    def __init__(self):
        self.quad = glu.gluNewQuadric()

    def draw_cylinder(self, inside, outside, height, base_thickness):
        glu.gluDisk(self.quad, 0, outside, 100, 5)
        gl.glTranslatef(0.0, 0.0, height)
        glu.gluDisk(self.quad, inside, outside, 100, 5)
        gl.glTranslatef(0.0, 0.0, -height)
        gl.glTranslatef(0.0, 0.0, base_thickness)
        glu.gluCylinder(self.quad, inside, inside, height - base_thickness, 100, 1)
        glu.gluDisk(self.quad, 0, inside, 100, 5)
        gl.glTranslatef(0.0, 0.0, -base_thickness)
        glu.gluCylinder(self.quad, outside, outside, height, 100, 1)

    def draw_tank(self, tank):
        # gl.glColor4f(1.0, 0.2, 0.2, 0.3)
        white = [0.8, 0.8, 0.8, 0.5]
        cyan =  [0.0, 0.8, 0.8, 0.5]
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE, cyan)
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, white)
        shininess = [50]
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SHININESS, shininess)
        self.draw_cylinder(0.4, 0.45, 0.5, 0.05)
