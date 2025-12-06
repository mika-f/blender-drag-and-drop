# Blender Add-on: Drag and Drop Support

Blender add-on for importing some files from drag-and-drop.

## Supported Formats

- `*.3mf` (Required [Blender 3MF Format](https://github.com/Ghostkeeper/Blender3mfFormat))
- `*.abc`
- `*.bvh`
- `*.dae` (Not supported in Blender 5.0+ due to Collada removal)
- `*.fbx`
- `*.glb`
- `*.gltf`
- `*.obj`
- `*.ply`
- `*.pmx` (Required [MMD Tools](https://extensions.blender.org/add-ons/mmd-tools/))
- `*.stl`
- `*.svg`
- `*.usd`
- `*.usda`
- `*.usdc`
- `*.vrm` (Required [VRM format](https://extensions.blender.org/add-ons/vrm/))
- `*.x3d` (Required [Web3D X3D/VRML2](https://extensions.blender.org/add-ons/web3d-x3d-vrml2-format/) when greater than Blender 4.4)
- `*.wrl`

## Planned

- `*.mqo` (Required [Metasequoia File Importer/Exporter](https://github.com/nutti/blender-mqo))
- Add file format and add-on pair you want to supported!
- or PR for additional features is also welcome!

## Supported Blenders

v3.0.0 supports the following versions of Blender:

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
- Blender 3.6.7 (x64 - Windows)
- Blender 3.6.8 (x64 - Windows)
- Blender 3.6.9 (x64 - Windows)
- Blender 3.6.10 (x64 - Windows)
- Blender 3.6.11 (x64 - Windows)
- Blender 3.6.12 (x64 - Windows)
- Blender 3.6.13 (x64 - Windows)
- Blender 3.6.14 (x64 - Windows)
- Blender 3.6.15 (x64 - Windows)
- Blender 3.6.16 (x64 - Windows)
- Blender 3.6.17 (x64 - Windows)
- Blender 3.6.18 (x64 - Windows)
- Blender 3.6.19 (x64 - Windows)
- Blender 3.6.20 (x64 - Windows)
- Blender 4.0.0 (x64 - Windows)
- Blender 4.0.1 (x64 - Windows)
- Blender 4.0.2 (x64 - Windows)

v4.0.0 supports the following versions of Blender:

- Blender 4.1.0
- Blender 4.1.1
- Blender 4.2.0 or greater

v1.2.0 supports the following versions of Blender:

- Blender 4.2.0 or greater
- Blender 5.0 or greater (Note: Collada .dae format not supported due to removal in Blender 5.0)

## ScreenShot

## Installation

1. Download Installation Archive from [GitHub Releases](https://github.com/mika-f/blender-drag-and-drop/releases/latest)
2. Extract downloaded zip archive
3. Open the Preferences window and select `Add-ons` tab
4. Press `Install` button, select `drag-and-drop-support.zip` and select `Install Add-on`
5. Select `Community` tab and enable `Import: Drag and Drop Support`

## How to use

1. If you use Blender 4.0 or lower
   1. Please agree to security policy in preferences add-ons view.
2. Drag and Drop some file to 3D view, load it

## Known Issues (Blender 4.0 or lower)

- if the dropped file(s) includes the non-ASCII characters, does not work import correctly.

## Remarks (Blender 4.0 or lower)

- This addon loading DLL written in C++ into Blender via Python, and replace `view3d_ima_empty_drop_poll` function in memory.
  - If you enable this addon, load DLL and replace it function.
  - And you disable this addon, unload DLL and restore it function.

## Contributing

1. Fork it
2. Create your feature branch from `develop` (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request to `develop`

## Release

### 4.x

Create a new pull request from GitHub to bump versions with pr template.

### 3.x

1. Create a new pull request from `develop` to `blender-3`, and merge it.
2. Create a new pull request from `blender-3/topic` to `blender-3` for bump version, and merge it.
3. After pull merge commit, tagging and pushing it.

## License

MIT by [@6jz](https://twitter.com/6jz)
