# connect_4_ai

Timofey Shichalin
CS-441 Artificial Intelligence Final Project
Portland State University Fall 2022


This goal of this project is to compare the following two algorithms: 
    1) Minimax (with alpha-beta pruning)
    2) Monte-Carlo Tree Search (with a random rollout policy)

For more info about the project, algorithms used, and findings, see the pdf file.

== == File Hierarchy == ==

-src
    -board
        -board.py -> Implementation of the Connect-4 board.
    -battle_agents.py -> Allows the two agents to play each other.
    -mcts.py -> Implementation of the Monte-Carlo Tree Search agent.
    -minimax.py -> Implementation of the Minimax agent.
    -testmcts.py -> Allows a user to play against the MCTS agent.
    -testminimax.py -> Allows a user to play against the Minimax agent
    -time_cmp.py -> Times how long it takes for an agent to return a move.

-CS-441 Final Project Report.pdf -> Final report for the project. Records findings and info on algorithms used.

-READMY.md -> This document.

[![Open in StackBlitz](https://developer.stackblitz.com/img/open_in_stackblitz.svg)](https://stackblitz.com/github/timshicha/connect_4_ai)

== == == == == == == == == ==
