# jf

jf is a short package that provides many useful Python 
tools allowing to write high-level code efficiently.
Basically, it provides tools for diminishing cognitive 
load during scripting. jf is not intended to be used
in production code but for research use, as it is made 
for scientists and not for developers.


Basically, jf handles utils function to accelerate
and facilitate the setup of projects. It also handles
proper project architecture in a simple and flexible way.


## Projects


A project requires 3 things :
- code
- data
- output

That's why `jf` projects are always like this. 
To init a `jf` project, just create a "root.jf" file.


## Exports

jf brings facilities for easily exports outputs.
js implements an `Experiment` class that requires
a location, a name and is able to export results 
or objects. The location must be for convenience, you can
use folder and subfolders as much as you want. The name
must, by convention, must express the scientific question
related with the experiment. This is the center and we advise
to keep an internal or external index of these experiments.
Finally the result exported must have all information about
parameters. It generally has no name but is self
explanatory.