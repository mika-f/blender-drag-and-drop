## Prepare for release the new version

### QA CHECKS

- [ ] Is is possible to import files such as FBX files via D&D from Explorer?
- [ ] Is is possible to import files such as Material files via D&D from Asset Explorer in Blender?
  - ([#23 Interferes with some asset browser files](https://github.com/mika-f/blender-drag-and-drop/issues/23))
- [ ] Is it possible to import files such as Image files via D&D from Explorer and create a new plane?
  - ([#29 [Bug]: Image plane is not created](https://github.com/mika-f/blender-drag-and-drop/issues/29))

### RELEASE CHECKS

- [ ] Is the version number bumped / updated?
  - [ ] `.github/ISSUE_TEMPLATE/bug-report.yml`
  - [ ] `src/blender-extension/__init__.py`
  - [ ] `Makefile`
  - [ ] `README.md`
