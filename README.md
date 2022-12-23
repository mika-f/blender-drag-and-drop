# Blender Add-on: Drag and Drop Support

Blender add-on for importing some files from drag-and-drop.

## Supports

v2.0.0 supports the following versions of Blender:

- Blender 3.3.2 (x64 - Windows)
- Blender 3.4.0 (x64 - Windows)
- Blender 3.4.1 (x64 - Windows)

if you want to use the older than Blender 3.3.2, please use v0.x:

- Blender 3.1.0 (x64 - Windows)
- Blender 3.1.1 (x64 - Windows)
- Blender 3.1.2 (x64 - Windows)
- Blender 3.2.0 (x64 - Windows)
- Blender 3.2.1 (x64 - Windows)
- Blender 3.2.2 (x64 - Windows)
- Blender 3.3.0 (x64 - Windows)
- Blender 3.3.1 (x64 - Windows)

## Installation

1. Download Installation Archive from [Natsuneko Laboratory](https://docs.natsuneko.moe/en-US/drag-and-drop-support/)
2. Open the Preferences window and select `Add-ons` tab
3. Press `Install` button, select downloaded zip-archive and select `Install Add-on`
4. Select `Community` tab and enable `Import: Drag and Drop Support`

## How to use

1. Drag and Drop some file to 3D view, load it
   1. if you want to configure import, please use `Drag and Drop Support` tab in 3D view.

## Known Issues

- if the dropped file(s) includes the non-ASCII characters, does not work import correctly.

## Remarks

- This addon loading DLL written in C++ into Blender via Python, and replace `view3d_ima_empty_drop_poll` function in memory.
  - If you enable this addon, load DLL and replace it function.
  - And you disable this addon, unload DLL and restore it function.

## License

MIT by [@6jz](https://twitter.com/6jz)
