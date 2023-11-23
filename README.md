# Blender Add-on: Drag and Drop Support

Blender add-on for importing some files from drag-and-drop.

## Supports

v2.0.0 supports the following versions of Blender:

- Blender 3.1.0 (x64 - Windows)
- Blender 3.1.1 (x64 - Windows)
- Blender 3.1.2 (x64 - Windows)
- Blender 3.2.0 (x64 - Windows)
- Blender 3.2.1 (x64 - Windows)
- Blender 3.2.2 (x64 - Windows)
- Blender 3.3.0 (x64 - Windows)
- Blender 3.3.1 (x64 - Windows)
- Blender 3.3.2 (x64 - Windows)
- Blender 3.3.3 (x64 - Windows)
- Blender 3.3.4 (x64 - Windows)
- Blender 3.4.0 (x64 - Windows)
- Blender 3.4.1 (x64 - Windows)
- Blender 3.5.0 (x64 - Windows)
- Blender 3.5.1 (x64 - Windows)
- Blender 3.6.0 (x64 - Windows)
- Blender 3.6.1 (x64 - Windows)
- Blender 3.6.2 (x64 - Windows)
- Blender 3.6.4 (x64 - Windows)
- Blender 3.6.5 (x64 - Windows)
- Blender 4.0.0 (x64 - Windows)

## Installation

1. Download Installation Archive from [GitHub Releases](https://github.com/mika-f/blender-drag-and-drop/releases/latest)
2. Extract downloaded zip archive
3. Open the Preferences window and select `Add-ons` tab
4. Press `Install` button, select `drag-and-drop-support.zip` and select `Install Add-on`
5. Select `Community` tab and enable `Import: Drag and Drop Support`

## How to use

1. Drag and Drop some file to 3D view, load it
   1. if you want to configure import, please use `Drag and Drop Support` tab in 3D view.

## Known Issues

- if the dropped file(s) includes the non-ASCII characters, does not work import correctly.

## Remarks

- This addon loading DLL written in C++ into Blender via Python, and replace `view3d_ima_empty_drop_poll` function in memory.
  - If you enable this addon, load DLL and replace it function.
  - And you disable this addon, unload DLL and restore it function.

## Release

Create a new pull request from GitHub to bump versions with pr template.

## License

MIT by [@6jz](https://twitter.com/6jz)
