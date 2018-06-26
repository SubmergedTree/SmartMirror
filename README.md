# SmartMirror

v0.1 - Early Alpha

# Road to v1.0
- More Widgets out of the box
- Support CSS
- Support Images

# Supplementary Projects
- Android App TBD
- Web App TBD (not yet started)

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
  "widgetShowTime": 3000,
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

# REST Calls
TBD



# How to create custom widgets
A widget consists of two (v 0.1 - in future versions css will be supported) files:
- <unique_name>Widget.html
- <unique_name>Eval.js

<unique_name> is an project wide unique name for one widget.
The html file must be in the html directory and the js file must be in the js directory

**In future versions demanded file names may differ.**

###html File:
Use a pair of curly brackets with a number inside as placeholder. These placeholders will be replaced in your <unique_name>Eval.js file.

Example:
```html
<b>Chuck Noris Jokes</b> <br> <br>
<div id="chuckNorisWidget"> {0} </div>
```

###js File
It is required to have a function with following arguments:
- url: url for optional rest call
- position: position of widget (1-4)
- widgetType: type/name of widget
- context: context with additional information

This function must be registered with the register function. Use as name the <unique_name> from both files.
You can use the *restCall(url, callback, position, queryString)* function to make a rest call.
The callback has following signature: *chuckNorisCallback(json, position)*.
Replace placeholders with *format('to insert')*.
With *changeWidget(position, html);* you can show the widget to the User.

Example 
```javascript
register("chuckNoris", chuckNorisEval);

function chuckNorisEval(url, position, widgetType, context) {
    restCall(url, chuckNorisCallback, position, context);
}

function chuckNorisCallback(json, position) {
    const formatedHtml = chuckNorisHtml.format(json.value.joke);
    changeWidget(position, formatedHtml);
}
```

Now fire the new widget rest call against your SmartMirror.
It is a post request with a body which should contain:
- widget:<unique_name>
- baseUrl:<url for rest call>

**Only one rest call is permitted for a widget.**


# Testing Guide
## Recognition Test
### Preparation
Download yale face database and put it in the test_data folder.
## Camera Test and View Test
These tests are not yet automated. Close the window per hand after a few seconds.