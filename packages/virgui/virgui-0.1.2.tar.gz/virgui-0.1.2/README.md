# virgo-gui

Prototype for the virgo control room gui

## Installation

Currently available on [pypi](https://pypi.org/project/virgui/)

Recommend to use in a fresh conda/python environment, you might mess up existing environments.

If using conda

```bash
conda create -n virgui-test
conda activate virgui-test
```

Then

```bash
pip install virgui
virgui
```

Will start up the program. Keep an eye out for the terminal, this is where any errors will appear.

## Usage

Currently there is only one layout available, a simple cavity.

Click on the different components to see the parameter values (no editing so far)

In the 'calculate' tab, you should be able to run an Xaxis and see the plot.

Currently I hardcoded in three powerdetectors.

![layout screen](layout.png)

![calculate screen](calculate.png)
