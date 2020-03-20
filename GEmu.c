/*
   -GCli 간 udp 통신에서 server 역할
   -dbus 주소: kr.gooroom.GEmu
   -GCli에서 받은 명령을 전달받음
 */

# include "header.h"

int main() 
{
    struct sockaddr_in listenSocket, clientSocket;
    sd_bus_error error = SD_BUS_ERROR_NULL;
    sd_bus_message *reply = NULL;
    sd_bus *bus = NULL;
    int listenFD;
    char *result;
    int r;
    int recv_len;
    char readBuff[BUFFER_SIZE];
    int addr_len;
    char cmd;

    listenFD = socket(AF_INET, SOCK_DGRAM, 0);

    memset(&listenSocket, 0, sizeof(listenSocket));
    memset(&clientSocket, 0, sizeof(clientSocket));

    listenSocket.sin_family = AF_INET;
    listenSocket.sin_addr.s_addr = htonl(INADDR_ANY);
    listenSocket.sin_port = htons(PORT);
    addr_len = sizeof(clientSocket);


    r = sd_bus_open_system(&bus);
    r = sd_bus_request_name(bus, "kr.gooroom.GEmu", 0);

    if (bind(listenFD, (struct sockaddr *) &listenSocket, sizeof(listenSocket)) == -1) 
    {
        printf("Can not bind.\n");
        return -1;
    }

    while (1) 
    {
        recv_len = recvfrom(listenFD, readBuff, BUFFER_SIZE, 0,
                            (struct sockaddr *)&clientSocket, &addr_len);

        readBuff[recv_len]='\0';
        printf("readBuff=%s\n", readBuff);

        r = sd_bus_call_method(bus,
                "kr.gooroom.GHub",   /* service to contact */
                "/kr/gooroom/GHub",  /* object path */
                "kr.gooroom.GHub",   /* interface name */
                "input_task",           /* method name */
                &error,              /* object to return error in */
                &reply,                  /* return message on success */
                "s",                 /* input signature */
                readBuff);            /* first argument */
     
        r = sd_bus_message_read(reply, "s", &result);
        printf("%s %d(%s)\n", result, r, strerror(r)); //print log

        sendto(listenFD, result, strlen(result), 0,\
                        (struct sockaddr*)&clientSocket, sizeof(clientSocket));
    }

finish:
    close(listenFD);
    sd_bus_error_free(&error);
    sd_bus_message_unref(reply);
    sd_bus_unref(bus);

    return r < 0 ? EXIT_FAILURE : EXIT_SUCCESS;
}
