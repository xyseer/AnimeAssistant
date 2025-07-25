# xyseer/AnimeAssistant

#### Welcome to xyseer-nas-tool/AnimeAssistant !

The AnimeAssistant is part of xy-nas-tool. The xy-nas-tool project aims at gathering useful and powerful tools so that users can get a full-automatic NAS assistant to achieve a better experience.

The AnimeAssistant focuses on automatically subscribing anime series. Users can get the latest anime just like what they do on the video sharing platforms. 

The AnimeAssistant is coding by Python, using Flask flamework to provide an interface for interaction. Docker image are also made for deploying this service into your NAS.

### How to use it?

For users, there are three parts: config file / db file / the AnimeAssistant application.

Config file must under the path "/config" and name as "config.json". It's a json format file which contains basic parameters for the application. The application will automatically generate a default config file when it cannot detect a valid config in "/config/config.json". After the file has been created. Users can edit this config file by manually editing this file or on the webpage(/setting).

DB files will automatically be created by the application for the first time. Users should never modify this file unless you know what you are doing. 

The AnimeAssistant application is very easy to use. Just run the main.py or start your Docker container and then the seivice will start. You can edit the subscroptions and settings with a simple web interface (default port is 12138).



### Latest:0.9b

WARNING: This is still a beta version. Please check the latest stable version unless you want to try and test this new version.

##### New Features:

+ Add EXPERIMENTAL flag for a not so that stable functions. Users who prefer an advanced features can toggle this flag by access `/experimental` and it shows the status of your current EXPERIMENTAL flag.

+ Add new function: Export your subscription as json. (With cover photo as base64 inside)

+ EXPERIMENTAL feature: Add import method. This allows user import from json text shared from others. 

  > [!NOTE]
  >
  > EXPERIMENTAL flag is required.

+ EXPERIMENTAL feature: Add HmacgImport method. Now it can read and convert xlsx file from HMacg. Currently it relies on lots of magic number to work. So take the risk if you use this feature. 

  > [!NOTE]
  >
  > EXPERIMENTAL flag is requied.
  >
  > Install requiements for xlsx processing is required (See requirements.txt)

- Fix some conflicts when updating a outdated DownloadItem.

##### While, there are still some functions not available yet:

+ User management.
+ No elegant user interface.

Due to my lack of building beautiful front-end pages and some personal issues, this project won't get a frequent update as long as the basic functions working well. The version won't pass 1.0 either though it's kind of perfectly working for me.
Thanks for all your supporting! Hope there will be a chance to make a big update in the future.
