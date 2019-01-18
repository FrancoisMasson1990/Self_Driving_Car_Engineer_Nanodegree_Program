#include "PID.h"

/**
 * TODO: Complete the PID class. You may add any additional desired functions.
 */

PID::PID() {}

PID::~PID() {}

void PID::Init(double Kp_, double Ki_, double Kd_) {
  /**
   * TODO: Initialize PID coefficients (and errors, if needed)
   */
  Kp = Kp_;
  Ki = Ki_;
  Kd = Kd_;

  p_error = 0;
  i_error = 0;
  d_error = 0; 

}

void PID::UpdateError(double cte) {
  /**
   * TODO: Update PID errors based on cte.
   */
  double pre_cte = p_error;

  p_error  = cte;
  i_error += cte;
  d_error  = cte - pre_cte;
}

double PID::OutputSteerAng() {

  return -Kp*p_error - Ki*i_error - Kd*d_error;
}


/**
 * Compute the throttle by PID controller
 * @param max_thro max throttle value
 * @return the computed throttle value
 */
double PID::OutputThrottle(double max_thro){

  return max_thro - Kp*p_error - Ki*i_error - Kd*d_error;
}

//double PID::TotalError() {
  /**
   * TODO: Calculate and return the total error
   */
  //return -Kp*p_error - Ki*i_error - Kd*d_error;
  //return 0.0;  // TODO: Add your total error calc here!
//}