# AmbuLights

This is the source code for Team Datanooga's 2020 Smart City Project, AmbuLights.

## Branches

There are two main branches in this repository, the master branch and the development branch. The master branch contains the latest stable prototype of our software, which *should* work properly. The development branch contains whatever progress we've worked on most recently. No guarantees of stability, features, or even being able to run the code on the development branch.

## Dependencies

Our project uses many of python's builtin libraries. It specifically uses `time`, `datetime`, `threading`, `queue`, `random`, `math` and `enum`. It also uses `graphics.py`, an open-source graphics library created by John Zelle, so special thanks to him for providing such a useful piece of software for free. You can find it [here](https://mcsp.wartburg.edu/zelle/python/graphics.py) if you're interested. The version that we use is also stored in this repository.

## This Version

This is a __stable__ version.  
Status: __Working.__

## Future Development
There are still some minor improvements that could be made. For example, it would be better if the triangle waited for the intersection to change before moving. However, that has not yet been implemented as it would probably take a good amount of time to get working properly.