## SmoothDE
smoothDE is a python library that trains on data samples to learn a probability distribution and then make predictions about the probability of points.

![plot](./example.png)

It uses a lattice based approach to estimate the smoothness of a potential probability distribution. Thus, while smoothDE can predict distributions in 1, 2, 3, or more dimensions, as the lattice increases in dimension smoothDE becomes slower.

Module docs: [gitlab pages](https://smoothde-rhys-m-adams-1c812a8316486f0551b8cc30ae17414bbd5eb4bba.gitlab.io/)

### Installation
The only tricky part of this install seems to be the scikit-sparse library. I suggest installing the fundamental libraries first as this installation gives faster scikit-sparse results:
```
# mac
brew install suite-sparse

# linux
sudo apt-get install libsuitesparse-dev
```
these commands were lifted straight from the scikit-sparse installation instructions. The conda installation did not perform operations as quickly as a fresh install of the above system libraries.
smoothDE should install scikit-sparse as a pip, but you can install it yourself if the next step doesn't work.
You should be able to run:
```
pip install -e <file path>/smoothDE/
```
or use the internet
```
pip install smoothDE
```
The preprint describing this library mathematically can be found and cited at here currently:
[preprint](http://osf.io/nwyur_v2)

### Quick usage
To fit a density estimator:
```
import numpy as np
from smoothDE.estimator import DensityFitter
X = np.array([[3, 1],[2,2],[1, 1],[2,3]]) #observed data points, 3 samples in 2D
box = [[0,4,32],[0,4,32]] # fit field from 0 to 4, with 32 gridpoints in 2 dimensions
dr = DensityFitter(box, dpow=2) # create the smoothDE object
record = dr.fit(X) # fit the data, returns a record of the fit results
phi = dr.predict(X) # predict phi from data, X in this case for conciseness
p = np.exp(-phi) # pdf estimate of X points
```

If you have many features and want to just calculate the 1 dimensional fields, you can use the make_subfields module:
```
from smoothDE.make_subfields import MakeSubfields

trf = MakeSubfields([2], [128],n_threads=1, paired=True)
trf.fit(X, np.array([0,0,1, 1]))
sub_fields = trf.predict(X)
print(sub_fields)
sub_field_array = trf.transform(X)
print(sub_field_array)
```
For 2D fields, the lists need to be length 2 in MakeSubfieds;

```
from smoothDE.make_subfields import MakeSubfields

trf = MakeSubfields([2, 2], [128, 48],n_threads=1, paired=True)
trf.fit(X, np.array([0,0,1, 1]))
sub_fields = trf.predict(X)
print(sub_fields)
sub_field_array = trf.transform(X)
print(sub_field_array)
```

Demo also shown at [youtube demo](https://www.youtube.com/watch?v=xu-XspvaRrQ)
