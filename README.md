# SmartMirror

Work in Progress !
(not functional)

# Installation
pip install -r requirements.txt
####Optional
For Raspberry Pi specific Camera:
pip install picamera

For legacy web engine:
TODO

Create "config.json" in root directory.

Example:
```json
{
  "webEngine": "standart", // (or "legacy")
  "camera": "generic",  // (or "pi")
  "serverPort": 5000,
  "apiKeys": [
    {
      "widget": "WeatherNow",
      "name": "APPID",
      "key": "*************"
    },
    {
      "widget": "WeatherForecast",
      "name": "APPID",
      "key": "*************"
    }
  ]
}
```

# Testing Guide
## Recognition Test
### Preparation
Download yale face database and put it in the test_data folder.
## Camera Test and View Test
These tests are not yet automated. Close the window per hand after a few seconds.