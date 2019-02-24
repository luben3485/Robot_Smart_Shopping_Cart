#include<stdio.h>
#include<math.h>
#include<wiringPi.h>
#include<sys/time.h>
#include<unistd.h>
#include<stdlib.h>
#include<stdint.h>
#include<signal.h>

#define ENCODER_PIN1 7 //pin7
#define ENCODER_PIN2 0 //pin11
#define MOTOR1_PIN1 1 //pin12
#define MOTOR1_PIN2 3//pin15 gpio control 
#define MOTOR2_PIN1 23 //pin33
#define MOTOR2_PIN2 2//pin13 gpio control

int reso;
double rad;
double sample_time;

//car_speed
double speed1, speed2;
double duration;

//encoder
int encoder_pre;
int encoder_end;
int encoder_check;
int diff;
struct timeval start, finish;

//PI control
double KP_1 , KP_2 , KI_1 , KI_2 , G_1 , G_2 , in_1 , in_2;
int PWM1, PWM2;

void init(){
	reso = 9;
	rad = 360/(reso*2)*M_PI/180;
	sample_time = 1000;
	
	//encoder
	encoder_pre = 0;
	encoder_end = 0; //end flag
	encoder_check = 0;
	diff = -1;

	//PI control
	PWM1 = 800;		PWM2 = 800;
	KP_1 = 300;		KP_2 = 500;
	KI_1 = 1000;		KI_2 = 1000;
	G_1 = 0;		G_2 = 0;
	in_1 = 0; 		in_2 = 0;

	//car_speed
	speed1 = 0;//motor1
	speed2 = 0;//motor2
	duration = 0;
}

void encoder(int);
double car_speed(int);
int pi_control(int , double , double);
void sighandler(int);

int main(){
	if(wiringPiSetup()== -1){
		exit(1);
	}

	init();
	double vcmd1, vcmd2;
	pinMode(ENCODER_PIN1, INPUT);
	pinMode(ENCODER_PIN2, INPUT);
	pinMode(MOTOR1_PIN1, PWM_OUTPUT);
	pinMode(MOTOR2_PIN1, PWM_OUTPUT);
	pinMode(MOTOR1_PIN2, OUTPUT);
	pinMode(MOTOR2_PIN2, OUTPUT);
	
	digitalWrite(MOTOR1_PIN2 , LOW);
	digitalWrite(MOTOR2_PIN2 , HIGH);

	signal(SIGINT, sighandler);

	//printf("Enter vcmd1 vcmd2:");
	//scanf("%lf %lf", &vcmd1, &vcmd2);
	//printf("start\n");	

	//pwmWrite(MOTOR1_PIN1 , 600);

	//pwmWrite(MOTOR2_PIN1 , 600);
	/*pwmWrite(MOTOR1_PIN1, 60);
	pwmWrite(MOTOR2_PIN1, 60);
	delay(500);*/

	while(1){
		pwmWrite(MOTOR1_PIN1, PWM1);
		pwmWrite(MOTOR2_PIN1, PWM2);
		//printf("start\n");
		//speed1 = car_speed(1);
		//printf("speed1\n");
		//speed2 = car_speed(2);
		//printf("speed2\n");
		//printf("%lf   %lf\n", speed1 , speed2);
		//printf("current_speed2 = %lf\n", speed2);
		//PWM1 = pi_control(1 , 2, speed1);
		//PWM2 = pi_control(2 , 2, speed2);
		//printf("%lf %d %lf %d\n", speed1 , PWM1, speed2 , PWM2);
		//printf("PWM2 = %d\n", PWM2);
	}
	return 0;
}

void encoder(int pin){
	int encoder_current;
	if(pin == 1)
		encoder_current = digitalRead(ENCODER_PIN1);
	else 
		encoder_current = digitalRead(ENCODER_PIN2);
	//printf("encoder_current = %d\n", encoder_current);
	/*if(encoder_current != encoder_pre){
		if(encoder_check == 0){//not start to count
			if(diff < 0)
				diff = 0;
		}
		else{ //end to count
			if(diff < 0)
				diff = 0;
		}

		if(diff < 0)
			diff = 0;
	}
	else if(encoder_current == encoder_pre){
		if(diff >=0 && diff < 3)
			diff ++;
		else{
			check = 1;
			gettimeofday(&start , NULL);
			diff = -1;
		}
	}*/
	/*if(encoder_current != encoder_pre){
		if (encoder_check == 0){
			encoder_check = 1;
			gettimeofday(&start , NULL);
		}
		else{
			encoder_check = 0;
			gettimeofday(&finish , NULL);
		}
	}
	else if(encoder_current == encoder_pre && encoder_check == 1)
		encoder_count ++;*/

	if(encoder_current != encoder_pre){
		if(diff == -1)
			diff = 0;
		else if((diff >= 0 && diff < 4) && encoder_check == 1) //noise
			diff = -1;
	}
	else if(encoder_current == encoder_pre){
		if(diff >= 0 && diff < 4)
			diff ++;
		if(diff >= 4){
			if(encoder_check == 0){
				encoder_check = 1; //start to count
				gettimeofday(&start , NULL);
				diff = -1;
			}
			else{//encoder_check = 1
				encoder_check = 0; //end counting
				gettimeofday(&finish , NULL);
				diff = -1;
				encoder_end = 1;//end flag
			}
		}	
	}
	encoder_pre = encoder_current;
}

double car_speed(int pin){
	while(1){
		encoder(pin);
		usleep(sample_time);
		if(encoder_end = 1 && encoder_check == 0)
			break;
	}

	duration = (finish.tv_sec - start.tv_sec) + (finish.tv_usec - start.tv_usec) * 0.000001;

	double speed = rad * 0.0675 / duration;
	encoder_end = 0;
	return speed;
}

int pi_control(int num , double vcmd, double speed){
	int PWM = 0;
	double ERR , G , in;
	
	ERR = vcmd - speed;

	if(num == 1){
		G_1 = ERR * KP_1;
		in_1 = in_1 + ERR * duration * KI_1;
		
		G = G_1;
		in = in_1;
	}
	else{
		G_2 = ERR * KP_2;
		in_2 = in_2 + ERR * duration * KI_2;
	
		G = G_2;
		in = in_2;
	}

	if(G > 1023)
		G = 1023;
	else if(G < -1023)
		G = -1023;

	if(in > 1023)
		in = 1023;
	else if(in < -1023)
		in = -1023;

	PWM = G + in;
	if(abs(PWM) >= 1023)
		PWM = 1023;
	else 
		PWM = abs(PWM);
	//else if(abs(PWM < 100))
		//PWM = 100;

	return PWM;
}

void sighandler(int signum){
	pwmWrite(MOTOR1_PIN1,0);
	pwmWrite(MOTOR2_PIN1,0);
	exit(1);
}
