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

using namespace std;


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
    /*
    char * pch;
    std::vector<char *> v;
    pch = strtok (str," ");
    while (pch != NULL)
    {
        //printf ("%s\n",pch);
        v.push_back(pch);
        pch = strtok (NULL, " ,.-");
    }
    char* action = v[0];
    char* level = v[1];
    */
    //printf("action:%s level:%s\n", action, level);
    // ---------- instruction split ----------
    cout << (atoi(str) - 48) << endl;
    switch(atoi(str) - 48){ // convert action to 'int' and do decision
        case 0: // stop
            cout << "stop\n" << endl;
            break;
        case 1: // velcity modify
            cout << "velcity modify\n" << endl;
            break;
        case 2: // turn left
        case 3: // turn right
            cout << "turn\n" << endl;
            break;
        case 4:
            //cout << "None Inst\n" << endl;
            break;
        case 8:
            cout << "first Test\n" << endl;
            break;
        default:
            cout << "Unexcept value\n" << endl;
    }
}


int main()
{
    char inputBuffer[256];
    
    int sockfd_client = createTCPsocket(7878); // create socket at port:7878
    while(true)
    {
        bzero(inputBuffer, 256);
        cout << "start receive" << endl;
        int inst_length = read(sockfd_client, inputBuffer, sizeof(inputBuffer)); // receive instruction
        cout << "finish receive" << endl;
        if(inst_length > 0) // receive something
        {
            printf("Get:%s\n", inputBuffer);
            check(inputBuffer);
            memset(inputBuffer, 0, sizeof(inputBuffer)); // clear inputBuffer
            cout << "finish get" << endl;
        }
        else // receive nothing
            printf("hey hey\n");
        usleep(500000); // delay
    }
    return 0;
}
