# 更新日志

### 最新版本：0.99_beta_01

注意：这是一个测试版本。除非您想测试或体验该新版本，请您选择使用最新的稳定版本。

##### 新特性：

+ 重建了后端部分。新版本更加强大和稳定。
+ 增加了DataItems和Download methods的接口。现在可以支持任何使用该接口标准的插件。只需简单的将插件的item/method的 $模块.名称$ 存储至downloadTable.related_table/subscriptionTable.type，新的SubscribeCore会自动查找相对应的类并使用它。
+ 为了更好的性能，数据库被重新设计。旧版本的数据库不能在该版本正常工作。对于从旧版本升级的用户，请将您的数据移至新的数据库。
+ 内置的下载方法Jackett现在会在下载匹配的结果之前检查本地文件是否存在。
+ 引入新的日志模块loguru。它可以提供更加便利和更加精妙的日志管理方法。
+ 解决了“配置数据可能不能按照预期更新”的问题
+ 对于从旧版本升级的用户，在该版本下，旧的配置文件仍然可以使用，但可能不会正确的工作。为了更好的使用体验，我们建议您重写您的配置文件来匹配新的格式。

##### 现在还有一些功能不可用：

+ 用户管理
+ 没有精致的用户界面

下个正式版本会主要解决这两个问题。



---------------

### 0.94

+ 解决了“不能删除任何项目”的错误。

因为目前版本有太多不能预测的问题，下一次更新可能考虑重建整个后端部分。



### 0.93

+ 解决了一些用户界面上的错误。
+ 解决了“订阅不能准时更新”的问题。



### 0.92

##### 欢迎来到xyseer-nas-tool/AnimeAssistant !

AnimeAssistant是xy-nas-tool的一部分。xy-nas-tool项目旨在收集好用且强大的工具，使得用户可以得到一个全自动NAS助手进而得到更好的体验。

AnimeAssistant着重于自动订阅番剧。用户可以像他们从视频平台上一样获取最新番剧。

AnimeAssistant是由Python编写，使用Flask框架提供交互界面。我们也制作了Docker镜像用于部署至您的NAS上。

目前，在0.92版本，AnimeAssistant有以下功能：

+ 手动添加/删除/更改需要订阅的剧集。
+ 按时下载订阅中最新的剧集。
+ 一个简易的界面用于管理整个服务。