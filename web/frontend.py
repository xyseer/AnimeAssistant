# -*- coding:utf-8 -*-
# This is a compromised method to present frontend because at that time the developer
# had little knowledge on frontend. Never try to deliver your app like this.
# I'm begging you never try like this!!


import importlib
import multiprocessing
import json
import os
from random import sample

import flask
from flask import Flask, request, render_template, redirect

from SubscribeCore import SubscribeCore
from parameters import Parameters
from multiprocessing import Pool
from GLOBAL_DEFINE import *
from web.response_funcs import *

app = Flask(__name__, static_folder=STATIC_DIR)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['MAX_FORM_PARTS'] = 50 * 1024 * 1024
app.config['MAX_FORM_MEMORY_SIZE'] = 50 * 1024 * 1024
ss = None


@app.route("/user", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['password']
        response_dict = {"status": 200, "auth": f"xy-nas-tool {VERSION_INFO}",
                         "session": login_by_passwd(username, passwd)}
        return json.dumps(response_dict, ensure_ascii=False)
    else:
        return json.dumps({"status": 404, "auth": f"xy-nas-tool {VERSION_INFO}"}, ensure_ascii=False)


@app.route("/experimental")
def experimental_flag():
    global EXPERIMENTAL
    EXPERIMENTAL = not EXPERIMENTAL
    return str(EXPERIMENTAL)


@app.route("/")
def homepage():
    html = '''<!DOCTYPE html >
<html >
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>xy-nas-tools</title>
<link href="static/css.css" rel="stylesheet" type="text/css" />
<style type="text/css">

</style>
</head>

<body>
<div class="box">
<table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
    <td><h1>xy-nas-tool</h1></td>
    <td width="100" align="center"><a href="./">主页</a></td>
    <td width="100" align="center"><a href="./all">在追番剧</a></td>
    <td width="100" align="center"><a href="./setting">设置</a></td>
    <td width="100" align="center"><a href="./log">查看日志</a></td>
    <td width="100" align="center"><a href="./about">关于</a></td>
  </tr>
</table>
<table width=80% border="1" align="center" cellpadding="1" cellspacing="0" class="main">
  <th width=16%>图片</th>
  <th width=14%>名称</th>
  <th width=30%>简介</th>
  <th width=10%>下次更新时间</th>
  <th width="5%">下次更新集数</th>
  <th width=25%>操作</th>
</table>
'''
    for metadata_dict in json.loads(get_current_metadata()).get("metadata_dict_list", []):
        metadata_item = MetadataItem(-1).from_dict(metadata_dict)
        subscription_item = SubscriptionItem(metadata_item.id)
        html += f'''
                <br>
<table width=80% height="200" border="1" align="center" cellpadding="1" cellspacing="0" class="main">
  <tr>
  <td width=16%><img src="{metadata_item.img}" width=100%></td>
  <td width=14% align="center">{metadata_item.name}</td>
  <td width=30% align="center">{metadata_item.info}</td>
  <td width=10% align="center">{subscription_item.nextUpdateTime.strftime(HTML_TIME_FORMAT)}</td>
  <td width="5%" align="center">{subscription_item.nextUpdateEP}</td>
    <td width=25% align="center"><a href="detail?id={metadata_item.id}"><button class="button1">详情</button></a>
    <a href="update?id={metadata_item.id}"><button class="button2">立即更新</button></a></td>
  </tr>
</table>
            '''
        continue
    html += f'''
  <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
    <td align=center><h4>xy-nas-tool V{VERSION_INFO}.&nbsp&nbsp&nbsp&nbsp&nbsp made by xyseer.</h4></td>
  </tr>
</table>
              </div>
</body>
</html>
        '''
    return html


@app.route('/all')
def animelist():
    html = f'''<!DOCTYPE html >
<html >
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>xy-nas-tools</title>
<link href="static/css.css" rel="stylesheet" type="text/css" />
<style type="text/css">

</style>
</head>

<body>
<div class="box">
<table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
    <td><h1>xy-nas-tool</h1></td>
    <td width="100" align="center"><a href="./">主页</a></td>
    <td width="100" align="center"><a href="./all">在追番剧</a></td>
    <td width="100" align="center"><a href="./setting">设置</a></td>
    <td width="100" align="center"><a href="./log">查看日志</a></td>
    <td width="100" align="center"><a href="./about">关于</a></td>
  </tr>
</table>
<table width=80% border="1" align="center" cellpadding="1" cellspacing="0" class="main">
  <th width=16%>图片</th>
  <th width=14%>名称</th>
  <th width=30%>简介</th>
  <th width=10%>下次更新时间</th>
  <th width="5%">下次更新集数</th>
  <th width=25%>操作</th>
</table>
<br>
<table width=80% height="40px" align="center" cellpadding="1" cellspacing="0">
<tr><td align="center">
<a href="add"><button class="button_add">点此以新增剧集</button></a></td>
<td align="center">
<a href="import"><button class="button_add" {"hidden" if not EXPERIMENTAL else ""}>导入信息</button></a></td>
<td align="center">
<a href="once"><button class="button_add">快速下载</button></a></td>
</tr>
</table>
'''
    for metadata_dict in json.loads(get_all_metadata()).get("metadata_dict_list", []):
        metadata_item = MetadataItem(-1).from_dict(metadata_dict)
        subscription_item = SubscriptionItem(metadata_item.id)
        html += f'''
                <br>
<table width=80% height="200" border="1" align="center" cellpadding="1" cellspacing="0" class="main">
  <tr>
  <td width=16%><img src="{metadata_item.img}" width=100%></td>
  <td width=14% align="center">{metadata_item.name}</td>
  <td width=30% align="center">{metadata_item.info}</td>
  <td width=10% align="center">{subscription_item.nextUpdateTime.strftime(HTML_TIME_FORMAT)}</td>
  <td width="5%" align="center">{subscription_item.nextUpdateEP}</td>
    <td width=25% align="center"><a href="detail?id={metadata_item.id}"><button class="button1">详情</button></a>
    <a href="update?id={metadata_item.id}"><button class="button2">立即更新</button></a>
    <a href="modify?id={metadata_item.id}"><button class="button3">修改</button></a>
    </td>
  </tr>
</table>
            '''
        continue
    html += f'''
  <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
    <td align=center><h4>xy-nas-tool V{VERSION_INFO}.&nbsp&nbsp&nbsp&nbsp&nbsp made by xyseer.</h4></td>
  </tr>
</table>
              </div>
</body>
</html>
        '''
    return html


@app.route('/detail', methods=['GET'])
def detail():
    id = int(request.args.get("id", "-1"))
    if id < 0 or id >= getValidID():
        return "Error: no such id was found."
    s = SubscriptionItem(id)
    ss = DBManipulator()
    d = ss.get_cursor().execute("SELECT * from downloadTable where id=?", (id,)).fetchone()
    del ss
    m = MetadataItem(id)
    html = f'''
    <!DOCTYPE html >
<html >
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>xy-nas-tools</title>
<link href="static/css.css" rel="stylesheet" type="text/css" />
<style type="text/css">

</style>
</head>

<body>
<div class="box">
<table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
    <td><h1>xy-nas-tool</h1></td>
    <td width="100" align="center"><a href="./">主页</a></td>
    <td width="100" align="center"><a href="./all">在追番剧</a></td>
    <td width="100" align="center"><a href="./setting">设置</a></td>
    <td width="100" align="center"><a href="./log">查看日志</a></td>
    <td width="100" align="center"><a href="./about">关于</a></td>
  </tr>
</table>
<table width=80% border="1" align="center" cellpadding="1" cellspacing="0" class="main">
  <tr>
    <td rowspan="2" width=20% align="center"><img src="{m.img}" height="300" width=100%></td>
    <td colspan="3" width="80%" height=50 align="center">{m.name}</td>
  </tr>
  <tr>
    <td colspan="3" height="60%" align="center">{m.info}</td>
  </tr>
</table>
<table width=80% height="300" border="1" align="center" cellpadding="1" cellspacing="0" class="main">
  <tr>
    <td width="25%" align="center">开播时间</td>
    <td width="25%" align="center">{s.starttime.strftime(UNIFIED_TIME_FORMAT)}</td>
    <td width="25%" align="center">总集数</td>
    <td width="25%" align="center">{s.totalEpisodes}</td>
  </tr>
  <tr>
    <td width="25%" align="center">上次更新时间</td>
    <td width="25%" align="center">{s.lastUpdateTime.strftime(UNIFIED_TIME_FORMAT)}</td>
    <td width="25%" align="center">上次更新集数</td>
    <td width="25%" align="center">{s.lastUpdateEP}</td>
  </tr>
  <tr>
    <td width="25%" align="center">下次更新时间</td>
    <td width="25%" align="center">{s.nextUpdateTime.strftime(UNIFIED_TIME_FORMAT)}</td>
    <td width="25%" align="center">下次更新集数</td>
    <td width="25%" align="center">{s.nextUpdateEP}</td>
  </tr>
  <tr>
    <td width="25%" align="center">更新间隔</td>
    <td width="25%" align="center">{s.span} h</td>
    <td width="25%" align="center">更新方式</td>
    <td width="25%" align="center">{s.type}</td>
  </tr>
</table>
  <table width=80% height="200" border="1" align="center" cellpadding="1" cellspacing="0" class="main">
    <tr>
    <td width="50%" align="center">下载来源</td>
    <td width="50%" align="center">{d[1]}</td>
  </tr>
    <tr>
    <td width="50%" align="center">下载目录</td>
    <td width="50%" align="center">{d[2]}</td>
  </tr>
    </tr>
    <tr>
    <td width="50%" align="center">过滤条件</td>
    <td width="50%" align="center">{listTostr(strTolist(d[3]))}</td>
  </tr>
  </table>

  <table width="100%" height="80" border="0" cellpadding="0" cellspacing="0" class="buttons">
  <tr>
    <td  align="right">
      <button class="button2" onclick="javascript :history.back(-1);">返回</button>
      <a href="update?id={m.id}"><button class="button1">立即更新</button></a>
      <a href="export?id={m.id}"><button class="button2">导出</button></a>
      <a href="modify?id={m.id}"><button class="button3">修改</button></a>
    </td>
  </tr>
</table>

  <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
    <td align=center><h4>xy-nas-tool V{VERSION_INFO}.&nbsp&nbsp&nbsp&nbsp&nbsp made by xyseer.</h4></td>
  </tr>
</table>

  </div>
</body>
</html>



    '''
    return html


@app.route("/update", methods=["GET"])
def update_imm():
    try:
        if int(request.args.get("id", "-1")) > 0:
            subscribe_immediately(int(request.args.get("id", "-1")), ss)
    except Exception as e:
        return f'''<script type="text/javascript">
                    alert("Error when update:{str(e)}");history.back(-1);</script>'''
    finally:
        return f'''<script type="text/javascript">history.back(-1);</script>'''


@app.route("/add")
def add_item():
    try:
        return_list = get_new_subscription_item()
        if not None:
            return redirect(f"modify?id={return_list[0].id}")
        else:
            f'''<script type="text/javascript">
                                alert("Error when update:{"No Valid ID was given."}");history.back(-1);</script>'''
    except Exception as e:
        return f'''<script type="text/javascript">
                    alert("Error when update:{str(e)}");history.back(-1);</script>'''


@app.route("/delete", methods=["GET"])
def del_item():
    try:
        if int(request.args.get("id", "-1")) > 0:
            table_id = int(request.args.get("id", "0"))
            if delete_item(table_id):
                return redirect(f"all")
            else:
                return f'''<script type="text/javascript">
                                    alert("删除失败.");{f'location.replace("/all")'};</script>'''
        return redirect(f"all")
    except Exception as e:
        return f'''<script type="text/javascript">
                    alert("Error when update:{str(e)}");history.back(-1);</script>'''


@app.route("/modify", methods=["GET"])
def modify():
    try:
        id = int(request.args["id"])
        if 0 < id < getValidID():
            s = SubscriptionItem(id)
            ss = DBManipulator()
            d = ss.get_cursor().execute("SELECT * from downloadTable where id=?", (id,)).fetchone()
            del ss
            m = MetadataItem(id)
        else:
            return ""
    except Exception as e:
        return str(e)

    html = f'''
        <!DOCTYPE html >
<html >
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>xy-nas-tools</title>
<link href="static/css.css" rel="stylesheet" type="text/css" />
<style type="text/css">

</style>
</head>

<body>
<div class="box">

<table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
    <td><h1>xy-nas-tool</h1></td>
    <td width="100" align="center"><a href="./">主页</a></td>
    <td width="100" align="center"><a href="./all">在追番剧</a></td>
    <td width="100" align="center"><a href="./setting">设置</a></td>
    <td width="100" align="center"><a href="./log">查看日志</a></td>
    <td width="100" align="center"><a href="./about">关于</a></td>
  </tr>
</table>
   <form action="/submit" method="post" enctype="multipart/form-data">
<table width=80% border="1" align="center" cellpadding="1" cellspacing="0" class="main">
  <tr>
    <td rowspan="2" width=20% align="center"><img src="{m.img}" id="image-preview" height="300" width=100%>
	<input type="file" id="file" name="img" accept="image/jpeg, image/png, image/jpg">
      <script type="text/javascript">
      ''' + '''
			let fileInput = document.getElementById('file');
			let preview = document.getElementById('image-preview');
			// 监听change事件:
			fileInput.addEventListener('change', function() {
				// 清除背景图片:
				preview.style.backgroundImage = '';
				let file = fileInput.files[0];
				if (!['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)) {
					alert('不是有效的图片文件!');
					return;
				}
				// 读取文件:
				let reader = new FileReader();
				reader.onload = function(e) {
					let data = e.target.result;
					preview.src = data
				};
				// 以DataURL的形式读取文件:
				reader.readAsDataURL(file);

			});
</script>
''' + f'''
</td>
    <td colspan="3" width="80%" height=50 align="center"><input type="text" value="{m.name}" class="text1" name="name"></td>
  </tr>
  <tr>
    <td colspan="3" height="60%" align="center"><textarea class="text1" name="meta">{m.info}</textarea></td>
  </tr>
</table>
<table width=80% height="300" border="1" align="center" cellpadding="1" cellspacing="0" class="main">
  <tr>
    <td width="25%" align="center">开播时间</td>
    <td width="25%" align="center"><input align="center" type="datetime-local" value="{s.starttime.strftime(HTML_INPUT_TIME_FORMAT)}" class="text1" name="starttime"></td>
    <td width="25%" align="center">总集数</td>
    <td width="25%" align="center"><input type="number" value="{s.totalEpisodes}" class="text1" name="totaleps"></td>
  </tr>
  <tr>
    <td width="25%" align="center">上次更新时间</td>
    <td width="25%" align="center"><input align="center" type="datetime-local" value="{s.lastUpdateTime.strftime(HTML_INPUT_TIME_FORMAT)}" class="text1" name="lasttime"></td>
    <td width="25%" align="center">上次更新集数</td>
    <td width="25%" align="center"><input type="number" value="{s.lastUpdateEP}" class="text1" name="lastep"></td>
  </tr>
  <tr>
    <td width="25%" align="center">下次更新时间</td>
    <td width="25%" align="center"><input align="center" type="datetime-local" value="{s.nextUpdateTime.strftime(HTML_INPUT_TIME_FORMAT)}" class="text1" name="nexttime"></td>
    <td width="25%" align="center">下次更新集数</td>
    <td width="25%" align="center"><input type="number" value="{s.nextUpdateEP}" class="text1" name="nextep"></td>
  </tr>
  <tr>
    <td width="25%" align="center">更新间隔</td>
    <td width="25%" align="center"><input type="number" width=80% value="{s.span}" class="span" name="span"> <label>小时</label></td>
    <td width="25%" align="center">更新方式</td>
    <td width="25%" align="center">
      <input type="text" width=80% value="{s.type}" class="text1" name="way">
    </td>
  </tr>
</table>
  <table width=80% height="200" border="1" align="center" cellpadding="1" cellspacing="0" class="main">
    <tr>
    <td width="50%" align="center">下载来源</td>
    <td width="50%" align="center"><input type="text" value="{d[1]}" class="text1" name="source"></td>
  </tr>
    <tr>
    <td width="50%" align="center">下载目录</td>
    <td width="50%" align="center"><input type="text" value="{d[2]}" class="text1" name="directory"></td>
  </tr>
    </tr>
    <tr>
    <td width="50%" align="center">过滤条件</td>
    <td width="50%" align="center">
      <select class="text1" name="filter">'''
    html += f"<option>{listTostr(strTolist(d[3]))}</option>"
    for i in Parameters().FILTER_DICTS.keys():
        if i not in strTolist(d[3]):
            html += f"<option>{i}</option>"
    html += f'''
      </select>
    </td>
    <input type="hidden" name="id" value="{id}">
  </tr>
  </table>

  <table width="100%" height="80" border="0" cellpadding="0" cellspacing="0" class="buttons">
  <tr>
    <td  align="right">
      <button class="button2" onclick="javascript :history.back(-1);" type="button">返回</button>
      <button class="button3" onclick="confirmDialog()" type="button">删除</button>
      <button class="button1" type="submit">提交</button>
      <script type="text/javascript">''' + '''
        function confirmDialog(){
			if(confirm("确认删除吗？")){
	    		top.location="./delete?id=''' + f"{id}" + '''";
			}else{
			}
    	}
      </script>''' + f'''
    </td>
  </tr>
</table>
</form>
<table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
    <td align=center><h4>xy-nas-tool V{VERSION_INFO}.&nbsp&nbsp&nbsp&nbsp&nbsp made by xyseer.</h4></td>
  </tr>
</table>
  </div>
</body>
</html>
    '''
    return html


@app.route("/submit", methods=["POST"])
def submit():
    try:
        if request.method == 'POST':
            id = request.form.get("id", "")
            name = request.form.get("name", "")
            starttime = request.form.get("starttime", "")
            meta = request.form.get("meta", "")
            totaleps = request.form.get("totaleps", "")
            lasttime = request.form.get("lasttime", "")
            lastep = request.form.get("lastep", "")
            nexttime = request.form.get("nexttime", "")
            nextep = request.form.get("nextep", "")
            span = request.form.get("span", "")
            source = request.form.get("source", "")
            directory = request.form.get("directory", "")
            way = request.form.get("way", "")
            filter_name = request.form.get("filter", "")
            img = request.files.get("img")
            if not id:
                return '''<script type="text/javascript">
            alert("修改失败: Invalid id!");history.back(-1);</script>'''
            request_dict = {}
            request_dict["id"] = int(id) if 0 < int(id) < getValidID() else -1
            if name:
                try:
                    request_dict["name"] = name
                except Exception:
                    return '''<script type="text/javascript">
                            alert("修改失败: Process NameTable Error!");history.back(-1);</script>'''
            if meta:
                try:
                    request_dict["info"] = meta
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process MetaInfo Error!");history.back(-1);</script>'''
            if img:
                try:
                    new_path = str(
                        Path(STATIC_DIR) / (''.join(sample(string.ascii_letters + string.digits, 16)) + ".jpg"))
                    img.save(new_path)
                    request_dict["img"] = new_path
                except Exception:
                    return '''<script type="text/javascript">
                        alert("修改失败: Process MetaImage Error!");history.back(-1);</script>'''
            if starttime:
                try:
                    startTime = datetime.strptime(str(starttime), HTML_INPUT_TIME_FORMAT)
                    request_dict["starttime"] = startTime
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process StartTime Error!");history.back(-1);</script>'''
            if lasttime:
                try:
                    lastTime = datetime.strptime(str(lasttime), HTML_INPUT_TIME_FORMAT)
                    request_dict["lastUpdateTime"] = lastTime
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process LastTime Error!");history.back(-1);</script>'''
            if nexttime:
                try:
                    nextTime = datetime.strptime(str(nexttime), HTML_INPUT_TIME_FORMAT)
                    request_dict["nextUpdateTime"] = nextTime
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process NextTime Error!");history.back(-1);</script>'''
            if totaleps:
                try:
                    if int(totaleps) > 0:
                        request_dict["totalEpisodes"] = int(totaleps)
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process TotalEPs Error!");history.back(-1);</script>'''
            if lastep:
                try:
                    if int(lastep) >= 0:
                        request_dict["lastUpdateEP"] = int(lastep)
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process LastEP Error!");history.back(-1);</script>'''
            if nextep:
                try:
                    if int(nextep) >= 0:
                        request_dict["nextUpdateEP"] = int(nextep)
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process NextEP Error!");history.back(-1);</script>'''
            if span:
                try:
                    if int(span) > 0:
                        request_dict["span"] = int(span)
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process Span Error!");history.back(-1);</script>'''
            if source:
                try:
                    request_dict["source"] = str(source)
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process Source Error!");history.back(-1);</script>'''
            if directory:
                try:
                    request_dict["directory"] = str(directory)
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process Directory Error!");history.back(-1);</script>'''
            if way:
                try:
                    request_dict["type"] = str(way)
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process DownloadWay Error!");history.back(-1);</script>'''
            if filter_name:
                try:
                    request_dict["filter_name"] = strTolist(str(filter_name), ",")
                except Exception:
                    return '''<script type="text/javascript">
                                                alert("修改失败: Process Filter Error!");history.back(-1);</script>'''
            try:
                modify_item(request_dict, ss)
            except Exception:
                return '''<script type="text/javascript">
                                                                alert("修改失败: Process Filter Error!");history.back(-1);</script>'''
    except Exception as e:
        return f'''<script type="text/javascript">
                                                alert("修改失败: Unexpected Error! {str(e)}");history.back(-1);</script>'''
    finally:
        return redirect(f"detail?id={id}")


@app.route("/log")
def watch_log():
    log = ""
    name = ""
    p = Parameters()
    with open(p.LOG_DIR + "/" + os.listdir(p.LOG_DIR)[-1], "r") as fp:
        name += os.listdir(p.LOG_DIR)[-1]
        log += fp.read()
    return f'''
    <!DOCTYPE html >
<html >
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>xy-nas-tools</title>
<link href="/static/css.css" rel="stylesheet" type="text/css" />
<style type="text/css">

</style>
</head>

<body>
<div class="box">
<table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
        <td><h1>xy-nas-tool</h1></td>
        <td width="100" align="center"><a href="./">主页</a></td>
        <td width="100" align="center"><a href="./all">在追番剧</a></td>
        <td width="100" align="center"><a href="./setting">设置</a></td>
        <td width="100" align="center"><a href="./log">查看日志</a></td>
        <td width="100" align="center"><a href="./about">关于</a></td>
      </tr>
</table>
  <table width=80% height="85%" border="0" align="center" class="main">
  <tr><th height="20px" align="center">{name}</th></tr>
    <tr>
      <td align="center"><textarea class="log1" readonly="readonly">{log}</textarea>

      </td>
    </tr>

  </table>
  <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
    <td align=center><h4>xy-nas-tool V{VERSION_INFO}.&nbsp&nbsp&nbsp&nbsp&nbsp made by xyseer.</h4></td>
  </tr>
</table>
  </div>
</body>
</html>
'''


@app.route("/setting", methods=["GET", "POST"])
def setting():
    if request.method == "POST":
        try:
            p = Parameters()
            p.DB_PATH = request.form.get("DB_PATH", p.DB_PATH)
            p.ARIA2_RPC_SERVER = request.form.get("ARIA2_RPC_SERVER", p.ARIA2_RPC_SERVER)
            p.ARIA2_JSONRPC_TOKEN = request.form.get("ARIA2_JSONRPC_TOKEN", p.ARIA2_JSONRPC_TOKEN)
            p.REGULAR_CHECK_SPAN = request.form.get("REGULAR_CHECK_SPAN", p.REGULAR_CHECK_SPAN)
            p.LOG_DIR = request.form.get("LOG_DIR", p.LOG_DIR)
            p.ERROR_RETRY_SPAN = request.form.get("ERROR_RETRY_SPAN", p.ERROR_RETRY_SPAN)
            if request.form.get("JACKETT_API_LINK_LIST", ""):
                tmp = request.form.get("JACKETT_API_LINK_LIST", "").split("\n")
                result_tmp = []
                for i in tmp:
                    i = i.replace("\n", "").replace("\r", "").replace("\r", "").replace("\r", "")
                    if i:
                        result_tmp.append(i)
                p.JACKETT_API_LINK_LIST = result_tmp
            if request.form.get("filter_name", ""):
                if request.form.get("filter_name", "") not in p.FILTER_DICTS.keys():
                    p.FILTER_DICTS[request.form.get("filter_name", "")] = {"reject_rules": [], "apply_rules": []}
            if request.form.get("filter_exclude", ""):
                tmp = request.form.get("filter_exclude", "").split(";")
                for i in tmp:
                    i.replace(";", "")
                    if not i:
                        tmp.remove("")
                if request.form.get("filter_name", ""):
                    p.FILTER_DICTS[str(request.form.get("filter_name", ""))]["reject_rules"] = tmp
            if request.form.get("filter_include", ""):
                tmp = request.form.get("filter_include", "").split(";")
                for i in tmp:
                    i.replace(";", "")
                    if not i:
                        tmp.remove("")
                if request.form.get("filter_name", ""):
                    p.FILTER_DICTS[str(request.form.get("filter_name", ""))]["apply_rules"] = tmp
            p.push()
            return f'''<script type="text/javascript">
                       alert("设置成功!");history.back(-1);</script>'''
        except Exception as e:
            return f'''<script type="text/javascript">
                        alert("修改失败: Unexpected Error! {str(e)}");history.back(-1);</script>'''
    else:
        p = Parameters()
        html = f'''
            <!DOCTYPE html >
    <html >
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>xy-nas-tools</title>
    <link href="static/css.css" rel="stylesheet" type="text/css" />
    <style type="text/css">
    
    </style>
    </head>
    
    <body>
    <div class="box">
    
    <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
      <tr>
        <td><h1>xy-nas-tool</h1></td>
        <td width="100" align="center"><a href="./">主页</a></td>
        <td width="100" align="center"><a href="./all">在追番剧</a></td>
        <td width="100" align="center"><a href="./setting">设置</a></td>
        <td width="100" align="center"><a href="./log">查看日志</a></td>
        <td width="100" align="center"><a href="./about">关于</a></td>
      </tr>
    </table>
       <form action="/setting" method="post">
      <table width=80%  border="1" align="center" cellpadding="1" cellspacing="0" class="main">
        <tr height="60px">
        <td width="50%" align="center">DB_PATH</td>
        <td width="50%" align="center"><input type="text" value="{p.DB_PATH}" class="text1" name="DB_PATH"></td>
      </tr>
      <tr height="60px">
        <td width="50%" align="center">ARIA2_RPC_SERVER</td>
        <td width="50%" align="center"><input type="text" value="{p.ARIA2_RPC_SERVER}" class="text1" name="ARIA2_RPC_SERVER"></td>
      </tr>
        <tr height="60px">
        <td width="50%" align="center">ARIA2_JSONRPC_TOKEN</td>
        <td width="50%" align="center"><input type="text" value="{p.ARIA2_JSONRPC_TOKEN}" class="text1" name="ARIA2_JSONRPC_TOKEN"></td>
      </tr>
        <tr height="60px">
        <td width="50%" align="center">REGULAR_CHECK_SPAN</td>
        <td width="50%" align="center"><input type="number" value="{p.REGULAR_CHECK_SPAN}" class="text1" name="REGULAR_CHECK_SPAN">days</td>
      </tr>
        <tr height="60px">
        <td width="50%" align="center">LOG_DIR</td>
        <td width="50%" align="center"><input type="text" value="{p.LOG_DIR}" class="text1" name="LOG_DIR"></td>
      </tr>
        <tr height="150px">
        <td width="50%" align="center">JACKETT_API_LINK_LIST</td><td width="50%" align="center"><textarea class="textarea1" name="JACKETT_API_LINK_LIST">'''
    for i in p.JACKETT_API_LINK_LIST:
        html += i + "&#10&#10"
    html += f'''</textarea></td></tr>
        <tr height="60px">
        <td width="50%" align="center">ERROR_RETRY_SPAN</td>
        <td width="50%" align="center"><input type="number" value="{p.ERROR_RETRY_SPAN}" class="text1" name="ERROR_RETRY_SPAN">hrs</td>
      </tr>
      </table>
         <table width=80%  border="1" align="center" cellpadding="1" cellspacing="0" class="main">
        <tr height="60px">
        <td colspan="2" align="center">过滤条件</td></tr>
        <tr height="60px"><td width="50%" align="center">选择</td>
        <td width="50%" align="center">
          <select class="text1" onchange="filter_select_changed();" id="filter_name">'''
    for i in p.FILTER_DICTS.keys():
        html += f"<option>{i}</option>"
    html += '''
            <option>新建...</option>
          </select>
          <script>'''
    html += "var filter_name_list={};"
    for i in p.FILTER_DICTS.keys():
        html += f'''filter_name_list["{i}"]={json.dumps(p.FILTER_DICTS.get(i), ensure_ascii=False)};'''
    html += '''
            function filter_select_changed(){
                var source = document.getElementById("filter_name");
                var name = document.getElementById("filter_name_edited");
                var exclude = document.getElementById("filter_exclude");
                var include = document.getElementById("filter_include");
                var display_name = source.options[source.selectedIndex].value
                if (display_name=="新建..."){
                name.setAttribute("value","");
                exclude.setAttribute("value","");
                include.setAttribute("value","");}
                else{
                name.setAttribute("value",display_name);
                var exclude_result=new String(filter_name_list[source.options[source.selectedIndex].value]["reject_rules"])
                var include_result=new String(filter_name_list[source.options[source.selectedIndex].value]["apply_rules"])
                exclude.setAttribute("value",exclude_result.replaceAll(",",";"));
                include.setAttribute("value",include_result.replaceAll(",",";"));}
    
    
            }
          </script>
        </td>
      </tr>
           <tr height="60px">
        <td width="50%" align="center">规则名称</td>
        <td width="50%" align="center"><input type="text" value="default" class="text1" name="filter_name" id="filter_name_edited"></td>
      </tr>
        <tr height="60px">
        <td width="50%" align="center">排除规则(正则,用;分隔)</td>
        <td width="50%" align="center"><input type="text" value="" class="text1" name="filter_exclude" id="filter_exclude"></td>
      </tr>
           <tr height="60px">
        <td width="50%" align="center">包含规则(正则,用;分隔)</td>
        <td width="50%" align="center"><input type="text" value="" class="text1" name="filter_include" id="filter_include"></td>
      </tr>
      </table>
    
      <table width="100%" height="80" border="0" cellpadding="0" cellspacing="0" class="buttons">
      <tr>
        <td  align="right">
          <button class="button2" onclick="javascript :history.back(-1);">返回</button>
          <button class="button1" type="submit">提交</button>
        </td>
      </tr>
    </table>'''
    html += f'''
      <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
      <tr>
        <td align=center><h4>xy-nas-tool V{VERSION_INFO}.&nbsp&nbsp&nbsp&nbsp&nbsp made by xyseer.</h4></td>
      </tr>
    </table>
    </form>
      </div>
    </body>
    </html>
        '''
    return html


@app.route("/about")
def about():
    return f'''<!DOCTYPE html >
<html >
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>xy-nas-tools</title>
<link href="/static/css.css" rel="stylesheet" type="text/css" />
<style type="text/css">

</style>
</head>

<body>
<div class="box">
<table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
        <td><h1>xy-nas-tool</h1></td>
        <td width="100" align="center"><a href="./">主页</a></td>
        <td width="100" align="center"><a href="./all">在追番剧</a></td>
        <td width="100" align="center"><a href="./setting">设置</a></td>
        <td width="100" align="center"><a href="./log">查看日志</a></td>
        <td width="100" align="center"><a href="./about">关于</a></td>
      </tr>
</table>
<table width=80% border="1" height="85%" align="center" cellpadding="1" cellspacing="0" class="main">
  <tr height=300px><td><textarea class="about" readonly="readonly" text-align="center">&#10&#10Thanks for using xy-nas-tool!&#10 xy-nas-tool  made by xy.&#10Github  @xyseer&#10Docker  @xyseer &#10 If you have problem while using this, please let me know on the Github Project.&#10 Enjoy & have fun!{"" if not DEBUG_MODE else ss.scheduler.get_jobs()}</textarea></td></tr>
  <tr height="80%"><td width="80%"><video width="100%" align="center" src="/static/about.mp4" autoplay="autoplay" controls="controls"></video></td></tr>

</table>
    <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
  <tr>
    <td align=center><h4>xy-nas-tool V{VERSION_INFO if not DEBUG_MODE else VERSION_INFO + "_Debugging"}.&nbsp&nbsp&nbsp&nbsp&nbsp made by xyseer.</h4></td>
  </tr>
</table>
  </div>
</body>
</html>


'''


@app.route("/once/download", methods=["POST"])
def download_for_once():
    if request.method == "POST":
        type = request.form.get("type", "Aria2")
        source = request.form.get("source", "")
        directory = request.form.get("directory", "/volume1/Download")
        filter_name = request.form.get("filter", "")
        if download_once(
                DownloadItem(-1, "instant", type=type, source=source, directory=directory, filter_name=filter_name)):
            return '''<script type="text/javascript">
                        alert("Successfully handled downloads!");document.location.href = '/all';</script>'''
        else:
            return '''<script type="text/javascript">
                                                alert("Failed!");history.back(-1);</script>'''
    else:
        return '''<script type="text/javascript">
                        alert("Illegal access!");document.location.href = '/all';</script>'''


@app.route("/once")
def once():
    html = '''<!DOCTYPE html >
<html >
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>xy-nas-tools</title>
    <link href="../static/css.css" rel="stylesheet" type="text/css" />
    <style type="text/css">

    </style>
</head>

<body>
<div class="box">

    <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
        <tr>
            <td><h1>xy-nas-tool</h1></td>
            <td width="100" align="center"><a href="./">主页</a></td>
            <td width="100" align="center"><a href="./all">在追番剧</a></td>
            <td width="100" align="center"><a href="./setting">设置</a></td>
            <td width="100" align="center"><a href="./log">查看日志</a></td>
            <td width="100" align="center"><a href="./about">关于</a></td>
        </tr>
    </table>
    <form action="/once/download" method="post" enctype="multipart/form-data">
        <table width=80% border="1" align="center" cellpadding="1" cellspacing="0" class="main">
            <tr>
                <td colspan="3" width="80%" height=50 align="center"><input type="text" value="instant download" class="text1" name="name"></td>
            </tr>
        </table>
        <table width=80% height="200" border="1" align="center" cellpadding="1" cellspacing="0" class="main">
            <tr>
                <td width="25%" align="center">更新方式</td>
                <td width="25%" align="center">
                    <input type="text" width=80% value="Aria2" class="text1" name="type">
                </td>
            </tr>
            <tr>
                <td width="50%" align="center">下载来源</td>
                <td width="50%" align="center"><input type="text" value="" class="text1" name="source"></td>
            </tr>
            <tr>
                <td width="50%" align="center">下载目录</td>
                <td width="50%" align="center"><input type="text" value="/volume1/Download" class="text1" name="directory"></td>
            </tr>
            </tr>
            <tr>
                <td width="50%" align="center">过滤条件</td>
                <td width="50%" align="center">
                    <select class="text1" name="filter">'''
    for i in Parameters().FILTER_DICTS.keys():
        html += f"<option>{i}</option>"
    html += f'''
                    </select>
                </td>
                <input type="hidden" name="id" value="-1">
            </tr>

        </table>

        <table width="100%" height="80" border="0" cellpadding="0" cellspacing="0" class="buttons">
            <tr>
                <td  align="right">
                    <button class="button2" onclick="javascript :history.back(-1);" type="button">返回</button>
                    <button class="button1" type="submit">提交</button>
                </td>
            </tr>
        </table>

        <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
            <tr>
                <td align=center><h4>xy-nas-tool V{VERSION_INFO}.&nbsp&nbsp&nbsp&nbsp&nbsp made by xyseer.</h4></td>
            </tr>
        </table>
    </form>
</div>
</body>
</html>'''
    return html


@app.route("/export")
def export():
    try:
        if int(request.args.get("id", "-1")) > 0:
            table_id = int(request.args.get("id", "0"))
            result_dict = SubscriptionItem(table_id).get_dict()
            m = MetadataItem(table_id)
            result_dict["info"] = m.info
            result_dict["anidb_id"] = m.animedb_id
            result_dict["img_base64"] = file_to_base64(m.img)

            html = f'''<!DOCTYPE html >
                <html >
                <head>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                    <title>xy-nas-tools</title>
                    <link href="../static/css.css" rel="stylesheet" type="text/css" />
                    <style type="text/css">

                    </style>
                </head>

                <body>
                <div class="box">

                    <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
                        <tr>
                            <td><h1>xy-nas-tool</h1></td>
                            <td width="100" align="center"><a href="./">Home</a></td>
                            <td width="100" align="center"><a href="./all">Watching</a></td>
                            <td width="100" align="center"><a href="./setting">Setting</a></td>
                            <td width="100" align="center"><a href="./log">Log</a></td>
                            <td width="100" align="center"><a href="./about">About</a></td>
                        </tr>
                    </table>
                    <table width="50%" border="0" cellpadding="0" cellspacing="0" style="
                              position: relative;
                              top: 13vh;
                              left: 50%;
                              transform: translate(-50%, -50%);
                            ">
                        <tr><td colspan="1" height="50" align="left"><h2>Export Result:</h2></td></tr>
                        <tr>
                          <td colspan="10" height="150vh" align="center">
                            <label>
                              <textarea width:100% height:100vh class="text1" name="meta">{json.dumps(result_dict)}</textarea>
                            </label>
                          </td>
                        </tr>
                      </table>
                                <table width="100%" height="80" border="0" cellpadding="0" cellspacing="0" class="buttons">
                <tr>
                    <td  align="right">
                        <button class="button2" onclick="javascript :history.back(-1);" type="button">返回</button>
                    </td>
                </tr>
            </table>

            <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
                <tr>
                    <td align=center><h4>xy-nas-tool V{VERSION_INFO}.&nbsp&nbsp&nbsp&nbsp&nbsp made by xyseer.</h4></td>
                </tr>
            </table>
                        </div>'''

            return html
        else:
            return f'''<script type="text/javascript">
                                alert("Error when export: Invalid ID");history.back(-1);</script>'''
    except Exception as e:
        return f'''<script type="text/javascript">
                    alert("Error when export:{str(e)}");history.back(-1);</script>'''


@app.route("/import")
def import_page():
    html = '''<!DOCTYPE html >
        <html >
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <title>xy-nas-tools</title>
            <link href="../static/css.css" rel="stylesheet" type="text/css" />
            <style type="text/css">

            </style>
        </head>

        <body>
        <div class="box">

            <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
                <tr>
                    <td><h1>xy-nas-tool</h1></td>
                    <td width="100" align="center"><a href="./">主页</a></td>
                    <td width="100" align="center"><a href="./all">在追番剧</a></td>
                    <td width="100" align="center"><a href="./setting">设置</a></td>
                    <td width="100" align="center"><a href="./log">查看日志</a></td>
                    <td width="100" align="center"><a href="./about">关于</a></td>
                </tr>
            </table>
            <form action="/import/submit" method="post" enctype="multipart/form-data">
                <table width=80% border="1" align="center" cellpadding="1" cellspacing="0" class="main">
                    <tr>
                        <td colspan="3" width="80%" height=50 align="center"><input type="text" value="import" class="text1" name="name"></td>
                    </tr>
                </table>
                <table width=80% height="200" border="1" align="center" cellpadding="1" cellspacing="0" class="main">
                    <tr>
                        <td width="25%" align="center">导入方式</td>
                        <td width="25%" align="center">
                            <select class="text1" name="type">'''
    for i in ['json', 'hmacg']:
        html += f"<option>{i}</option>"
    html += f'''
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <td width="50%" align="center">手动输入</td>
                        <td width="50%" align="center"><input type="text" value="" class="text1" name="textinput"></td>
                    </tr>
                    <tr>
                        <td width="50%" align="center">上传文件</td>
                        <td width="50%" align="center"><input type="file" id="file" name="file" accept="txt, .xlsx"></td>
                    </tr>
                    </tr>

                </table>

                <table width="100%" height="80" border="0" cellpadding="0" cellspacing="0" class="buttons">
                    <tr>
                        <td  align="right">
                            <button class="button2" onclick="javascript :history.back(-1);" type="button">返回</button>
                            <button class="button1" type="submit" {"hidden" if not EXPERIMENTAL else ""}>提交</button>
                        </td>
                    </tr>
                </table>

                <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
                    <tr>
                        <td align=center><h4>xy-nas-tool V{VERSION_INFO}.&nbsp&nbsp&nbsp&nbsp&nbsp made by xyseer.</h4></td>
                    </tr>
                </table>
            </form>
        </div>
        </body>
        </html>'''
    return html


@app.route("/import/save", methods=["POST"])
def save_import():
    if request.method == 'POST':
        idx = 0
        scc = 0
        err_list = []
        while f'name{idx}' in request.form:
            old_img = request.form.get(f"old_img{idx}", "")
            if old_img:
                Path(old_img).unlink(missing_ok=True)
            if not request.form.get(f"save{idx}", ""):
                idx += 1
                continue
            name = request.form.get(f"name{idx}", "")
            starttime = request.form.get(f"starttime{idx}", "")
            meta = request.form.get(f"meta{idx}", "")
            totaleps = request.form.get(f"totaleps{idx}", "")
            lasttime = request.form.get(f"lasttime{idx}", "")
            lastep = request.form.get(f"lastep{idx}", "")
            nexttime = request.form.get(f"nexttime{idx}", "")
            nextep = request.form.get(f"nextep{idx}", "")
            span = request.form.get(f"span{idx}", "")
            source = request.form.get(f"source{idx}", "")
            directory = request.form.get(f"directory{idx}", "")
            way = request.form.get(f"way{idx}", "")
            filter_name = request.form.get(f"filter{idx}", "")
            img = request.files.get(f"img{idx}")
            request_dict = {}
            request_dict["id"] = get_new_subscription_item()[0].id
            if name:
                try:
                    request_dict["name"] = name
                except Exception as e:
                    err_list.append(str(e))
            if meta:
                try:
                    request_dict["info"] = meta
                except Exception as e:
                    err_list.append(str(e))
            if img:
                try:
                    new_path = str(
                        Path(STATIC_DIR) / (''.join(sample(string.ascii_letters + string.digits, 16)) + ".jpg"))
                    img.save(new_path)
                    request_dict["img"] = new_path
                except Exception as e:
                    err_list.append(str(e))
            if starttime:
                try:
                    startTime = datetime.strptime(str(starttime), HTML_INPUT_TIME_FORMAT)
                    request_dict["starttime"] = startTime
                except Exception as e:
                    err_list.append(str(e))
            if lasttime:
                try:
                    lastTime = datetime.strptime(str(lasttime), HTML_INPUT_TIME_FORMAT)
                    request_dict["lastUpdateTime"] = lastTime
                except Exception as e:
                    err_list.append(str(e))
            if nexttime:
                try:
                    nextTime = datetime.strptime(str(nexttime), HTML_INPUT_TIME_FORMAT)
                    request_dict["nextUpdateTime"] = nextTime
                except Exception as e:
                    err_list.append(str(e))
            if totaleps:
                try:
                    if int(totaleps) > 0:
                        request_dict["totalEpisodes"] = int(totaleps)
                except Exception as e:
                    err_list.append(str(e))
            if lastep:
                try:
                    if int(lastep) >= 0:
                        request_dict["lastUpdateEP"] = int(lastep)
                except Exception as e:
                    err_list.append(str(e))
            if nextep:
                try:
                    if int(nextep) >= 0:
                        request_dict["nextUpdateEP"] = int(nextep)
                except Exception as e:
                    err_list.append(str(e))
            if span:
                try:
                    if int(span) > 0:
                        request_dict["span"] = int(span)
                except Exception as e:
                    err_list.append(str(e))
            if source:
                try:
                    request_dict["source"] = str(source)
                except Exception as e:
                    err_list.append(str(e))
            if directory:
                try:
                    request_dict["directory"] = str(directory)
                except Exception as e:
                    err_list.append(str(e))
            if way:
                try:
                    request_dict["type"] = str(way)
                except Exception as e:
                    err_list.append(str(e))
            if filter_name:
                try:
                    request_dict["filter_name"] = strTolist(str(filter_name), ",")
                except Exception as e:
                    err_list.append(str(e))
            try:
                modify_item(request_dict, ss)
                scc+=1
            except Exception as e:
                err_list.append(str(e))
            idx += 1
        if err_list:
            html = f'''<script type="text/javascript">
                                        alert("处理{idx}项，已导入{scc}项, 修改失败:'''
            for i in err_list:
                html += rf'''\n {str(i)}'''
            html += '''");history.back(-1);</script>'''
            return html
        else:
            return f'''<script type="text/javascript">
                    alert("处理{idx}项，导入成功{scc}项!");window.location.href = "/all";</script>'''
    else:
        redirect(f"/all")


@app.route("/import/submit", methods=["POST"])
def import_submit():
    try:
        if request.method == 'POST':
            type = request.form.get("type", "")
            if type == "json":
                if request.form.get("textinput", ""):
                    textinput = request.form.get("textinput", "")
                    im = [json.loads(textinput), ]
                else:
                    file = request.files.get("file")
                    if file:
                        im = json.load(file.stream)
                    else:
                        raise FileNotFoundError("No valid json file found.")

            elif type == "hmacg":
                try:
                    f = getattr(__import__("web.HmacgImport", fromlist=['processing_workbook_to_list']),
                                'processing_workbook_to_list')
                except ModuleNotFoundError or AttributeError:
                    return f'''<script type="text/javascript">
                                    alert("导入失败: HmacgImport Module Not found");history.back(-1);</script>'''
                file = request.files.get("file")
                if file and file.filename.endswith('.xlsx'):
                    im = f(file.stream)
                else:
                    im = []
            else:
                return f'''<script type="text/javascript">
                alert("导入失败: Not Supported Method");history.back(-1);</script>'''
            return import_details(import_items(im))
        else:
            redirect(f"all")
    except Exception as e:
        return f'''<script type="text/javascript">
                alert("导入失败: Unexpected Error! {str(e)}");history.back(-1);</script>'''


def import_details(im_d: list):
    html = f'''
            <!DOCTYPE html >
    <html >
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>xy-nas-tools</title>
    <link href="/static/css.css" rel="stylesheet" type="text/css" />
    <style type="text/css">

    </style>
    </head>

    <body>
    <div class="box">

    <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
      <tr>
        <td><h1>xy-nas-tool</h1></td>
        <td width="100" align="center"><a href="/">主页</a></td>
        <td width="100" align="center"><a href="/all">在追番剧</a></td>
        <td width="100" align="center"><a href="/setting">设置</a></td>
        <td width="100" align="center"><a href="/log">查看日志</a></td>
        <td width="100" align="center"><a href="/about">关于</a></td>
      </tr>
      </table>
       <form action="/import/save" method="post" enctype="multipart/form-data">
      '''
    for idx, item in enumerate(im_d):
        n, s, d, m = item
        html += f'''
    
    <table width=80% border="1" align="center" cellpadding="1" cellspacing="0" class="main">
      <tr>
        <td rowspan="2" width=20% align="center"><img src="{m.img}" id="image-preview{idx}" height="300" width=100%>
    	<input type="file" id="file{idx}" name="img{idx}" accept="image/jpeg, image/png, image/jpg">
          <script type="text/javascript">
                let fileInput{idx} = document.getElementById('file{idx}');
    			let preview{idx} = document.getElementById('image-preview{idx}');
    			// 监听change事件:
    			fileInput{idx}.addEventListener('change', function() {{
    				// 清除背景图片:
    				preview{idx}.style.backgroundImage = '';
    				let file{idx} = fileInput{idx}.files[0];
    				if (!['image/jpeg', 'image/png', 'image/jpg'].includes(file{idx}.type)) {{
    					alert('不是有效的图片文件!');
    					return;
    				}}
    				// 读取文件:
    				let reader{idx} = new FileReader();
    				reader{idx}.onload = function(e) {{
    					let data{idx} = e.target.result;
    					preview{idx}.src = data{idx}
    				}};
    				// 以DataURL的形式读取文件:
    				reader{idx}.readAsDataURL(file{idx});

    			}});
    </script>
    <script>
    ''' + f'''
  const imageUrl{idx} = '{m.img}';  // your image link
  ''' + f'''
  fetch(imageUrl{idx})
    .then(res => res.blob())
    .then(blob => {{
      preview{idx}.src = URL.createObjectURL(blob);
      const file = new File([blob], imageUrl{idx}.split('/').pop(), {{ type: blob.type }});
      const dt = new DataTransfer();
      dt.items.add(file);
      fileInput{idx}.files = dt.files;
      fileInput{idx}.dispatchEvent(new Event('change'));
    }})
    .catch(err => console.error('Image load error', err));
</script>
    ''' + f'''
    </td>
        <td colspan="3" width="80%" height=50 align="center"><input type="text" value="{m.name}" class="text1" name="name{idx}"></td>
      </tr>
      <tr>
        <td colspan="3" height="60%" align="center"><textarea class="text1" name="meta{idx}">{m.info}</textarea></td>
      </tr>
    </table>
    <table width=80% height="300" border="1" align="center" cellpadding="1" cellspacing="0" class="main">
      <tr>
        <td width="25%" align="center">开播时间</td>
        <td width="25%" align="center"><input align="center" type="datetime-local" value="{s.starttime.strftime(HTML_INPUT_TIME_FORMAT)}" class="text1" name="starttime{idx}"></td>
        <td width="25%" align="center">总集数</td>
        <td width="25%" align="center"><input type="number" value="{s.totalEpisodes}" class="text1" name="totaleps{idx}"></td>
      </tr>
      <tr>
        <td width="25%" align="center">上次更新时间</td>
        <td width="25%" align="center"><input align="center" type="datetime-local" value="{s.lastUpdateTime.strftime(HTML_INPUT_TIME_FORMAT)}" class="text1" name="lasttime{idx}"></td>
        <td width="25%" align="center">上次更新集数</td>
        <td width="25%" align="center"><input type="number" value="{s.lastUpdateEP}" class="text1" name="lastep{idx}"></td>
      </tr>
      <tr>
        <td width="25%" align="center">下次更新时间</td>
        <td width="25%" align="center"><input align="center" type="datetime-local" value="{s.nextUpdateTime.strftime(HTML_INPUT_TIME_FORMAT)}" class="text1" name="nexttime{idx}"></td>
        <td width="25%" align="center">下次更新集数</td>
        <td width="25%" align="center"><input type="number" value="{s.nextUpdateEP}" class="text1" name="nextep{idx}"></td>
      </tr>
      <tr>
        <td width="25%" align="center">更新间隔</td>
        <td width="25%" align="center"><input type="number" width=80% value="{s.span}" class="span" name="span{idx}"> <label>小时</label></td>
        <td width="25%" align="center">更新方式</td>
        <td width="25%" align="center">
          <input type="text" width=80% value="{s.type}" class="text1" name="way{idx}">
        </td>
      </tr>
    </table>
      <table width=80% height="200" border="1" align="center" cellpadding="1" cellspacing="0" class="main">
        <tr>
        <td width="50%" align="center">下载来源</td>
        <td width="50%" align="center"><input type="text" value="{d.source}" class="text1" name="source{idx}"></td>
      </tr>
        <tr>
        <td width="50%" align="center">下载目录</td>
        <td width="50%" align="center"><input type="text" value="{d.directory}" class="text1" name="directory{idx}"></td>
      </tr>
        </tr>
        <tr>
        <td width="50%" align="center">过滤条件</td>
        <td width="50%" align="center">
          <select class="text1" name="filter{idx}">'''
        html += f"<option>{listTostr(d.filter_name)}</option>"
        for i in Parameters().FILTER_DICTS.keys():
            if i not in d.filter_name:
                html += f"<option>{i}</option>"
        html += f'''
          </select>
        </td>
      </tr>
      <tr>
        <td width="50%" align="center">是否保存</td>
        <td width="50%" align="center"><input type="checkbox" name="save{idx}"></td>
      </tr>
        <tr>
        <input type="hidden" name="old_img{idx}" value="{m.img}">
      </tr>
      </table>
      <span><br><br><br><br></span>
      <span></span>
        '''
    html += '''
          <table width="100%" height="80" border="0" cellpadding="0" cellspacing="0" class="buttons">
      <tr>
        <td  align="right">
          <button class="button2" onclick="javascript :history.back(-1);" type="button">返回</button>
          <button class="button1" type="submit">提交</button>
        </td>
      </tr>
    </table>
    </form>
    <table width="100%" border="0" cellpadding="0" cellspacing="0" class="nav">
      <tr>
        <td align=center><h4>xy-nas-tool V{VERSION_INFO}.&nbsp&nbsp&nbsp&nbsp&nbsp made by xyseer.</h4></td>
      </tr>
    </table>
      </div>
    </body>
    </html>
        '''
    return html


def flask_main(S_C: SubscribeCore):
    try:
        global ss
        ss = S_C
        app.run("0.0.0.0", 12138)
        Logger().error("================MAIN PROCESS UNEXPECTED EXIT=================")
    except KeyboardInterrupt:
        Logger().info("================MAIN PROCESS TERMINATE=================")
        exit(0)
    except InterruptedError:
        Logger().info("================MAIN PROCESS TERMINATE=================")
        exit(0)
    except Exception as e:
        Logger().error(f"mainThread:{str(e)}")
        pass
