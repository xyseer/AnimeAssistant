# 更新日志

### 最新版本：0.9b

注意：这是一个测试版本。除非您想测试或体验该新版本，请您选择使用最新的稳定版本。

##### 新特性：

+ 为一些没那么稳定的功能增加了 EXPERIMENTAL 开关，想使用高级功能的用户可以通过`/experimental` 打开这个开关，并且它会展示您当前的 EXPERIMENTAL 开关状态

+ 增加新功能：用json导出您的订阅（包含封面图片的base64数据）

+ 实验特性：添加导入功能。这允许用户从其他人分享的json文本导入订阅

  > [!NOTE]
  >
  > 需要 EXPERIMENTAL 开关开启.

+ 实验特性：添加H萌导入方式。现在它可以读取并转换H萌 xlsx格式的新番表。当前它依赖于一些魔法数字工作，请自行承担风险。

  > [!NOTE]
  >
  > 需要 EXPERIMENTAL 开关开启.
  >
  > 需要额外安装处理xlsx的依赖。（具体查看requirements.txt）

- 修复了更新过时的DownloadItem时产生的冲突

##### 现在还有一些功能不可用：

+ 用户管理
+ 没有精致的用户界面

下个正式版本会主要解决这两个问题。

### 0.9a

- 迁移到了新的订阅方式。由于apscheduler可靠，新方式不再每隔一段时间检查所有更新，这减少了开销并提升了性能
- 修复了日志保留问题，loguru自带保留功能不生效的原因仍不可知，但这里提供了一个新实现，它会和`remap_scheduler`一起运行，并保留REGULAR_CHECK_SPAN数量的日志
- 提供了arm64架构的docker镜像

通过这些更改，我们建议您将REGULAR_CHECK_SPAN 修改为一个大于7（天）的整数以获取更好体验

-------

### 0.99e

- 紧急修复：修复了建立新剧集时建立新文件夹时出现的权限错误，这之前会导致无法建立或更改剧集（感谢pathlib库没有指出这个问题，以及感谢其实现os库明确的指出了这个问题）
- 修复了新建剧集时无法递归创建上级文件夹

-----------

### 0.999

+ 现在'主页'和'在追番剧'都按照id倒序展示,这意味着时间越近的剧集会展示在前面
+ 重试策略回退成正常的增长方式,ERROR_RETRY_SPAN现在指最后一次最大的重试时间
+ 在详情界面增加'修改'和'立即更新'按钮
+ 现在下载会检测目标目录是否存在,如果不存在会自动创建.这需要您将目标目录映射到容器中
+ 修复了InnerIndexer使用名称搜索时没有正确转译成url字符串的问题
+ 修改了一些默认值为了更方便的创建剧集

---------------

### 0.99：

+ 重建了后端部分。新版本更加强大和稳定。
+ 增加了DataItems和Download methods的接口。现在可以支持任何使用该接口标准的插件。只需简单的将插件的item/method的 $模块.名称$ 存储至downloadTable.related_table/subscriptionTable.type，新的SubscribeCore会自动查找相对应的类并使用它。
+ 为了更好的性能，数据库被重新设计。旧版本的数据库不能在该版本正常工作。对于从旧版本升级的用户，请将您的数据移至新的数据库。
+ 内置的下载方法Jackett现在会在下载匹配的结果之前检查本地文件是否存在。
+ 引入新的日志模块loguru。它可以提供更加便利和更加精妙的日志管理方法。
+ 解决了“配置数据可能不能按照预期更新”的问题
+ 对于从旧版本升级的用户，在该版本下，旧的配置文件仍然可以使用，但可能不会正确的工作。为了更好的使用体验，我们建议您重写您的配置文件来匹配新的格式。
+ 添加了立即更新功能

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