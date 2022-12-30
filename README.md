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



### Latest:0.99_beta_01

WARNING: This is still a beta version. Please check the latest stable version unless you want to try and test this new version.

##### New Features:

+ Rebuild all back-end parts. The new version is more powerful and stable.
+ Interface for data items and download methods. It can support any extensions developed under the new interface standard. Simply store the new $module.class$ name of extension's item/method into the downloadTable.related_table/subscriptionTable.type so that the brand new SubscribeCore will automatically find the related class and apply it.
+ Database has been redesigned for a better performance.The old database will not work on this version. For users upgraded from earlier versions, please move your data to the new database.
+ The integrated download method Jackett will check the local file existence before applying the matched results.
+ Introducing the new logging module: loguru. It provides more convenient and more delicate log management.
+ Fix the issue that the config parameters may not be updated as expected.
+ For users upgrade from earlier versions, the old config files may still available but may not correctly work on this version. For a better experience we recommand you rewrite your config to match the new format.

##### While, there are still some functions not available yet:

+ User management.
+ No elegant user interface.

The next formal version may focus on dealing with these two issues.