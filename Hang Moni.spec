# -*- mode: python ; coding: utf-8 -*-

import os
import sys

project_dir = SPECPATH
assets = [
    "PixelifySans.ttf",
    "1 smile.png",
    "2 eye google.png",
    "3 face_down.png",
    "4 close eye jig.png",
    "5 steal from Riho.png",
    "6 tounge out.png",
    "7 anger.png",
    "speach bubble.png",
    "cat_animation-Sheet.png",
    "platform.png",
    "back_ground.png",
    "temple.gif",
]
corpora = [
    ("nltk_data/corpora/words", "nltk_data/corpora/words"),
    ("nltk_data/corpora/wordnet.zip", "nltk_data/corpora"),
]

missing = [
    path
    for path in assets + [source for source, _ in corpora]
    if not os.path.exists(os.path.join(project_dir, path))
]
if missing:
    raise SystemExit(
        "Missing build resources: "
        + ", ".join(missing)
        + ". See BUILDING.md for setup instructions."
    )

datas = [
    (os.path.join(project_dir, path), ".")
    for path in assets
] + [
    (os.path.join(project_dir, source), destination)
    for source, destination in corpora
]

a = Analysis(
    [os.path.join(project_dir, "ui_components.py")],
    pathex=[project_dir],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Hang Moni",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Hang Moni",
)

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="Hang Moni.app",
        icon=None,
        bundle_identifier="com.hangmoni.game",
    )
