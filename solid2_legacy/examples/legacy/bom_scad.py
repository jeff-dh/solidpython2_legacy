#! /usr/bin/env python3

# Basic shape with several repeated parts, demonstrating the use of
# solid.utils.bill_of_materials()
#
# Basically:
#   -- Define every part you want in the Bill of Materials in a function
#   -- Use the 'bom_part' decorator ahead of the definition of each part's function
#           e.g.:
# @bom_part()
# def my_part():
#     pass
#   -- Optionally, you can add a description and a per-unit cost to the
#       decorator invocations.
#
#   -- To generate the bill of materials, call solid.utils.bill_of_materials()
#
#       -ETJ 08 Mar 2011

from solid2 import *
from solid2_legacy.utils import EPSILON
from solid2_legacy.bill_of_materials import bill_of_materials, bom_part, set_bom_headers

head_rad = 2.65
head_height = 2.8

nut_height = 2.3
nut_rad = 3

m3_rad = 1.4

doohickey_h = 5

set_bom_headers("link", "leftover")


def head():
    return cylinder(h=head_height, r=head_rad)


@bom_part("M3x16 Bolt", 0.12, currency="€", link="http://example.io/M3x16", leftover=0)
def m3_16(a=3):
    bolt_height = 16
    m = union()(
            head(),
            translate((0, 0, -bolt_height))(
                    cylinder(r=m3_rad, h=bolt_height)
            )
    )
    return m


@bom_part("M3x12 Bolt", 0.09, leftover=0)
def m3_12():
    bolt_height = 12
    m = union()(
            head(),
            translate((0, 0, -bolt_height))(
                    cylinder(r=m3_rad, h=bolt_height)
            )
    )
    return m


@bom_part("M3 Nut", 0.04, currency="R$")
def m3_nut():
    hx = cylinder(r=nut_rad, h=nut_height, _fn=6)
    n = difference()(
            hx,
            translate((0, 0, -EPSILON))(
                    cylinder(r=m3_rad, h=nut_height + 2 * EPSILON)
            )
    )
    return n


@bom_part()
def doohickey(c):
    hole_cyl = translate((0, 0, -EPSILON))(
            cylinder(r=m3_rad, h=doohickey_h + 2 * EPSILON)
    )
    d = difference()(
            cube([30, 10, doohickey_h], center=True),
            translate((-10, 0, 0))(hole_cyl),
            hole_cyl,
            translate((10, 0, 0))(hole_cyl)
    )
    return color(c)(d)


def assembly():
    nut = m3_nut()
    return union()(
            doohickey(c='blue'),
            translate((-10, 0, doohickey_h / 2))(m3_12()),
            translate((0, 0, doohickey_h / 2))(m3_16()),
            translate((10, 0, doohickey_h / 2))(m3_12()),
            # Nuts
            translate((-10, 0, -nut_height - doohickey_h / 2))(nut),
            translate((0, 0, -nut_height - doohickey_h / 2))(nut),
            translate((10, 0, -nut_height - doohickey_h / 2))(nut),
    )


if __name__ == '__main__':
    import sys
    out_dir = sys.argv[1] if len(sys.argv) > 1 else None

    a = assembly()
    bom = bill_of_materials(a)
    file_out = scad_render_to_file(a, out_dir=out_dir)

    print(f"{__file__}: SCAD file written to: \n{file_out}")
    print(bom)

    print("Or, Spreadsheet-ready TSV:\n\n")
    bom = bill_of_materials(a, csv=True)
    print(bom)
