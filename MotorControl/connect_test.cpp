#include <iostream>
#include <vector>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sstream>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <typeinfo>
#include<wiringPi.h>
#include<sys/time.h>
#include<stdint.h>
#include<math.h>

using namespace std;

#define ENCODER_PIN1 7 //pin7
#define ENCODER_PIN2 0 //pin11
#define MOTOR1_PIN1 1 //pin12
#define MOTOR1_PIN2 3 //pin15 gpio control
#define MOTOR2_PIN1 23 //pin33
#define MOTOR2_PIN2 //gpio control

int reso , sample_time;
double rad ;

//encoder
int encoder_pre , encoder_count , encoder_check;
struct timeval start, finish;

//speed
double vcmd1 , vcmd2;
double duration;

//PI control
double KP , KI , G , in , ERR;

//functions
void encoder(int);
double car_speed(int);
int pi_control(double , double); //change speed
void motor_stop();
void motor_acc(int);
void motor_turn_left(int);
void motor_turn_right(int);

void init(){
    reso = 9;
    rad = 360/(reso * 2) * M_PI / 180;
    sample_time = 1000;

    //encoder
    encoder_pre = 0;
    encoder_count = 0;
    encoder_check = 0;

    //speed
    vcmd1 = 0; vcmd2 = 0;
    duration = 0;

    //PI control
    KP = 500;
    KI = 2000;
    G = 0; in = 0; ERR = 0;
}


int createTCPsocket(int port) // create socket
{
    char inputBuffer[256] = {};
    char message[] = {"Connection success."};
    int sockfd = 0, forClientSockfd = 0;
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if(sockfd == -1)
        printf("Fail to create a socket.\n");

    // socket connetion
    struct sockaddr_in serverInfo, clientInfo;
    bzero(&serverInfo, sizeof(serverInfo));

    serverInfo.sin_family = AF_INET;
    serverInfo.sin_addr.s_addr = INADDR_ANY;
    serverInfo.sin_port = htons(7878);
    bind(sockfd, (struct sockaddr *)&serverInfo, sizeof(serverInfo));
    listen(sockfd, 5);

    socklen_t addrlen = sizeof(clientInfo); // in c++11 can't use int 
                                            // instead of using socklen_t
    forClientSockfd = accept(sockfd, (struct sockaddr *) &clientInfo, &addrlen);
    recv(forClientSockfd, inputBuffer, sizeof(inputBuffer), 0);
    printf("Get:%s\n", inputBuffer);
    send(forClientSockfd, message, sizeof(message), 0);
    return forClientSockfd;
}


void check(string instruction) // check instruction funtion
{
    // ---------- instruction split ----------
    char str[1024];
    strcpy(str, instruction.c_str());
    char * pch;
    std::vector<char *> v;
    pch = strtok (str," ");
    while (pch != NULL)
    {
        printf ("%s\n",pch);
        v.push_back(pch);
        pch = strtok (NULL, " ,.-");
    }
    char* action = v[0];
    char* level = v[1];
    printf("action:%s level:%s\n", action, level);
    // ---------- instruction split ----------
    switch(atoi(action)){ // convert action to 'int' and do decision
        case 0: // stop
            cout << "stop\n" << endl;
            motor_stop();
            break;
        case 1: // velcity modify
            cout << "velcity modify\n" << endl;
            motor_acc(atoi(level));
            break;
        case 2: // turn left
            cout << "turn left\n" << endl;
            motor_turn_left(atoi(level));
            break;
        case 3: // turn right
            cout << "turn right\n" << endl;
            motor_turn_right(atoi(level));
            break;
        default:
            cout << "Unexcept value\n" << endl;
    }
}


int main()
{
    char inputBuffer[256] = {};
    int sockfd_client = createTCPsocket(7878); // create socket at port:7878

    if(wiringPiSetup() == -1){
        exit(1);
    }

    init();
    int PWM1 = 0; //initial
    int PWM2 = 0; //initial
    double speed1 , speed2;

    //setup
    pinMode(ENCODER_PIN1 , INPUT);
    pinMode(ENCODER_PIN2 , INPUT);
    pinMode(MOTOR1_PIN1 , PWM_OUTPUT);
    pinMode(MOTOR2_PIN2 , PWM_OUTPUT);
    pinMode(MOTOR1_PIN2 , OUTPUT);

    digitalWrtie(MOTOR1_PIN2 , HIGH);

    while(true)
    {
        int inst_length = read(sockfd_client, inputBuffer, sizeof(inputBuffer)); // receive instruction
        if(inst_length > 0) // receive something
        {
            printf("Get:%s\n", inputBuffer);
            check(inputBuffer);
            memset(inputBuffer, 0, sizeof(inputBuffer)); // clear inputBuffer
        }
        else // receive nothing
            printf("hey hey\n");
        
        pwmWrite(MOTOR1_PIN1 , PWM1);
        pwmWrite(MOTOR2_PIN2 , PWM2);

        speed1 = car_speed();
        pi_control(vcmd1 , speed1);
        speed2 = car_speed();
        pi_control(vcmd2 , speed2);
        //usleep(100000); // delay
    }
    return 0;
}

void encoder(int pin){
    int encoder_current;
    if(pin == 1)
        encoder_current = digitalRead(ENCODER_PIN1);
    else
        encoder_current = digitalRead(ENCODER_PIN2);
    
    if(encoder_current != encoder_pre){
        if(encoder_check == 0){
            encoder_check = 1;
            gettimeofday(&start , NULL);
        }
        else{
            encoder_check = 0;
            gettimeofday(&finish , NULL);
        }
    }
    else if(encoder_current == encoder_pre && encoder_check = 1)
        encoder_count ++;
    
    encoder_pre = encoder_current;
}

double car_speed(int pin){
    while(1){
        encoder(pin);
        usleep(sample_time);
        if(encoder_count > 0 && encoder_check == 0)
            break;
    }
    duration = (finish.tv_sec - start.tv_sec) + 0.000001 * (finish.tv_usec - start.tv_usec);

    double speed = rad * 0.0675 / duration;
    encoder_count = 0;

    return speed;
}

void motor_stop(){
    vcmd1 = 0;
    vcmd2 = 0;
}

void motor_acc(int level){
    switch(level){
        case 1:
            break;
        
        case 2:
            break;
        
        case 3:
            break;
        
        case 4:
            break;
        
        case 5:
            break;
    }
}

void motor_turn_left(int level){
    switch(level){
        case 1:

    }
}

void motor_turn_right(int level){
    switch(level){
        case 1:
            break;
    }
}

int pi_control(double vcmd, double speed){
    int PWM = 0;

    ERR = vcmd - speed;
    G = ERR * KP;
    in = in + ERR * duration * KI;

    if(G > 1023)
        G = 1023;
    else if(G < -1023)
        G = -1023;
    
    if(in > 1023)
        in = 1023;
    else if(in < -1023)
        in = -1023;

    PWM = G + in;
    if(abs(PWM) > =960)
        PWM = 960;
    else if(abs(PWM) < 100)
        PWM = 100;
    
    return PWM;
}