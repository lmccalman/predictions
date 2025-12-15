# Predictions

This repository contains a tool to analyse and publish the results of
a predction game, played annually by our family.

## The game

    - At the beginning of the year, each family member proposes a number of
      _statements_, which are true/false statements that can be evaluated by
      December 24th of that year (the judging date).

    - Example: "The pope will die". This is implied to be resolved by the
      judging date if the pope is still alive, and will be judged before then
      should the current pope die.
    
    - The statements are annotated with categories.

    - Once the statements are compiled, all family members assign a probability
      to all statements. This is the probability that each statement is
      resolved as true.

    - The scoring for each statement uses a standardised log probability which
      gives the log of the probility mass the person assigned to the outcome
      that occurred, minus the log of the prior, assumed to be 0.5

    - The scores are updated over the course of the year as events get
      resolved, with the remaining staments resolved, final scoring and prizes
      occuring in the family Christmas Eve gathering.

## The Software

The goal of the predictions tool is to create an interative website hosted on
cloud infrastructure that the family can access to examine the game's progress
and explore statistics and comparisons between players. Examples of analyses
could include:

 - performance over time for an indivdual (by year)
 - performance on different categories
 - levels of confidence of different people
 - comparitive analyses between two selected people
 - how people fare on their own predictions compared to other peoples'


## Current status

Initial planning phases. The data are currently stored in xlsx spreadsheets
which need to be ingested into a consistent data format. 

### Ingestion component

This will be a python script that reads the xlsx files and extracts the
questions, predictions and results into a consistent data format suitable for
further processing and hosting online.


### Web frontent

It is not yet decided on the best technology to host the interactive analyses,
and this component has not been started yet.


### Technology stack
 - For python:
    - uv for environment management
    - pytest for unit tests
    - ruff for automatic formatting
    - basedpyright for linting and static analysis
    - click for commandline argument processing









