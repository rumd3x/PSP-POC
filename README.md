# PSP-POC

Running Python scripts to control PSP hardware as a proof of concept.

## Running Code

Copy this project contents into `PSP/GAME` folder and execute it like you would with any other homebrew.

## How it works

- This POC takes advantage of Stackless Python. It uses Stackless Python 2.5.2 port for PSP from [this repo](https://github.com/carlosedp/PSP-StacklessPython).

- When launched, the interpreter will try to find a "script.py" file in its directory and run it. If there is none, it will exit to XMB.

- The `python` folder teoretically holds all python built-in libraries (the ones from Python 2.5 at least, but it is possible that some features were not fully ported) and are used by the Stackless Python interpreter at run time. **KEEP THIS FOLDER.**

- While developing, to enable code-completion for the PSP specific libraries, copy the files inside `dev-mocks` to the same folder as `script.py`. They are embeded into `EBOOT.PBP` when running on real hardware, so it can be safely discarted on a final release build.
