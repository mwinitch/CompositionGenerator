
#include <WebServer.h>
#include <WiFi.h>
#include <WiFiUdp.h>

// Initial code for setting up connection
const char* ssid = "";
const char* password = "";
WiFiUDP Udp;
unsigned int localUdpPort = 4210;  //  port to listen on
char incomingPacket[255];  // buffer for incoming packets

void setup()
{
  int status = WL_IDLE_STATUS;
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("");
  
  // Connecting to the buttons
  pinMode(18, INPUT_PULLUP);
  pinMode(32, INPUT_PULLUP);

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to wifi");
  Udp.begin(localUdpPort);
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);

  // Tests that a connection has been established
  bool readPacket = false;
  while (!readPacket) {
    int packetSize = Udp.parsePacket();
    if (packetSize)
     {
      // receive incoming UDP packets
      Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
      int len = Udp.read(incomingPacket, 255);
      if (len > 0)
      {
        incomingPacket[len] = 0;
      }
      Serial.printf("UDP packet contents: %s\n", incomingPacket);
      readPacket = true;
    } 
  }
}

void loop()
{
  // Begin sending button input to the client
  Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
  int colorButton = digitalRead(18);
  int directionButton = digitalRead(32);
  Serial.print(colorButton);
  Serial.print(directionButton);
  Serial.print("\n");
  Udp.printf("%d", colorButton);
  Udp.printf("%d", directionButton);
  Udp.endPacket();
  delay(1000);
}
