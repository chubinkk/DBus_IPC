/*
   -udp접속 후(client) 사용자의 표준입력 대기
   -AppA를 실행/정지시킴.
   -AppA에게 최근 10개 로그를 수집하여 전송하라는 명령 지원
 */
# include "header.h"

#define ANSI_COLOR_RED  "\x1b[31m"
#define ANSI_COLOR_YELLOW  "\x1b[33m"
#define ANSI_COLOR_RESET  "\x1b[0m"

int main(int argc, char *argv[])
{
    struct sockaddr_in connectSocket, server_addr;
    int read_log;
    int addr_len = 0;
    char receiveBuffer[BUFFER_SIZE];


    int cmd=0;
    char c_cmd[3] = {0, };
    int connectFD = socket(AF_INET, SOCK_DGRAM, 0);

    memset(&connectSocket, 0, sizeof(connectSocket));

    connectSocket.sin_family = AF_INET;
    inet_aton("127.0.0.1", (struct in_addr*) &connectSocket.sin_addr.s_addr);
    connectSocket.sin_port = htons(PORT);
    
    addr_len = sizeof(connectSocket);

    if (connect(connectFD, (struct sockaddr*) &connectSocket, sizeof(connectSocket)) == -1)
    {
        printf("Can not connect.\n");
        return -1;
    }

    while (1)
    {
        printf("=========================================\n");
        printf("1.AppA 실행\n");
        printf("2.AppA 로그 수집\n");
        printf("3.AppA 정지\n");
        printf("4.AppA 상태 보기\n");
        printf("5.프로그램 종료\n");
        printf("실행하려는 기능의 번호를 입력하세요: ");
        scanf("%d",&cmd);
        printf("=========================================\n");

        if(cmd==4)
        {
            system("systemctl status myAppA.service");
        }
        else if(cmd==5)
        {
            printf("프로그램을 종료합니다.\n");
            return 0;
        }
        sprintf(c_cmd, "%d", cmd);

        if(sendto(connectFD, c_cmd, strlen(c_cmd),0,\
                    (struct sockaddr*)&connectSocket,sizeof(connectSocket)) <= 0) 
        {
            perror("sendto failed");
            exit(1);
        }
    read_log = recvfrom(connectFD, receiveBuffer, BUFFER_SIZE, 0,\
                            (struct sockaddr *)&connectSocket, &addr_len);
    receiveBuffer[read_log] = '\0';

    printf(ANSI_COLOR_YELLOW);
//printf("log: %s\n", receiveBuffer);

    fputs(receiveBuffer, stdout);
    printf(ANSI_COLOR_RESET);
    fflush(stdout);
    }
   return 0;
}

