#ifndef wirelessConnection_HPP
#define wirelessConnection_HPP

#define W_OK              0
#define W_ERR_INIT        10
#define W_ERR_FTC         11

typedef struct 
{
    char ssid[20];
    char pass[20];
} wirelessConnection ;

int init_wifi();
int connect(wirelessConnection *input);
void send_data_to_server(const char *data);

//void send_udp_data(const char *data);


#endif