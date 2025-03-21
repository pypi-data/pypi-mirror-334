"""Check that basic features work.

Catch cases where e.g. files are missing so the import doesn't work. It is
recommended to check that e.g. assets are included."""

import sys

platform = sys.platform

if platform != "win32":
    exit(0)
else:
    import pywet

    pywet.main()
