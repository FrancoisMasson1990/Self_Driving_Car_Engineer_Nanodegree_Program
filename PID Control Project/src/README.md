Parameters of PID controller

Description of PID values in PID control

P (proportional) accounts for present values of the error. For example, if the error is large and positive, the control output will also be large and positive.

I (integral) accounts for all past values of the error. For example, if the current output is not sufficiently strong, the integral of the error will accumulate over time, and the controller will respond by applying a stronger action.

D (differential) accounts for possible future trends of the error, based on its current rate of change.

Finally parameters

PID parameters used for steering angles:

p value: 0.1
i value: 0.001
d value: 2.8
PID parameters used for throttle:

p value: 0.45
i value: 0.000
d value: 0.5
How to tune the parameters

The parameters are tuned manually with the order of: p, d, i. The d and i are first setted to be zeros, and 0.2 is used for the p value. I adjust the p value up and down till it could drive around the first corner and hard to imporve more. Then I keep the p value as it is, and increase the d value. Use the same approach for d value and i value.

In order to automatically fine tune the parameters, an optimization algorithm twiddle could be used.