# Setup Tutorial

This guide explains how to set up the tools needed to compile and run the project on Windows.

## 1. About the compiler (MSYS2 is recommended, not required)

You do **not** need MSYS2 specifically: any working C++ compiler, Python interpreter and CMake installation will do (for example MSVC, a standalone MinGW, or the tools from your Linux/macOS package manager).

However, **MSYS2 is the recommended option** because:

- it installs `g++`, `python` and `cmake` with a single package manager (`pacman`);
- it is well integrated with **Visual Studio Code** (IntelliSense, debugging, CMake Tools find the toolchain easily);
- everyone working on the project ends up with the same compiler and versions.

If you already have a working toolchain, you can skip to [section 4](#4-building-the-project).

## 2. Installing MSYS2

1. Download the installer from <https://www.msys2.org> and run it. Keep the default install path (`C:\msys64`).
2. At the end of the installation, open the **MSYS2 UCRT64** terminal (search for "MSYS2 UCRT64" in the Start menu). Make sure it is the *UCRT64* one, not MSYS or MINGW32.
3. Update the base system:

   ```bash
   pacman -Syu
   ```

   The terminal may ask you to close it. Reopen the **UCRT64** terminal and run the command again until there is nothing left to update.

## 3. Installing the compilers and tools

In the **MSYS2 UCRT64** terminal run:

```bash
pacman -S --needed mingw-w64-ucrt-x86_64-gcc \
                   mingw-w64-ucrt-x86_64-gdb \
                   mingw-w64-ucrt-x86_64-cmake \
                   mingw-w64-ucrt-x86_64-ninja \
                   mingw-w64-ucrt-x86_64-python \
                   mingw-w64-ucrt-x86_64-python-pip
```

What each package gives you:

| Package  | Purpose                              |
|----------|--------------------------------------|
| `gcc`    | C and C++ compilers (`gcc`, `g++`)   |
| `gdb`    | debugger (used by VS Code)           |
| `cmake`  | build system generator               |
| `ninja`  | fast build tool used by CMake        |
| `python` | Python interpreter (+ `pip`)         |

### Add the tools to the Windows PATH

So that the tools are available from VS Code, PowerShell, `cmd` and `.bat` files (not only from the MSYS2 terminal), add this folder to your Windows `PATH`:

```
C:\msys64\ucrt64\bin
```

To do it: *Start menu → "Edit the system environment variables" → Environment Variables → Path → Edit → New*. Then **close and reopen** any terminal or VS Code window.

### Check that everything works

Open a new PowerShell (or the UCRT64 terminal) and run:

```bash
g++ --version
python --version
cmake --version
```

Each command should print a version number.

## 3b. VS Code integration

1. Install [Visual Studio Code](https://code.visualstudio.com).
2. Install these extensions:
   - **C/C++** (Microsoft)
   - **CMake Tools**
   - **Python**
3. Open the project folder with *File → Open Folder*.
4. If VS Code asks for a compiler/kit, choose the one located in `C:\msys64\ucrt64\bin` (GCC).

## 4. Building the project

The file `build.bat` (**Windows only**) compiles the project and creates a `build/` folder containing all the executables.

From the project root, run it from PowerShell or `cmd`:

```bat
build.bat
```

(or double-click it).

When it finishes you will find the `build/` folder with all the compiled executables inside.

> On Linux/macOS `build.bat` does not work. Compile the sources manually with your own compiler instead.

## 5. Working on the project

Once `build/` exists, you can use the scripts in the project to work on it: run the executables from `build/`, launch the Python scripts, and so on. Re-run `build.bat` whenever you change the C++ sources to regenerate the executables.

## Troubleshooting

- **`g++` is not recognized**: `C:\msys64\ucrt64\bin` is not in your `PATH`, or you did not restart the terminal / VS Code after editing it.
- **`pacman` errors about keys or databases**: run `pacman -Syu` again in the UCRT64 terminal.
- **Wrong Python used**: run `where python` and check that the MSYS2 one (`C:\msys64\ucrt64\bin\python.exe`) is the one you expect.
