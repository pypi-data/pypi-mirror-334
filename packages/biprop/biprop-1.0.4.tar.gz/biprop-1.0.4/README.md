# Biprop - A Python Library for Calculating Biproportional Apportionments

> [!CAUTION]
> DO NOT use this repository to calculate the official results of actual elections! The code in this repository was not formally verified and might not always deliver correct results or terminate.

Welcome to the `biprop` library. This library is meant for election enthusiats and statistics nerds like me who want to ask questions like
> How would the parliament of country X look like if they used biproportional apportionment in their last election?

or
> How would the apportionment change if party Y and Z ran together as one and if we introduced a quorum that parties have to fulfill?

The `biprop` library contains all the tools you need to answer these questions and more.

## Installation

You can install `biprop` with `pip` using
```
pip install biprop
```

## Basic Usage

To demonstrate the basic usage of the `biprop` library, we will replicate the calculations from the [example from this Wikipedia article](https://en.wikipedia.org/wiki/Biproportional_apportionment#Specific_example). We start with importing the `biprop` library and defining the votes, region and party names from the example:
```
>>> import biprop as bp
>>> party_names = ['A', 'B', 'C']
>>> region_names = ['I', 'II', 'III']
>>> votes = [[123,  45, 815],
...          [912, 714, 414],
...          [312, 255, 215]]
```
Now we can use the votes to define an election and calculate the upper and lower apportionments:
```
>>> e = bp.Election(votes, party_names=party_names, region_names=region_names, total_seats=20)
>>> e.upper_apportionment(which='parties')
array([ 5, 11,  4])
>>> e.upper_apportionment(which='regions')
array([7, 5, 8])
>>> e.lower_apportionment()
Lower apportionment converged after 2 iterations.
array([[1, 0, 4],
       [4, 4, 3],
       [2, 1, 1]])
```
We indeed arrive at the same seat distribution as the example in the Wikipedia article. You can find more usage examples and more detailed explanations in the [Examples directory of the project's GitHub page](https://github.com/herold-t/biprop/tree/main/Examples).

## Examples and Tutorial

You can find practical examples and detailed explanations in the tutorial iPython notebooks in the [Examples directory of the project's GitHub page](https://github.com/herold-t/biprop/tree/main/Examples). The tutorials are still being worked on and are not yet complete.

## Version 0

> [!WARNING]
> Version `0.1.0` is outdated and is not maintained anymore. Users still using this version are encouraged to migrate to version `1.x.x`.

If you still need access to the version `0.1.0`, you can find the code for it in the [v0 directory](https://github.com/herold-t/biprop/tree/main/v0). This directory includes the `biprop.py` module which implements the version `0.1.0`. It also contains an `example.py` module that uses the 2019 and 2023 Swiss National Council Elections to demonstrate how to use `biprop.py`.
