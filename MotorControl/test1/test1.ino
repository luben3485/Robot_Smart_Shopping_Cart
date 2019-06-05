#include "motor.h"
/*-----input velocity & angle-----*/
double velocity,angle;

void setup(){
    pinMode(GPIO1, OUTPUT);
    pinMode(MOTOR1, OUTPUT);
    pinMode(GPIO2, OUTPUT);
    pinMode(MOTOR2, OUTPUT);
    pinMode(ENCODER1 , INPUT);
    pinMode(ENCODER2 , INPUT);
    Serial.begin(9600);
    EncoderInit();

    //digitalWrite(GPIO1 , HIGH);
    //digitalWrite(GPIO2 , LOW);
}

void loop(){ 
    serial_update();

    //String trans = String(speed2 , 2);
    //char s[10] = {};
    //trans.toCharArray(s,10);
    //s[strlen(s)]='\n';
    //Serial.write(s);
    //delay(1000);

    //PWM2 = 100;
    //Serial.write(speed1);
    //char s[10];
    //sprintf(s , "%lf" , speed1);
    //s[strlen(s)]= '\n';
    //Serial.write(s);

    analogWrite(MOTOR1 , PWM1);
    analogWrite(MOTOR2 , PWM2);
}

void serial_update(){
    static String inString = "";
    bool finish_receive = false;
    if(Serial.available()){
        delay(10);
        char inChar = Serial.read();
        if(inChar != ' ' && inChar != '\n'){
            inString += (char)inChar;
        }
        else{
            if(inChar == ' '){
                velocity = inString.toDouble();
                char result[10]={};
                inString.toCharArray(result,10);
                //sprintf(result,"%lf",velocity);
                result[strlen(result)]='\n';
                Serial.write(result);
                inString = "";
            }
            else if(inChar == '\n'){
                angle = inString.toDouble();
                char result[10] = {};
                inString.toCharArray(result,10);
                //sprintf(result,"%lf",angle);
                result[strlen(result)]='\n';
                Serial.write(result);
                /*if(angle < 0){
                    Serial.write('h');
                    Serial.write('\n');
                }*/
                finish_receive = true;
                inString = "";
            }
        }
    }

    if(finish_receive){
        if(velocity == 0){
            if(angle < 0){
                digitalWrite(GPIO1,HIGH);
                digitalWrite(GPIO2,HIGH);
                vcmd1 = abs(angle)/MAX_SELF_ANGLE * MAX_VELOCITY;
                vcmd2 = abs(angle)/MAX_SELF_ANGLE * MAX_VELOCITY;
            }
            else if(angle > 0){
                digitalWrite(GPIO1,LOW);
                digitalWrite(GPIO2,LOW);
                vcmd1 = angle / MAX_SELF_ANGLE * MAX_VELOCITY;
                vcmd2 = angle / MAX_SELF_ANGLE * MAX_VELOCITY;
            }
            else if(angle == 0){
                digitalWrite(GPIO1,HIGH);
                digitalWrite(GPIO2,LOW);
                vcmd1 = velocity;
                vcmd2 = velocity;
            }
        }
        else{
            digitalWrite(GPIO1,HIGH);
            digitalWrite(GPIO2,LOW);
            velocity >= MAX_FOLLOW_VELOCITY ? velocity = MAX_FOLLOW_VELOCITY : velocity = velocity;
            angle >= MAX_FOLLOW_ANGLE ? angle = MAX_FOLLOW_ANGLE : angle = angle;
            if(angle < 0){
                vcmd1 = MappingVelocity(velocity) + 0.1 * (WHEEL_WIDTH / 2) * abs(angle);
                vcmd2 = MappingVelocity(velocity) - 0.1 * (WHEEL_WIDTH / 2) * abs(angle);
            }
            else if(angle > 0){
                vcmd1 = MappingVelocity(velocity) - 0.1 * (WHEEL_WIDTH / 2) * angle;
                vcmd2 = MappingVelocity(velocity) + 0.1 * (WHEEL_WIDTH / 2) * angle;
            }
            else if(angle == 0){
                vcmd1 = MappingVelocity(velocity);
                vcmd2 = MappingVelocity(velocity);
            }
        }
    }
    /*if(velocity == 0){
        if(angle < 0){
            digitalWrite(GPIO1,HIGH);
            digitalWrite(GPIO2,HIGH);
            vcmd1 = abs(angle)/MAX_SELF_ANGLE * MAX_VELOCITY;
            vcmd2 = abs(angle)/MAX_SELF_ANGLE * MAX_VELOCITY;
        }
        else if(angle > 0){
            digitalWrite(GPIO1,LOW);
            digitalWrite(GPIO2,LOW);
            vcmd1 = angle/MAX_SELF_ANGLE * MAX_VELOCITY;
            vcmd2 = angle/MAX_SELF_ANGLE * MAX_VELOCITY;
        }
        else if(angle == 0){
            digitalWrite(GPIO1,HIGH);
            digitalWrite(GPIO2,LOW);
            vcmd1 = velocity;
            vcmd2 = velocity;
        }
    }
    else{//velocity != 0
        velocity >= MAX_FOLLOW_VELOCITY ? velocity = MAX_FOLLOW_VELOCITY : velocity = velocity; //maximum velocity = 20
        angle >= MAX_FOLLOW_ANGLE ? angle = MAX_FOLLOW_ANGLE : angle = angle;
        digitalWrite(GPIO1,HIGH);
        digitalWrite(GPIO2,LOW);
        if(angle < 0){
            vcmd1 = velocity + (WHEEL_WIDTH / 2) * abs(angle);
            vcmd2 = velocity - (WHEEL_WIDTH / 2) * abs(angle);
            vcmd1 = MappingVelocity(vcmd1);
            vcmd2 = MappingVelocity(vcmd2);
        }
        else if(angle > 0){
            vcmd1 = velocity - (WHEEL_WIDTH / 2) * angle;
            vcmd2 = velocity + (WHEEL_WIDTH / 2) * angle;
            vcmd1 = MappingVelocity(vcmd1);
            vcmd2 = MappingVelocity(vcmd2);
        }
        else if(angle == 0){
            vcmd1 = velocity;
            vcmd2 = velocity;
        }
    }*/
}

double MappingVelocity(double velocity){
    return velocity / MAX_FOLLOW_CAL_VELOCITY * MAX_VELOCITY;
}
