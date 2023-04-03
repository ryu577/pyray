import numpy as np
from pyray.rotation import rotation
import pyray.shapes.fourd.tesseract_graph as tg
import pyray.shapes.fourd.tsrct_face_rotation as tfr
import pyray.shapes.fourd.open_tsrct as ot
from pyray.shapes.fourd.open_tsrct import Rotation
from PIL import Image, ImageDraw


def tst_smooth_rotation():
    r = rotation(4, np.pi*17/60.0)
    f1 = tg.Face1('-00+')
    f2 = tg.Face1('00-+')
    f3 = tg.Face1('-0-0')
    for i in range(11):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        f1.plot(draw, r)
        f2.rotate_about_plane(f3.vertices[0], f3.vertices[1],
                              f3.vertices[2], np.pi/20.0,
                              ref_pt=f1.face_center)
        f2.plot(draw, r)
        im.save("Images//RotatingCube//im" +
                        str(i).rjust(4, '0') + 
                        ".png")


def tst_rotation_three_faces():
    r = rotation(4, np.pi*17/60.0)
    f1 = tg.Face1('00-+')
    f2 = tg.Face1('-00+')
    f3 = tg.Face1('-0-0')
    f4 = tg.Face1('00++')
    f5 = tg.Face1('-0+0')
    for i in range(10):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        f1.plot(draw, r)
        f2.rotate_about_plane(f3.vertices[0],
                              f3.vertices[1],
                              f3.vertices[2], np.pi/20,
                              ref_pt = f1.face_center)
        f2.plot(draw, r)

        f5.rotate_about_plane(f3.vertices[0],
                              f3.vertices[1],
                              f3.vertices[2], np.pi/20,
                              ref_pt = f1.face_center)

        f4.rotate_about_plane(f3.vertices[0],
                              f3.vertices[1],
                              f3.vertices[2], np.pi/20,
                              ref_pt = f1.face_center)
        f4.rotate_about_plane(f5.vertices[0],
                              f5.vertices[1],
                              f5.vertices[2], np.pi/20,
                              ref_pt = f1.face_center)
        f4.plot(draw, r)
        im.save("Images//RotatingCube//im" +
                        str(i).rjust(4, '0') +
                        ".png")


def tst_smooth_rotation2():
    r = rotation(4, np.pi*17/60.0)
    f1 = tg.Face1('-00+')
    f2 = tg.Face1('00-+')
    f3 = tg.Face1('-0-0')
    for i in range(11):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        f1.plot(draw, r)
        pt1, pt2, pt3 = tfr.get_rotation_plane(f1, f2)
        f2.rotate_about_plane(pt1, pt2, pt3, np.pi/20.0,
                              ref_pt=f1.face_center)
        f2.plot(draw, r)
        im.save("Images//RotatingCube//im" +
                        str(i).rjust(4, '0') + 
                        ".png")


def tst_rotation_three_faces2():
    r = rotation(4, np.pi*17/60.0)
    f1 = tg.Face1('00-+')
    f2 = tg.Face1('-00+')
    f3 = tg.Face1('-0-0')
    f4 = tg.Face1('00++')
    f5 = tg.Face1('-0+0')
    for i in range(10):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        f1.plot(draw, r)
        pt1_1, pt2_1, pt3_1 = tfr.get_rotation_plane(f1, f2)
        f2.rotate_about_plane(pt1_1, pt2_1, pt3_1, np.pi/20,
                              ref_pt = f1.face_center)
        f2.plot(draw, r)
        pt1_2, pt2_2, pt3_2 = tfr.get_rotation_plane(f2, f4)
        f4.rotate_about_plane(pt1_1, pt2_1, pt3_1, np.pi/20,
                              ref_pt = f1.face_center)
        f4.rotate_about_plane(pt1_2, pt2_2, pt3_2, np.pi/20,
                              ref_pt = f1.face_center)
        f4.plot(draw, r)
        im.save("Images//RotatingCube//im" +
                        str(i).rjust(4, '0') +
                        ".png")


