# Changelog for DougLib


## 1.0.14 (2017-02-22)
+ Fix GitLab CI
+ Added automatic doc generation and upload.


## 1.0.13 (2017-02-22)
+ At some point in the past, I ported to Py3
+ added missing `max_dist_sqrd` function
+ Removed SciPy requirement
+ Updates to CI
+ Added sphinx docs
+ Various cleanup.
+ Unknown changes. Sorry!


## 1.0.6 (2015-03-30)
+ Added new function to douglib.gdw: 'gdw_fo' used for calculating GDW with
  fixed offsets instead of letting the program choose between the four
  default options.


## 1.0.5 (2015-03-02)
+ Added "delta" method to CodeTimer.


##1.0.4 (2015-01-28)
+ Fixed bug in douglib.gdw.gdw() where die were incorrectly being counted as
  'off flat' and 'outside flat exclusion'. This was caused by
  double-counting of die_y/2 on lines 133 and 139.
