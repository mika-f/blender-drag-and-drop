@echo off
setlocal

cd /d %~dp0

:: check argument
set ARCH=%1
set TARGET="%2"
set VERSION=%3

if "%ARCH%" == "" (
    echo usage: build.bat $arch $target $version
    echo example: build.bat x64 Release 1.0.0
    goto :error_exit
)

if "%TARGET%" == "" (
    echo usage: build.bat $arch $target $version
    echo example: build.bat x64 Release 1.0.0
    goto :error_exit
)

if "%VERSION%" == "" (
    echo usage: build.bat $arch $target $version
    echo example: build.bat x64 Release 1.0.0
    goto :error_exit
)


if not "%ARCH%" == "x64" (
    if not "%ARCH%" == "x86" (
        echo arch must be x64 or x86
        goto :error_exit
    )
)

set PF32=%ProgramFiles(x86)%
if not exist "%PF32%" set PF32=%ProgramFiles%

set VS_WHERE_PATH="%PF32%\Microsoft Visual Studio\Installer\vswhere.exe"

if not exist ""%VS_WHERE_PATH%"" (
    echo vswhere not found
    goto :error_exit
)

for /f "usebackq tokens=*" %%i in (`%VS_WHERE_PATH% -latest -requires Microsoft.Component.MSBuild -find MSBuild\**\Bin\MSBuild.exe`) do (
    if exist "%%i" (
        set MSBUILD=%%i
        goto :msb_found
    )
)

goto :error_exit

:error_exit
exit 1

:success_exit
exit 0

:msb_found
echo MSBuild Found  : %MSBUILD%

echo ******************************************************************************************************
echo Build blender-injection for %2 (%ARCH%)
echo ******************************************************************************************************

"%MSBUILD%" /p:Configuration=%2 /p:Platform=%1 /t:Rebuild src/blender-injection/blender-injection.vcxproj


echo ******************************************************************************************************
echo Build blender-extension for %2 (%ARCH%)
echo ******************************************************************************************************

mkdir bin
del bin\drag-and-drop-support.zip
echo D | xcopy /e src/blender-extension bin/drag-and-drop-support/


echo ******************************************************************************************************
echo Collect Artifacts
echo ******************************************************************************************************

for /f "tokens=2 delims=: " %%i in (%2) do (
    set VERSION=%%i.%3
)

set DEST="bin\%1\DragAndDropSupport-v%VERSION%"

echo Y | rmdir /s "%DEST%"
mkdir "%DEST%"

echo F | xcopy /s "src\blender-injection\%1\"%2"\*.dll" "%DEST%\drag-and-drop-support\"
echo F | xcopy /s "src\blender-extension\*" "%DEST%\drag-and-drop-support\"
echo F | xcopy "src\LICENSE.txt" "%DEST%\"

pwsh -Command  compress-archive "%DEST%\drag-and-drop-support" "%DEST%\drag-and-drop-support.zip"
echo Y | rmdir /s "%DEST%\drag-and-drop-support"

echo ******************************************************************************************************
echo Packaging Artifact
echo ******************************************************************************************************

if exist "%DEST%.zip" (
    del "%DEST%.zip"
)

pwsh -Command compress-archive %DEST% %DEST%.zip


set HASH=
for /F "usebackq skip=1 delims==" %%i in (`certutil -hashfile %DEST%.zip SHA256`) do (
    if not defined HASH (
        set HASH=%%i
    )
)

echo %HASH% > "%DEST%.zip.sha256"

echo "packaged -> %DEST%.zip"
echo "hash -> %HASH%"