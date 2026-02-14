# L3

Languange 3 is a simple programming language, that has some basic features. These includes functions that introduces/accesses scope in different ways. 

Things that add scope include 

* program
* let
* letRec
* abstract
* reference

Some things, such as `let` add scope that only accessible through the body, while other funcitons, such as `letRec` recursively passes down the scope to its children's body.


Certain functions do not introduce scope, and just does its action, these includes

* immediate 
* primitive

immediate is a leaf, and will always pass, but primitive has children, and will only pass if its children are valid.