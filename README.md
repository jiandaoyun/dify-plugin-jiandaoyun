## jiandaoyun

**Author:** hectum_shen
**Version:** 0.0.1
**Type:** tool

### Description

简道云dify插件，提供了基本的简道云表单API插件，能够支持查询应用、表单、表单内数据等基本能力，并且支持新增、修改、删除表单内数据的能力。

## 基础功能

### 1.查询所有应用（app management）

通过此功能，可以查询到持有api_key的用户下，有权限访问的全部表单的信息，返回结构为text和json，其中包含表单的名称和entry_id




### 2.新建单条数据（create data）
通过此功能，可以在指定的表单中新增一条数据，返回结构为text和json，其中包含新增数据的id，以及新增后数据的具体内容（无效的内容、不符合格式的内容会自动置空）

### 3.查询单条数据（query data）
根据具体的数据的data_id，结合entry_id和app_id，可以查询到指定的单条数据，返回结构为text和json，其中包含数据的具体内容

### 4.修改单条数据（update data）
根据具体的数据的data_id，结合entry_id和app_id，可以修改指定的单条数据，返回结构为text和json，其中包含修改后数据的具体内容和更新者信息

### 5.删除单条数据（delete data）
删除指定data_id的单条数据

### 6.查询全部表单（query entries）
根据用户提供的app_id，可以查询到指定应用下的全部表单信息，返回结构为text和json，其中包含表单的名称和entry_id，可以使用limit和offset进行分页查询

### 7.查询多条数据（query data list）
根据app_id和entry_id对于指定表单下进行数据批量查询，可以使用fields指定查询字段（数组），使用filter进行条件查询

### 8.查询表单字段（query widgets）
根据app_id和entry_id可以查询到指定表单下的全部字段信息，返回结构为text和json，其中包含字段的名称、类型、是否必填等信息

## 安装和使用
### Prerequisites
无特定

### Install the Plugin
在marketplace安装简道云dify插件，然后在配置中填写api_key即可，api_key的获取方式，请访问[简道云开放平台](http://jiandaoyun.com/open#/key/api_key)自行创建获取，具体创建规则以及使用方法可以查看[简道云文档](https://hc.jiandaoyun.com/open/11498)"



