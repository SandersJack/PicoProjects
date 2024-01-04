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

int connect(wirelessConnection *input);

#endif