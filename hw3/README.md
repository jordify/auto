Homework #3

Autonomic Computing Fall 2011

By: Jorge Gomez

Last Modified: Fri Oct 14, 2011 at 15:48

Data:

  Run times for cap 50 (N: time rate)
  
  * 10: 097.951 9.7510
  * 20: 200.215 10.018
  * 30: 295.338 9.8446
  * 40: 393.414 9.8354
  * 50: 442.972 8.8594

  Run times for cap 75 (N: time rate)
  
  * 10: 063.960 6.3960
  * 20: 128.410 6.4205
  * 30: 192.311 6.4104
  * 40: 256.539 6.4135
  * 50: 320.581 6.4116

  Run times for cap 100 (N: time rate)
  
  * 10: 047.661 4.7661
  * 20: 097.664 4.8723
  * 30: 143.366 4.7789
  * 40: 191.105 4.7776
  * 50: 239.053 4.7811

Operating point (u,y) = (75,6.4104)

|  N   |  ü   |     ÿ    |
|------|------|----------|
|  10  |  50  |  9.7510  |
|  20  |  50  |  10.018  |
|  30  |  50  |  9.8446  |
|  40  |  50  |  9.8354  |
|  50  |  50  |  8.8594  |
|------|------|----------|
|  10  |  75  |  6.3960  |
|  20  |  75  |  6.4205  |
|  30  |  75  |  6.4104  |
|  40  |  75  |  6.4135  |
|  50  |  75  |  6.4116  |
|------|------|----------|
|  10  | 100  |  4.7661  |
|  20  | 100  |  4.8723  |
|  30  | 100  |  4.7789  |
|  40  | 100  |  4.7776  |
|  50  | 100  |  4.7811  |

Answer to 5:
Use 10 for the input to the model which will return an expected
difference from operating point output. In this case 10 will return
-0.427536 which if you add to the 6.4104 is 5.982864. 5.98 is the
throughput, so to get expected program time you multiply by N, giving
2m 29.5715s as the expected time.

The following is the structure of the files and folders included in this
submission.

  * ./hw3.py -> program used to run experiments and gather data
  * ./analyze3.py -> program used to make model and get RMSE and plot
  * ./modelVsOutput.png -> plot of results
  * ./README.md -> (This document) write-up
