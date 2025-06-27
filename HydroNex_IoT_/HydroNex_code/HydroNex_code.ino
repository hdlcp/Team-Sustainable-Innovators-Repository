#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// Identifiant de connexions wifi
const char* ssid = "TestESP33";
const char* password = "12345678";
 void setupWiFi() {
   Serial.print("Connexion à ");
   Serial.println(ssid);
   WiFi.begin(ssid, password);
   while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.print(".");
   }
   Serial.println("\nConnecté à WiFi !");
 }

// Serveur cible 
const char* serverName = "https://api-hydro-nex.onrender.com/api/donnees";

// Capteurs 
#define ONE_WIRE_BUS 4
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature ds18b20(&oneWire);

#define TURBIDITY_PIN 34
#define PH_PIN 36
// Paramètres de calibration
const float PH7_VOLTAGE = 1.61;    // Tension pour pH=7 (ESP32: 3.3V système)
const float PH_SLOPE = 0.116;       // Pente en V/pH
const int SAMPLES = 50;            // Nombre d'échantillons pour moyennage
#define SALINITY_PIN 33
#define BATTERY 32

float readVoltage(int pin) {
  int analogValue = analogRead(pin); // Lit une valeur analogique entière compris entre 0 et 4095.0 car 
  // la résolution du ADC1 de l'esp32 est de 12 bit
  return analogValue * (3.3 / 4095.0); // en volt
}

float calculatePH() {
  // Lecture avec moyennage pour précision
  long sum = 0;
  for(int i = 0; i < SAMPLES; i++) {
    sum += analogRead(PH_PIN);
    delayMicroseconds(1000); // 1ms entre lectures
  }
 
  // Conversion en tension
  float average = sum / (float)SAMPLES;
  float voltage = (average / 4095.0) * 3.3; // ESP32: 12-bit, 3.3V ref
  // Conversion en pH
  float ph = abs(7.0 + ((PH7_VOLTAGE - voltage) / PH_SLOPE));
  if(ph <0 || ph > 14){
    ph = NAN;
  }
  return ph;
  //return 7 + ((2.5 - voltage) / 0.18);  // à ajuster selon calibration
  // ph = 7 + (2.5 - V)/0.18 avec V la tension lu sur la broche analogique du capteur de ph
  // 7 est le point zéro indiquant la neutralité du liquide (ni acide, ni basique)
  // 2.5 volt est la tension à ph = 7
}

float calculateSalinity(float conductivity, float temperature) {
  //Conpensation de température (référence 25°C)
  float tempCoef = 1.0 + 0.02 * (temperature - 25.0);
  float compensationConductivity = conductivity / tempCoef;
  //Convertion en salinité
  float salinity = 0.1 * compensationConductivity;
  return salinity; 
}

float calculateNTU() {
  //La tension à la sortie du capteur présente d'importantes variation.
  //Nous avons donc effectuée 800 mesures puis retenues la moyenne.
   float ntu = 0.0, volt = 0.0;
    for(int i=0; i<800; i++)
    {
        volt += ((float)analogRead(TURBIDITY_PIN)/4095.0)*3.3; // Cela normalise la valeur
        // lue pour qu'elle soit comprise entre 0 et 1.
        //ensuite on multiplie le résultat par 5 pour avoir une tension réel comprise entre 0 et 5V.
    }
    volt = volt / 800;
    volt = round_to_dp(volt, 2);
     // Conversion de la tension 3.3V vers équivalent 5V pour utiliser l'équation originale
    float volt_5v_equivalent = volt * (5.0 / 3.3);
   
    // Vérification de la plage valide (en équivalent 5V)
    if (volt_5v_equivalent < 2.5) {
        ntu = 3000;
    }
    else if (volt_5v_equivalent > 4.2) {
        ntu = 0; // Eau très claire
    }
    else {
        // Application de l'équation du graphique avec la tension équivalente 5V
        float v = volt_5v_equivalent;
        ntu = -1120.4 * (v * v) + 5742.3 * v - 4352.9;
        // Vérification que le résultat est cohérent
        if (ntu < 0) {
            ntu = 0; 
        }
    }
  return ntu;
}

float round_to_dp( float in_value, int decimal_place )
{
  float multiplier = powf( 10.0f, decimal_place );
  in_value = roundf( in_value * multiplier ) / multiplier;
  return in_value;
}

void setup() {
  Serial.begin(115200);
  ds18b20.begin();
  // Configuration ADC pour meilleure précision
  analogReadResolution(12);        // 12-bit (0-4095)
  analogSetAttenuation(ADC_11db);  // Permet lecture jusqu'à 3.9V
  setupWiFi();
  delay(2000); // Stabilisation initiale
}

void loop() {
  // Température
  ds18b20.requestTemperatures();
  float temperature = ds18b20.getTempCByIndex(0);
  float pH = calculatePH();

  // Voltages analogiques
  float salinityVoltage = readVoltage(SALINITY_PIN);
  float battery_level = (readVoltage(BATTERY)*(5/3.3))*(100/5);//Pour obtenir une valeure en pourcentage

  // Valeurs converties
  float salinity = calculateSalinity(salinityVoltage, temperature);
  float turbidity = calculateNTU();

  // Affichage local
  // Serial.print("Temp: °C ");
  // Serial.println(temperature);
  // Serial.print("pH : ");
  // Serial.println(pH);
  // Serial.print("Salinité: (g/L)");
  // Serial.println(salinity);
  // Serial.print("turbidité (NTU): ");
  // Serial.println(turbidity);
  // Serial.print("battery_level (%): ");
  // Serial.println(battery_level);

   //Envoi HTTP POST
   if (WiFi.status() == WL_CONNECTED) {
     HTTPClient http;
     http.begin(serverName);
     http.addHeader("Content-Type", "application/json");

     String json = "{\"dispositif_id\":" + String(0, 10) +
                     ",\"temperature\":" + String(temperature, 10) +
                     ",\"salinity\":" + String(salinity, 10) +
                     ",\"ph\":" + String(pH, 10) +
                     ",\"turbidity\":" + String(turbidity, 10) + 
                     ",\"battery_level\":" + String(battery_level, 10) +"}";

     int httpResponseCode = http.POST(json);
     Serial.print("HTTP Response code: ");
     Serial.println(httpResponseCode);

     http.end();
   } else {
     Serial.println("WiFi déconnecté !");
   }

  delay(5000);  // Pause de 5 secondes
}