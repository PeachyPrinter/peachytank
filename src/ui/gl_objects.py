import OpenGL.GL as gl
import OpenGL.GLUT as glut
import OpenGL.GLU as glu
from domain.objects import Tank

import logging

class GLObject(object):
    def draw(self, domain_object):
        raise NotImplementedError()

class Axis(GLObject):
    def __init__(self):
        self.quad = glu.gluNewQuadric()

    def arrow(self):
        glu.gluCylinder(self.quad, 0.005, 0.005, 0.7, 100, 1)
        gl.glTranslatef(0.0, 0.0, 0.7)
        glu.gluCylinder(self.quad, 0.03, 0.0, 0.1, 100, 1)
        gl.glTranslatef(0.0, 0.0, -0.7)

    def draw(self, ignored):
        #RED X
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE,  [0.8, 0.2, 0.2, 1.0])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, [0.9, 0.5, 0.5, 1.0])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_EMISSION, [0.2, 0.1, 0.1, 1.0])
        gl.glRotate(90, 0.0, 1.0, 0.0)
        self.arrow()
        gl.glRotate(-90, 0.0, 1.0, 0.0)

        #GREEN Y
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE,  [0.2, 0.8, 0.2, 1.0])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, [0.5, 0.9, 0.5, 1.0])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_EMISSION, [0.1, 0.2, 0.1, 1.0])
        gl.glRotate(90, 1.0, 0.0, 0.0)
        self.arrow()
        gl.glRotate(-90, 1.0, 0.0, 0.0)

        #BLUE Z
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE,  [0.2, 0.2, 0.8, 1.0])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, [0.5, 0.5, 0.9, 1.0])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_EMISSION, [0.1, 0.1, 0.2, 1.0])
        self.arrow()


class DrawTank(GLObject):
    def __init__(self):
        self.quad = glu.gluNewQuadric()

    def draw_cylinder(self, inside, outside, height, base_thickness):
        gl.glRotate(180, 0.0, 1.0, 0.0)
        glu.gluDisk(self.quad, 0, outside, 100, 5)
        gl.glRotate(-180, 0.0, 1.0, 0.0)
        gl.glTranslatef(0.0, 0.0, height)
        glu.gluDisk(self.quad, inside, outside, 100, 5)
        gl.glTranslatef(0.0, 0.0, -height)
        gl.glTranslatef(0.0, 0.0, base_thickness)
        glu.gluQuadricOrientation(self.quad, glu.GLU_INSIDE)
        glu.gluCylinder(self.quad, inside, inside, height - base_thickness, 100, 1)
        glu.gluQuadricOrientation(self.quad, glu.GLU_OUTSIDE)
        glu.gluDisk(self.quad, 0, inside, 100, 5)
        gl.glTranslatef(0.0, 0.0, -base_thickness)
        glu.gluCylinder(self.quad, outside, outside, height, 100, 1)

    def square_cup(self, width, height, inside):
        base_normal = 1.0 if inside else -1.0
        gl.glBegin(gl.GL_QUADS)

        gl.glNormal( 0.0, base_normal, 0.0 )
        gl.glVertex3f( width, -width, 0.0     )
        gl.glVertex3f(-width, -width, 0.0     )
        gl.glVertex3f(-width, -width, height  )
        gl.glVertex3f( width, -width, height  )

        gl.glNormal(0.0, -base_normal, 0.0)
        gl.glVertex3f( width,  width, 0.0     )
        gl.glVertex3f(-width,  width, 0.0     )
        gl.glVertex3f(-width,  width, height  )
        gl.glVertex3f( width,  width, height  )

        gl.glNormal(base_normal, 0.0, 0.0)
        gl.glVertex3f(-width,  width, 0.0     )
        gl.glVertex3f(-width, -width, 0.0     )
        gl.glVertex3f(-width, -width, height  )
        gl.glVertex3f(-width,  width, height  )

        gl.glNormal(-base_normal, 0.0, 0.0)
        gl.glVertex3f( width,  width, 0.0     )
        gl.glVertex3f( width, -width, 0.0     )
        gl.glVertex3f( width, -width, height  )
        gl.glVertex3f( width,  width, height  )

        gl.glNormal(0.0, 0.0, base_normal)
        gl.glVertex3f( width,  width, 0.0     )
        gl.glVertex3f(-width,  width, 0.0     )
        gl.glVertex3f(-width, -width, 0.0     )
        gl.glVertex3f( width, -width, 0.0     )
        gl.glEnd()

    def square_disk(self, outer, depth):

        inner = outer - depth

        gl.glBegin(gl.GL_QUADS)
        gl.glNormal( 0.0, 0.0, 1.0 )
        gl.glVertex3f( outer,  outer, 0.0)
        gl.glVertex3f(-outer,  outer, 0.0)
        gl.glVertex3f(-outer,  inner, 0.0)
        gl.glVertex3f( outer,  inner, 0.0)

        gl.glVertex3f( outer, -outer, 0.0)
        gl.glVertex3f(-outer, -outer, 0.0)
        gl.glVertex3f(-outer, -inner, 0.0)
        gl.glVertex3f( outer, -inner, 0.0)

        gl.glVertex3f( outer,  inner, 0.0)
        gl.glVertex3f( inner,  inner, 0.0)
        gl.glVertex3f( inner, -inner, 0.0)
        gl.glVertex3f( outer, -inner, 0.0)

        gl.glVertex3f(-outer,  inner, 0.0)
        gl.glVertex3f(-inner,  inner, 0.0)
        gl.glVertex3f(-inner, -inner, 0.0)
        gl.glVertex3f(-outer, -inner, 0.0)

        gl.glEnd()

    def draw_box(self, inside, outside, height, base_thickness):
        self.square_cup(outside, height, False)
        gl.glTranslatef(0.0, 0.0, base_thickness)
        self.square_cup(inside, height - base_thickness, True)
        gl.glTranslatef(0.0, 0.0, -base_thickness)
        gl.glTranslatef(0.0, 0.0, height)
        self.square_disk(outside, base_thickness)
        gl.glTranslatef(0.0, 0.0, -height)

    def draw(self, domain_object):
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE, [0.2, 0.2, 0.8, 0.3])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, [0.5, 0.5, 0.9, 0.5])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_EMISSION, [0.1, 0.1, 0.2, 0.3])
        gl.glEnable(gl.GL_BLEND)
        gl.glDepthMask(gl.GL_FALSE)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        if domain_object.shape == 'Box':
            self.draw_box(domain_object.inside_radius_mm, domain_object.outside_radius_mm, domain_object.height_mm, domain_object.material_thickness_mm)
        else:
            gl.glMaterialfv(gl.GL_FRONT, gl.GL_SHININESS, [100])
            self.draw_cylinder(domain_object.inside_radius_mm, domain_object.outside_radius_mm, domain_object.height_mm, domain_object.material_thickness_mm)
        gl.glDepthMask(gl.GL_TRUE)
        gl.glDisable(gl.GL_BLEND)