def tst_rotation_many_faces():
    r = rotation(4, np.pi*17/60.0)
    f1 = tg.Face1('00++')
    f2 = tg.Face1('+00+')
    f3 = tg.Face1('00-+')
    f4 = tg.Face1('-0-0')
    f5 = tg.Face1('00--')
    f6 = tg.Face1('0--0')
    f7 = tg.Face1('+0-0')
    f8 = tg.Face1('0+-0')
    faces = np.array([f1, f2, f3, f4, f5, f6, f7, f8])
    for i in range(10):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        f1.plot(draw, r)
        rots = []
        for jx in range(1, len(faces)):
            face = faces[jx]
            print("Rotation for " + faces[jx].val)
            for rr in rots:
                pt1, pt2, pt3 = rr.ax1, rr.ax2, rr.ax3
                face.rotate_about_plane(pt1, pt2, pt3, np.pi/20,
                                        ref_pt = f1.face_center)
            rr = Rotation(faces[jx-1], faces[jx], np.pi/20)
            rots.append(rr)
            pt1, pt2, pt3 = rr.ax1, rr.ax2, rr.ax3
            face.rotate_about_plane(pt1, pt2, pt3, np.pi/20,
                                        ref_pt = f1.face_center)
            face.plot(draw, r)
        im.save("Images//RotatingCube//im" +
                        str(i).rjust(4, '0') +
                        ".png")


def tst_rotation_simplified():
    r = rotation(4, np.pi*17/60.0)
    f1 = tg.Face1('00++')
    f2 = tg.Face1('+00+')
    f3 = tg.Face1('00-+')
    f4 = tg.Face1('-0-0')
    f5 = tg.Face1('00--')
    f6 = tg.Face1('0--0')
    f7 = tg.Face1('+0-0')
    f8 = tg.Face1('0+-0')
    faces = np.array([f1, f2, f3, f4, f5, f6, f7, f8])
    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    for i1 in range(8):
        ff = faces[i1]
        ff.plot(draw, r, rgba=(0, 255,0,90))
    im.save("Images//RotatingCube//im" +
                str(0).rjust(4, '0') +
                ".png")
    for i in range(10):
        theta = np.pi/20*(i+1)
        #theta = np.pi/20
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        pt1_1, pt2_1, pt3_1 = tfr.get_rotation_plane(f1, f2)
        f2.rotate_about_plane(pt1_1, pt2_1, pt3_1, theta,
                                ref_pt=f1.face_center,
                                take_farther=True)
        f3.rotate_about_plane2(pt1_1, pt2_1, pt3_1, theta,
                                ref_face=f2)
        f4.rotate_about_plane2(pt1_1, pt2_1, pt3_1, theta,
                                ref_face=f3)
        f5.rotate_about_plane2(pt1_1, pt2_1, pt3_1, theta,
                                ref_face=f4)
        f6.rotate_about_plane2(pt1_1, pt2_1, pt3_1, theta,
                                ref_face=f5)
        f7.rotate_about_plane2(pt1_1, pt2_1, pt3_1, theta,
                                ref_face=f6)
        f8.rotate_about_plane2(pt1_1, pt2_1, pt3_1, theta,
                                ref_face=f7)

        pt1_2, pt2_2, pt3_2 = tfr.get_rotation_plane(f2, f3)
        f3.rotate_about_plane(pt1_2, pt2_2, pt3_2, theta,
                              ref_pt=f2.face_center,
                              take_farther=True)
        f4.rotate_about_plane2(pt1_2, pt2_2, pt3_2, theta,
                                ref_face=f3)
        f5.rotate_about_plane2(pt1_2, pt2_2, pt3_2, theta,
                                ref_face=f4)
        f6.rotate_about_plane2(pt1_2, pt2_2, pt3_2, theta,
                                ref_face=f5)
        f7.rotate_about_plane2(pt1_2, pt2_2, pt3_2, theta,
                                ref_face=f6)
        f8.rotate_about_plane2(pt1_2, pt2_2, pt3_2, theta,
                                ref_face=f7)

        pt1_3, pt2_3, pt3_3 = tfr.get_rotation_plane(f3, f4)
        f4.rotate_about_plane(pt1_3, pt2_3, pt3_3, theta,
                              ref_pt=f3.face_center,
                              take_farther=True)
        f5.rotate_about_plane2(pt1_3, pt2_3, pt3_3, theta,
                                ref_face=f4)
        f6.rotate_about_plane2(pt1_3, pt2_3, pt3_3, theta,
                                ref_face=f5)
        f7.rotate_about_plane2(pt1_3, pt2_3, pt3_3, theta,
                                ref_face=f6)
        f8.rotate_about_plane2(pt1_3, pt2_3, pt3_3, theta,
                                ref_face=f7)

        pt1_4, pt2_4, pt3_4 = tfr.get_rotation_plane(f4, f5)
        f5.rotate_about_plane(pt1_4, pt2_4, pt3_4, theta,
                              ref_pt=f4.face_center,
                              take_farther=True)
        f6.rotate_about_plane2(pt1_4, pt2_4, pt3_4, theta,
                                ref_face=f5)
        f7.rotate_about_plane2(pt1_4, pt2_4, pt3_4, theta,
                                ref_face=f6)
        f8.rotate_about_plane2(pt1_4, pt2_4, pt3_4, theta,
                                ref_face=f7)

        pt1_5, pt2_5, pt3_5 = tfr.get_rotation_plane(f5, f6)
        f6.rotate_about_plane(pt1_5, pt2_5, pt3_5, theta,
                              ref_pt=f5.face_center,
                              take_farther=True)
        f7.rotate_about_plane2(pt1_5, pt2_5, pt3_5, theta,
                               ref_face=f6)
        f8.rotate_about_plane2(pt1_5, pt2_5, pt3_5, theta,
                               ref_face=f7)

        pt1_6, pt2_6, pt3_6 = tfr.get_rotation_plane(f6, f7)
        f7.rotate_about_plane(pt1_6, pt2_6, pt3_6, theta,
                              ref_pt=f6.face_center,
                              take_farther=True)
        f8.rotate_about_plane2(pt1_6, pt2_6, pt3_6, theta,
                               ref_face=f7)
        
        pt1_7, pt2_7, pt3_7 = tfr.get_rotation_plane(f7, f8)
        f8.rotate_about_plane(pt1_7, pt2_7, pt3_7, theta,
                              ref_pt=f7.face_center,
                              take_farther=True)
        
        for i1 in range(len(faces)):
            ff = faces[i1]
            ff.plot(draw, r, rgba=(0, 255,0,90))
            ff.reset()
        
        im.save("Images//RotatingCube//im" +
                        str(i+1).rjust(4, '0') +
                        ".png")


