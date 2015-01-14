import OpenGL.GL as gl
import OpenGL.GLUT as glut
import OpenGL.GLU as glu

class Tank(object):
    shapes = ['Cylinder', 'Box']

    def __init__(
        self,
        height_mm,
        material_thickness_mm,
        inside_radius_mm,
        shape,
    ):
        self.height_mm = float(height_mm)
        self.material_thickness_mm = float(material_thickness_mm)
        self.inside_radius_mm = float(inside_radius_mm)
        if shape in self.shapes:
            self.shape = shape
        else:
            raise Exception("Unacceptable Shape Must be: %s" % ",".join(self.shapes))

    @property
    def outside_radius_mm(self):
        return self.inside_radius_mm + self.material_thickness_mm

    def get_scaled(self, max_size):
        max_detail = max(self.height_mm, self.inside_radius_mm + self.material_thickness_mm)
        return Tank(
            (self.height_mm / max_detail) * max_size,
            (self.material_thickness_mm / max_detail) * max_size,
            (self.inside_radius_mm / max_detail) * max_size,
            self.shape
            )


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

    def square_cup(self, width, height, inside):
        base_normal = 1.0 if inside else -1.0
        gl.glBegin(gl.GL_QUADS)

        gl.glNormal( 0.0, base_normal, 0.0 )
        gl.glVertex3f( width, -width, 0.0     )
        gl.glVertex3f(-width, -width, 0.0     )
        gl.glVertex3f(-width, -width, height  )
        gl.glVertex3f( width, -width, height  )

        gl.glNormal(0.0,-base_normal, 0.0)
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

    def draw_tank(self, tank):
        scaled_tank = tank.get_scaled(1.0)
 
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE, [0.8, 0.8, 0.8, 0.5])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, [0.0, 0.8, 0.8, 0.5])
        # gl.glMaterialfv(gl.GL_FRONT, gl.GL_SHININESS, [50])
        # self.draw_cylinder(scaled_tank.inside_radius_mm, scaled_tank.outside_radius_mm, scaled_tank.height_mm, scaled_tank.material_thickness_mm)
        self.draw_box(scaled_tank.inside_radius_mm, scaled_tank.outside_radius_mm, scaled_tank.height_mm, scaled_tank.material_thickness_mm)
