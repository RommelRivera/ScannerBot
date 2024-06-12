
/*
Integrantes:
Aleman Rodriguez, Diego Fernando     25-2714-2018
Medina Maradiaga, William Alexander  25-2298-2020
Rivera Pinto, Rommel Alejandro       25-0728-2020
Rodríguez Dueñas, Ernesto Vladimir   25-2824-2019
Vasquez Sanchez, Luis Jaime          25-1315-2020
*/

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <Servo.h>
#include <Math.h>

extern "C" {
  #include "user_interface.h"
  #include "wpa2_enterprise.h"
  #include "c_types.h"
}

// Información de red UTEC
char utec_ssid[] = "UTEC-Academico";
char username[] = "2507282020";
char identity[] = "2507282020";
char utec_password[] = "09112000";

// Información de red regular
char red_ssid[] = "KIRA";
char red_password[] = "RomGab1409";

// Información de servidor
ESP8266WebServer server(80);
IPAddress IP_local(192,168,0,25);
IPAddress gateway(192,168,0,1);
IPAddress subred(255,255,255,0);

// Datos del servomotor
int posicion = 0;
Servo servo;
int pinServo = 9;

// Datos del sensor ultrasonido
int pinTrigger = 2;
int pinEcho = 3;
long tiempo;
int delayGiro = 50;  // Testear si se pueden valores más pequeños para reducir tiempo de escaneo, con 50 son ~9s, con 25 son ~5s

// Datos para carro
Servo motor;
int pinMotor = 5;
int poderAvanzar = 110;
int poderRetroceder = 70;
int delayAvanzar = 525;
int delayRetroceder = 525;
int delayDobleAvanzar = 1050;
int delayDobleRetroceder = 1250;
Servo direccion;
int pinDireccion = 6;
int direccionIzquierda = 55;
int direccionDerecha = 125;

int WiFiResult() {
  if (WiFi.waitForConnectResult() == WL_CONNECTED) {
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());

    return 1;
  } else {
    return 0;
  }
}

int WiFiUTEC() {
  WiFi.mode(WIFI_STA);
  Serial.begin(115200);
  delay(1000);
  Serial.setDebugOutput(true);
  Serial.printf("SDK version: %s\n", system_get_sdk_version());
  Serial.printf("Free Heap: %4d\n", ESP.getFreeHeap());

  // Setting ESP into STATION mode only (no AP mode or dual mode)
  wifi_set_opmode(STATION_MODE);

  struct station_config wifi_config;

  memset(&wifi_config, 0, sizeof(wifi_config));
  strcpy((char*)wifi_config.ssid, utec_ssid);
  strcpy((char*)wifi_config.password, utec_password);

  wifi_station_set_config(&wifi_config);
  // wifi_set_macaddr(STATION_IF, target_esp_mac);


  wifi_station_set_wpa2_enterprise_auth(1);

  // Clean up to be sure no old data is still inside
  wifi_station_clear_cert_key();
  wifi_station_clear_enterprise_ca_cert();

  wifi_station_set_enterprise_identity((uint8*)identity, strlen(identity));
  wifi_station_set_enterprise_username((uint8*)username, strlen(username));
  wifi_station_set_enterprise_password((uint8*)utec_password, strlen((char*)utec_password));


  wifi_station_connect();

  return WiFiResult();
}

int WiFiPublico() {
  WiFi.begin(red_ssid, red_password);

  return WiFiResult();
}

void setup() {
  // Inicializar conexión serial
  Serial.begin(115200);

  // Intentar conexión a red de UTEC
  // if (WiFiUTEC() == 0) {
  //   Serial.print("Conexión fallida, nada va a funcionar.");
  // }

  // Intentar conexión a red regular
  if (WiFiPublico() == 0) {
    Serial.print("Conexión fallida, nada va a funcionar.");
  }

  // Inicializar servomotor
  servo.attach(pinServo);
  servo.write(0);

  // Inicializar sensor ultrasonido
  pinMode(pinTrigger, OUTPUT);
  pinMode(pinEcho, INPUT);
  digitalWrite(pinTrigger, LOW);

  // Inicializar carro
  motor.attach(pinMotor);
  motor.write(90);
  direccion.attach(pinDireccion);
  direccion.write(90);

  // Inicializar servidor
  server.begin();

  server.on("/escanear/", escanear);
  server.on("/avanzar/", avanzar);
  server.on("/retroceder/", retroceder);
  server.on("/izquierda/", izquierda);
  server.on("/derecha/", derecha);
}

// Escaneo del area
void escanear() {
  digitalWrite(pinTrigger, LOW);
  delayMicroseconds(2);
  digitalWrite(pinTrigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrigger, LOW);

  tiempo = pulseIn(pinEcho, HIGH);
  server.send(200, "text/plain", String(tiempo));

  if(posicion == 180) {
    posicion = 0;
  } else {
    posicion++;
  }

  servo.write(posicion);
}

// Código para mover el carro al frente
void avanzar() {
  motor.write(poderAvanzar);
  delay(delayAvanzar);
  motor.write(90);

  server.send(200, "text/plain", "avanzado");
}

// Código para mover el carro hacia atrás
void retroceder() {
  motor.write(poderRetroceder);
  delay(delayRetroceder);
  motor.write(90);

  server.send(200, "text/plain", "retrocedido");
}

// Código para hacer girar el carro a la izquierda
void izquierda() {
  direccion.write(direccionIzquierda);
  delay(25);
  motor.write(poderAvanzar);
  delay(delayAvanzar);
  motor.write(90);
  delay(25);
  direccion.write(direccionDerecha);
  delay(25);
  motor.write(poderRetroceder);
  delay(delayDobleRetroceder);
  motor.write(90);
  delay(25);
  direccion.write(direccionIzquierda);
  delay(25);
  motor.write(poderAvanzar);
  delay(delayDobleAvanzar);
  motor.write(90);
  delay(25);
  direccion.write(direccionDerecha);
  delay(25);
  motor.write(poderRetroceder);
  delay(delayDobleRetroceder);
  motor.write(90);
  delay(25);
  direccion.write(90);

  server.send(200, "text/plain", "izquierda");
}

// Código para hacer girar el carro a la derecha
void derecha() {
  direccion.write(direccionDerecha);
  delay(25);
  motor.write(poderAvanzar);
  delay(delayAvanzar);
  motor.write(90);
  delay(25);
  direccion.write(direccionIzquierda);
  delay(25);
  motor.write(poderRetroceder);
  delay(delayDobleRetroceder);
  motor.write(90);
  delay(25);
  direccion.write(direccionDerecha);
  delay(25);
  motor.write(poderAvanzar);
  delay(delayDobleAvanzar);
  motor.write(90);
  delay(25);
  direccion.write(direccionIzquierda);
  delay(25);
  motor.write(poderRetroceder);
  delay(delayDobleRetroceder);
  motor.write(90);
  delay(25);
  direccion.write(90);

  server.send(200, "text/plain", "derecha");
}

void loop() {
  server.handleClient();
}