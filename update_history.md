# Update History

### Latest:0.999

WARNING: This is still a beta version. Please check the latest stable version unless you want to try and test this new version.

##### New Features:

+ Now both 'home' and 'all' lists are descending by id, which means the more recent series will show on the top.
+ Fallback the retry method to normal increasing method. the ERROR_RETRY_SPAN means the maximum span for the last try.
+ Add 'modify' & 'update' button in the detail page.
+ Now the download parts will check the existence of target folder. If it's not it will automatically be created. However you must bind the target directory to the container.
+ fix InnerIndexer failed in using item name to search results due to not parsing to url format string.
+ Modify some default value for convenience of creating new series.



##### While, there are still some functions not available yet:

+ User management.
+ No elegant user interface.

Due to my lack of building beautiful front-end pages and some personal issues, this project won't get a frequent update as long as the basic functions working well. The version won't pass 1.0 either though it's kind of perfectly working for me.
Thanks for all your supporting! Hope there will be a chance to make a big update in the future.



----------

### 0.99:

+ Rebuild all back-end parts. The new version is more powerful and stable.
+ Interface for data items and download methods. It can support any extensions developed under the new interface standard. Simply store the new $module.class$ name of extension's item/method into the downloadTable.related_table/subscriptionTable.type so that the brand new SubscribeCore will automatically find the related class and apply it.
+ Database has been redesigned for a better performance.The old database will not work on this version. For users upgraded from earlier versions, please move your data to the new database.
+ The integrated download method Jackett will check the local file existence before applying the matched results.
+ Introducing the new logging module: loguru. It provides more convenient and more delicate log management.
+ Fix the issue that the config parameters may not be updated as expected.
+ For users upgrade from earlier versions, the old config files may still available but may not correctly work on this version. For a better experience we recommand you rewrite your config to match the new format.
+ Add instant download function.

### 0.94

+ Fix the "cannot delete any item" bug.

Due to too many unpredictable issues in the current version, the next update may rebuild the whole back-end parts.



### 0.93

+ Fix some bugs on the UI pages.
+ Fix the "Subscription cannot update on time" issue



### 0.92

##### Welcome to xyseer-nas-tool/AnimeAssistant !

The AnimeAssistant is part of xy-nas-tool. The xy-nas-tool project aims at gathering useful and powerful tools so that users can get a full-automatic NAS assistant to achieve a better experience.

The AnimeAssistant focuses on automatically subscribing anime series. Users can get the latest anime just like what they do on the video sharing platforms. 

The AnimeAssistant is coding by Python, using Flask flamework to provide an interface for interaction. Docker image are also made for deploying this service into your NAS.

Currently, on version 0.92, AnimeAssistant has following functions:

+ Manually add/delete/modify a Series for subscription.
+ Download the latest episode of a subscription on time.
+ A simple web interface to manage this service

