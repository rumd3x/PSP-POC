# PSP-POC

Running Python scripts to control PSP hardware as a proof of concept.

## Running Code

Copy the project into `PSP/GAME` folder and execute like any other homebrew.

## How it works

- This POC takes advantage of Stackless Python. It uses Stackless Python version 2.5.2 from [this repo](https://github.com/carlosedp/PSP-StacklessPython)

- To enable code-completion for the psp wrappers, copy the files inside `dev-mocks` to the same folder as `script.py`. They are embeded into `EBOOT.PBP` when running on real hardware.

- The `python` folder teoretically holds all python built-in libraries (the ones from Python 2.5 at least, but it is possible that some features were not fully ported) and are used by the Stackless Python interpreter at run time. **KEEP THIS FOLDER.**
