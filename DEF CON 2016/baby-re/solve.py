import angr
import claripy
import simuvex
import sys
from IPython import embed
import logging
logging.getLogger('ctf.defcon.16.re.baby-re').setLevel(logging.DEBUG)


success=(0x402964)
fail=(0x401693, 0x4017db, 0x401927, 0x401a72, 0x401bbe, 0x401d0d, 0x401e59, 0x401fa7, 0x4020ef, 0x40223b, 0x40237f, 0x4024a0, 0x4025c1, 0x4025e0)


def main():
    proj = angr.Project("baby-re", load_options={'auto_load_libs':False})
    exp = proj.surveyors.Explorer(find=success, avoid=fail)
    exp.run()

    if len(exp.found) < 1:
        print "No path found"
        embed()
    for idx, success_path in enumerate(exp.found):
        print "Path", idx
        for idx in range(13):
            ch = success_path.state.posix.files[0].read_from(1)
            success_path.state.se.add(ch >= ord('0'))
            success_path.state.se.add(ch <= ord('9'))

        try:
            pw = success_path.state.posix.dumps(1).strip("\n").strip("\r").strip("\0")
        except Exception as ex:
            print "Could not find password for path ", idx, " (", ex.message, ")"
            continue
        print "Password for path ", idx, ": [" + pw + "]"


if __name__ == "__main__":
    main()
