# The palaestrAI environments package

## Introduction

This package contains a set of environemnts for palaestrAI that are 
ready-to-use.

## Installation

Clone the repository, install the project with pip:

```bash
pip install -e .
```

## Usage

Use one of the environments in your experiment run file. The environments
live in the `palaestrai.environment` namespace. For example, in your 
experiment run file, set 
`palaestrai_environments.tictactoe:TicTacToeEnvironment` as argument to the 
environment `name` key. Also do not forget to define the respective sensors 
and actuators.

Please consult palaestrAI's main documentation at <http://docs.palaestr.
ai> to learn more.

Have a lot of fun!
