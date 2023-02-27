import numpy as np
from pyray.rotation import rotation
import pyray.shapes.fourd.tesseract_graph as tg
import pyray.shapes.fourd.tsrct_face_rotation as tfr
import pyray.shapes.fourd.open_tsrct as ot
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


if __name__ == "__main__":
    tst_rotation_three_faces2()