class DrawPrinter(GLObject):
    def __init__(self):
        self.quad = glu.gluNewQuadric()

    def _square_pyrmid(self, base_length, top_length, height):
        base_leg = base_length / 2.0
        base_arm = top_length / 2.0
        gl.glBegin(gl.GL_QUADS)

        gl.glNormal(0.0, 0.0, 1.0)
        gl.glVertex3f( base_leg,  base_leg, 0.0)
        gl.glVertex3f(-base_leg,  base_leg, 0.0)
        gl.glVertex3f(-base_arm,  base_arm, height)
        gl.glVertex3f( base_arm,  base_arm, height)

        gl.glVertex3f( base_leg, -base_leg, 0.0)
        gl.glVertex3f(-base_leg, -base_leg, 0.0)
        gl.glVertex3f(-base_arm, -base_arm, height)
        gl.glVertex3f( base_arm, -base_arm, height)

        gl.glVertex3f( base_leg,  base_leg, 0.0)
        gl.glVertex3f( base_leg, -base_leg, 0.0)
        gl.glVertex3f( base_arm, -base_arm, height)
        gl.glVertex3f( base_arm,  base_arm, height)

        gl.glVertex3f(-base_leg, -base_leg, 0.0)
        gl.glVertex3f(-base_leg,  base_leg, 0.0)
        gl.glVertex3f(-base_arm,  base_arm, height)
        gl.glVertex3f(-base_arm, -base_arm, height)

        gl.glEnd()


    def _draw_projection(self, domain_object):
        logging.debug("Drawing Projection")
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE,  [0.8, 0.2, 0.2, 0.1])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, [0.9, 0.5, 0.5, 0.3])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_EMISSION, [0.2, 0.1, 0.1, 0.1])
        gl.glEnable(gl.GL_BLEND)
        gl.glDepthMask(gl.GL_FALSE)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        if domain_object.projection_shape == 'Circle':
            glu.gluCylinder(self.quad, domain_object.radius_at_base, 0.0, domain_object.height_mm, 100, 1)
        else:
            self._square_pyrmid(domain_object.radius_at_base * 2.0, 0.0, domain_object.height_mm)
        gl.glDepthMask(gl.GL_TRUE)
        gl.glDisable(gl.GL_BLEND)

    def _draw_printer(self, domain_object):
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE, [0.8, 0.2, 0.2, 1])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, [0.8, 0.4, 0.4, 1])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_EMISSION, [0.2, 0.1, 0.1, 1])
        gl.glTranslatef(0.0, 0.0, domain_object.height_mm)
        printer_size = 50 * domain_object.relitive_size
        gl.glTranslatef(0.0, 0.0, printer_size / 2.0)
        glut.glutSolidCube(printer_size, 5, 5)
        gl.glTranslatef(0.0, 0.0, -printer_size / 2.0)
        gl.glTranslatef(0.0, 0.0, -domain_object.height_mm)

    def draw(self, domain_object):
        self._draw_printer(domain_object)
        self._draw_projection(domain_object)

class DrawEnvironment(GLObject):
    def draw(self, domain_object):
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE,  [0.9, 0.9, 0.9, 1.0])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_EMISSION, [0.3, 0.3, 0.3, 1.0])

        gl.glBegin(gl.GL_QUADS)
        gl.glNormal( 0.0, 0.0, 1.0 )
        gl.glVertex3f( 4.0,  2.0, -0.00001)
        gl.glVertex3f( 4.0, -2.0, -0.00001)
        gl.glVertex3f(-4.0, -2.0, -0.00001)
        gl.glVertex3f(-4.0,  2.0, -0.00001)
        gl.glEnd()


