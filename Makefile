ARCH = x64
REVISION = 2.5.0

ALL_TASKS = Release

.PHONY: Release
Release:
	./build.bat $(ARCH) "Release" $(REVISION)

.PHONY: clean
clean:
	echo Y | rm -rf ./bin

all: clean $(ALL_TASKS)
	echo