if __name__ == "__main__":
    tst_rotation_simplified()


def draw_specific():
    r = rotation(4, np.pi*17/60.0)
    f1 = tg.Face1('00++')
    f2 = tg.Face1('+00+')
    f3 = tg.Face1('00-+')
    f4 = tg.Face1('-0-0')
    f5 = tg.Face1('00--')
    f6 = tg.Face1('0--0')
    f7 = tg.Face1('+0-0')
    f8 = tg.Face1('0+-0')
    faces = np.array([f1, f2, f3, f4, f5, f6, f7, f8])
    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    f2.plot(draw, r, rgba=(255,0,0,80))
    f3.plot(draw, r, rgba=(255,255,0,80))
    f6.plot(draw, r, rgba=(0,255,0,80))
    f7.plot(draw, r, rgba=(0,255,255,80))
    im.save("Images//RotatingCube//im" +
                        str(0).rjust(4, '0') +
                        ".png")
    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    pt1_1, pt2_1, pt3_1 = tfr.get_rotation_plane(f1, f2)
    f2.rotate_about_plane(pt1_1, pt2_1, pt3_1, np.pi/20,
                            ref_pt = f1.face_center)
    f2.plot(draw, r, rgba=(255,0,0,80))
    f3.rotate_about_plane(pt1_1, pt2_1, pt3_1, np.pi/20,
                            ref_pt = f1.face_center)
    pt1_2, pt2_2, pt3_2 = tfr.get_rotation_plane(f2, f3)
    f3.rotate_about_plane(pt1_2, pt2_2, pt3_2, np.pi/20,
                            ref_pt = f1.face_center)
    f3.plot(draw, r, rgba=(255,255,0,80))
    f6.rotate_about_plane(pt1_1, pt2_1, pt3_1, np.pi/20,
                            ref_pt = f1.face_center)
    f6.plot(draw, r, rgba=(0,255,0,80))
    f7.rotate_about_plane(pt1_1, pt2_1, pt3_1, np.pi/20,
                            ref_pt = f1.face_center)
    f7.plot(draw, r, rgba=(0,255,255,80))
    im.save("Images//RotatingCube//im" +
                        str(1).rjust(4, '0') +
                        ".png")

