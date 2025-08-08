# Update History

### Latest:0.9c

WARNING: This is still a beta version. Please check the latest stable version unless you want to try and test this new version.

##### What's new:

+ Fix the delay deletion problem in the new subscription handler method.
+ Move default source links to DEFAULT_SOURCE in settings.
+ Support more feeds in InnerIndexer.


##### While, there are still some functions not available yet:

+ User management.
+ No elegant user interface.

Due to my lack of building beautiful front-end pages and some personal issues, this project won't get a frequent update as long as the basic functions working well. The version won't pass 1.0 either though it's kind of perfectly working for me.
Thanks for all your supporting! Hope there will be a chance to make a big update in the future.

### 0.9b

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

-------

### 0.9a

- Migrate to a new subscription handler method. As apscheduler is reliable, the new method won't need to check everything in a regular span, which reduced the cost and improved performance.
- Fixed log retention issue. The reason why loguru retention is not working remains unknown. However, there is a new log retention method implementation, which will run with `remap_scheduler` and leave REGULAR_CHECK_SPAN amount of logs.
- Provide arm64 build for docker images.

With these changes, we strongly recommend you change the REGULAR_CHECK_SPAN into a integer greater than 7 (days) for a better experience.

-------

### 0.99e

+ Emerge fix: Fixed incorrect permission when creating new series, which previously leaded to failure when creating or editing new series. (Thanks for pathlib for not pointing out the issue in their document and thanks for the implentation used by path lib, os, pointing out this feature in their documents clearly.)
+ Fixed not creating directories recursively when creating new series.

----------------------

### 0.999

+ Now both 'home' and 'all' lists are descending by id, which means the more recent series will show on the top.
+ Fallback the retry method to normal increasing method. the ERROR_RETRY_SPAN means the maximum span for the last try.
+ Add 'modify' & 'update' button in the detail page.
+ Now the download parts will check the existence of target folder. If it's not it will automatically be created. However you must bind the target directory to the container.
+ fix InnerIndexer failed in using item name to search results due to not parsing to url format string.
+ Modify some default value for convenience of creating new series.

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

