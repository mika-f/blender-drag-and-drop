ARCH = x64
REVISION = 8

ALL_TASKS =
ALL_TASKS += blender-3-1-0
ALL_TASKS += blender-3-1-1
ALL_TASKS += blender-3-1-2
ALL_TASKS += blender-3-2-0
ALL_TASKS += blender-3-2-1
ALL_TASKS += blender-3-2-2
ALL_TASKS += blender-3-3-0

.PHONY: blender-3-1-0
blender-3-1-0:
	build.bat $(ARCH) "Blender 3.1.0" $(REVISION)

.PHONY: blender-3-1-1
blender-3-1-1:
	build.bat $(ARCH) "Blender 3.1.1" $(REVISION)

.PHONY: blender-3-1-2
blender-3-1-2:
	build.bat $(ARCH) "Blender 3.1.2" $(REVISION)

.PHONY: blender-3-2-0
blender-3-2-0:
	build.bat $(ARCH) "Blender 3.2.0" $(REVISION)

.PHONY: blender-3-2-1
blender-3-2-1:
	build.bat $(ARCH) "Blender 3.2.1" $(REVISION)

.PHONY: blender-3-2-2
blender-3-2-2:
	build.bat $(ARCH) "Blender 3.2.2" $(REVISION)

.PHONY: blender-3-3-0
blender-3-3-0:
	build.bat $(ARCH) "Blender 3.3.0" $(REVISION)

.PHONY: clean
clean:
	echo Y | rmdir /s .\bin

all: clean $(ALL_TASKS)
	echo