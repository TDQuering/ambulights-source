# AmbuLights

This is the source code for Team Datanooga's 2020 Smart City Project, AmbuLights.

## Branches

There are two main branches in this repository, the master branch and the development branch. The master branch contains the latest stable prototype of our software, which *should* work properly. The development branch contains whatever progress we've worked on most recently. No guarantees of stability, features, or even being able to run the code on the development branch.

## Dependencies

Our project uses many of python's builtin libraries. It specifically uses `time`, `datetime`, `threading`, `queue`, `random`, and `enum`. It also uses `graphics.py`, an open-source graphics library created by John Zelle, so special thanks to him for providing such a useful piece of software for free. You can find it [here](https://mcsp.wartburg.edu/zelle/python/graphics.py) if you're interested. The version that we use is also stored in this repository.

## This Version

This is a __development__ version.  
Status: __Working.__ This version of the code will run. However, the `Route` feature which we are in the middle of implementing currently does nothing.

## Notes & Next Steps

The next step should be to refactor `IntersectionManager` to use a 2D array to store intersections. Here's some example code that I was messing around with in IDLE as a reference: 

```python
twoDim = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]

def index_2D(array, index):
	index_1 = math.floor(index / len(array))
	index_2 = index % len(array[0])
	return array[index_1][index_2]
```

After this, it will be much easier to work with turns from a `Route` object. 