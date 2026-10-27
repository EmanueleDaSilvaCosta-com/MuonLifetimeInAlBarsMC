@echo off
rem Usage:
rem   build.bat                 configure + build everything (Release)
rem   build.bat debug           Debug build
rem   build.bat uniform         build only the "uniform" app
rem   build.bat debug uniform   both
rem   build.bat clean           remove compiled files (keeps the configuration)
setlocal
cd /d "%~dp0"

set "BUILD_TYPE=Release"
set "TARGET="
set "CLEAN=0"

:args
if "%~1"=="" goto run
if /i "%~1"=="debug" set "BUILD_TYPE=Debug" & shift & goto args
if /i "%~1"=="release" set "BUILD_TYPE=Release" & shift & goto args
if /i "%~1"=="clean" set "CLEAN=1" & shift & goto args
set "TARGET=--target %~1"
shift
goto args

:run
where cmake >nul 2>&1
if errorlevel 1 set "PATH=C:\msys64\ucrt64\bin;%PATH%"
where cmake >nul 2>&1
if errorlevel 1 (
    echo cmake not found. Install it in MSYS2 and add C:\msys64\ucrt64\bin to PATH.
    exit /b 1
)

if "%CLEAN%"=="1" (
    if exist build\CMakeCache.txt cmake --build build --target clean
    exit /b %errorlevel%
)

cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=%BUILD_TYPE%
if errorlevel 1 exit /b 1

cmake --build build %TARGET%
if errorlevel 1 exit /b 1

echo Done (%BUILD_TYPE%).
endlocal