def tst_problematic_rotation():
    r = rotation(4, np.pi*17/60.0)
    f1 = tg.Face1('+00+')
    f2 = tg.Face1('00-+')
    f3 = tg.Face1('+0-0')
    rr = ot.Rotation(f1, f2)
    tgr = tg.TsrctFcGraph()
    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    for kk in tgr.face_map.keys():
        ff = tg.Face1(kk)
        ff.plot(draw, r, rgba=(10,31,190,120))
    f1.plot(draw, r, rgba=(255,0,0,200))
    f2.plot(draw, r, rgba=(0,255,0,200))
    f3.plot(draw, r, rgba=(255,255,0,200))
    im.save("Images//RotatingCube//im" +
                        str(0).rjust(4, '0') +
                        ".png")


def tst_case_failing():
    r = rotation(4, np.pi*17/60.0)
    f1 = tg.Face1('00++')
    f2 = tg.Face1('+00+')
    f3 = tg.Face1('00-+')
    f4 = tg.Face1('-0-0')
    f5 = tg.Face1('00--')
    f6 = tg.Face1('0--0')
    f7 = tg.Face1('+0-0')
    f8 = tg.Face1('0+-0')
    faces = np.array([f1, f2, f3, f4, f5, f6, f7, f8])
    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    for ff in faces:
        ff.plot(draw, r)
    im.save("Images//RotatingCube//im" +
                        str(0).rjust(4, '0') +
                        ".png")
    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    f1.plot(draw, r)
    pt1_1, pt2_1, pt3_1 = tfr.get_rotation_plane(f1, f2)
    f2.rotate_about_plane(pt1_1, pt2_1, pt3_1, np.pi/20,
                            ref_pt = f1.face_center)
    f2.plot(draw, r)
    f3.rotate_about_plane(pt1_1, pt2_1, pt3_1, np.pi/20,
                            ref_pt = f1.face_center)
    pt1_2, pt2_2, pt3_2 = tfr.get_rotation_plane(f2, f3)
    f3.rotate_about_plane(pt1_2, pt2_2, pt3_2, np.pi/20,
                            ref_pt = f1.face_center)
    f3.plot(draw, r)
    f4.rotate_about_plane(pt1_1, pt2_1, pt3_1, np.pi/20,
                            ref_pt = f1.face_center)
    f4.rotate_about_plane(pt1_2, pt2_2, pt3_2, np.pi/20,
                            ref_pt = f1.face_center)
    pt1_3, pt2_3, pt3_3 = tfr.get_rotation_plane(f3, f4)
    f4.rotate_about_plane(pt1_3, pt2_3, pt3_3, np.pi/20,
                            ref_pt = f1.face_center)
    f4.plot(draw, r)
    f5.rotate_about_plane(pt1_1, pt2_1, pt3_1, np.pi/20,
                            ref_pt = f1.face_center)
    f5.rotate_about_plane(pt1_2, pt2_2, pt3_2, np.pi/20,
                            ref_pt = f1.face_center)
    f5.rotate_about_plane(pt1_3, pt2_3, pt3_3, np.pi/20,
                            ref_pt = f1.face_center)
    pt1_4, pt2_4, pt3_4 = tfr.get_rotation_plane(f4, f5)
    f5.rotate_about_plane(pt1_4, pt2_4, pt3_4, np.pi/20,
                            ref_pt = f1.face_center)
    f5.plot(draw, r)
    f6.rotate_about_plane(pt1_1, pt2_1, pt3_1, np.pi/20,
                            ref_pt = f1.face_center)
    f6.rotate_about_plane(pt1_2, pt2_2, pt3_2, np.pi/20,
                            ref_pt = f1.face_center)
    f6.rotate_about_plane(pt1_3, pt2_3, pt3_3, np.pi/20,
                            ref_pt = f1.face_center)
    f6.rotate_about_plane(pt1_4, pt2_4, pt3_4, np.pi/20,
                            ref_pt = f1.face_center)
    pt1_5, pt2_5, pt3_5 = tfr.get_rotation_plane(f5, f6)
    f6.rotate_about_plane(pt1_5, pt2_5, pt3_5, np.pi/20,
                            ref_pt = f1.face_center)
    f6.plot(draw, r)
    f7.rotate_about_plane(pt1_1, pt2_1, pt3_1, np.pi/20,
                            ref_pt = f1.face_center)
    f7.rotate_about_plane(pt1_2, pt2_2, pt3_2, np.pi/20,
                            ref_pt = f1.face_center)
    f7.rotate_about_plane(pt1_3, pt2_3, pt3_3, np.pi/20,
                            ref_pt = f1.face_center)
    f7.rotate_about_plane(pt1_4, pt2_4, pt3_4, np.pi/20,
                            ref_pt = f1.face_center)
    f7.rotate_about_plane(pt1_5, pt2_5, pt3_5, np.pi/20,
                            ref_pt = f1.face_center)
    ## Here, f6 and f7 don't have a common vertex anymore.
    # This doesn't make sense since they started off with
    # two common vertices and then all the same operations
    # were applied to them.
    pt1_6, pt2_6, pt3_6 = tfr.get_rotation_plane(f6, f7)
    ##
    f7.rotate_about_plane(pt1_6, pt2_6, pt3_6,
                            np.pi/20,
                            ref_pt = f1.face_center)
    f7.plot(draw, r)
    im.save("Images//RotatingCube//im" +
                    str(1).rjust(4, '0') +
                    ".png")

