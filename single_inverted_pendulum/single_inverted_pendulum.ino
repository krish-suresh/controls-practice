#include <Encoder.h>
#include <JrkG2.h>

Encoder joint_0(2, 3);
Encoder slide(18, 19);

JrkG2I2C jrk;

float slide_pos = 0;
float joint_0_pos = 0;
float joint_1_pos = 0;
float slide_pos_prev = 0;
float joint_0_pos_prev = 0;
float joint_1_pos_prev = 0;
float slide_pos_dot = 0;
float joint_0_pos_dot = 0;
float joint_1_pos_dot = 0;
float x_dot_dot = 0;
// -223.60679784 -374.38787001 2853.69348521 1124.31833194
float K_0 = -223.60679784;
float K_1 = -374.38787001;
float K_2 = 2853.69348521;
float K_3 = 1124.31833194;
bool off = false;
int current_time = 0;
int prev_time = 0;
float time_diff = 0;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  while(Serial.available() == 0) {
  }
}
long oldPosition  = -999;
double divideVal = 500;
void loop() {


  current_time = millis();
  time_diff = (current_time - prev_time)/1000.0;
  slide_pos = slide.read()/464.64 * 0.04;
  joint_0_pos = angleWrap(M_PI * 2 * joint_0.read() / 2400.0 + M_PI);

  slide_pos_dot = (slide_pos - slide_pos_prev) / time_diff;
  joint_0_pos_dot = (joint_0_pos - joint_0_pos_prev) / time_diff;
  x_dot_dot = slide_pos*K_0 + slide_pos_dot*K_1 + joint_0_pos*K_2, joint_0_pos_dot*K_3;
  Serial.print(slide_pos,7);
  Serial.print(",");
  Serial.print(slide_pos_dot,7);
  Serial.print(",");
  Serial.print(joint_0_pos,7);
  Serial.print(",");
  Serial.print(joint_0_pos_dot,7);
  Serial.print(" | ");
  Serial.println(x_dot_dot/divideVal,7);
//  if (!off) {
     setForce(x_dot_dot);
//
//  } else {
//     setForce(0);
//  }
  slide_pos_prev = slide_pos;
  joint_0_pos_prev = joint_0_pos;
  prev_time = current_time;

}

void setForce(double x_dot_dot) {

  double motor_power  = x_dot_dot/divideVal; // -1 to 1, neg to to the right
  jrk.setTarget((-motor_power*600)+ 2048);
}

float angleWrap(float angle) {
  while (angle < -M_PI) {
    angle += 2 * M_PI  ;
  }
  while (angle > M_PI) {
    angle -= 2 * M_PI  ;
  }
  return angle;
}