########
def zigzag_working():
    r = rotation(4, np.pi*17/60.0)
    f1 = tg.Face1('-0-0')
    f2 = tg.Face1('00--')
    f3 = tg.Face1('0--0')
    f4 = tg.Face1('+0-0')

    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    for i in range(10):
        im.save("Images//RotatingCube//im" +
                            str(0).rjust(4, '0') +
                            ".png")
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        f1.plot(draw, r)
        pt1_1, pt2_1, pt3_1 = tfr.get_rotation_plane(f1, f2)
        f2.rotate_about_plane(pt1_1, pt2_1, pt3_1, np.pi/20,
                                ref_pt = f1.face_center)
        f2.plot(draw, r)
        f3.rotate_about_plane(pt1_1, pt2_1, pt3_1, np.pi/20,
                                ref_pt = f1.face_center)
        pt1_2, pt2_2, pt3_2 = tfr.get_rotation_plane(f2, f3)
        f3.rotate_about_plane(pt1_2, pt2_2, pt3_2, np.pi/20,
                                ref_pt = f1.face_center)
        f3.plot(draw, r)
        f4.rotate_about_plane(pt1_1, pt2_1, pt3_1, np.pi/20,
                                ref_pt = f1.face_center)
        f4.rotate_about_plane(pt1_2, pt2_2, pt3_2, np.pi/20,
                                ref_pt = f1.face_center)
        pt1_3, pt2_3, pt3_3 = tfr.get_rotation_plane(f3, f4)
        f4.rotate_about_plane(pt1_3, pt2_3, pt3_3, np.pi/20,
                                ref_pt = f1.face_center)
        f4.plot(draw, r)
        im.save("Images//RotatingCube//im" +
                        str(i).rjust(4, '0') +
                        ".png")

