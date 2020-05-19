### 1. 依赖
 `MySqlOperator` 的数据库交互通过 `MySQLdb` 模块来实现, 使用前需要安装相关依赖:
```Shell
pip install apache-airflow[mysql]
```
### 2. 使用

使用 `MySqlOperator` 执行sql任务的一个简单例子:
```Python
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.mysql_operator import MySqlOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['j_hao104@163.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

dag = DAG(
    'MySqlOperatorExample',
    default_args=default_args,
    description='MySqlOperatorExample',
    schedule_interval="30 18 * * *")

insert_sql = "insert into log SELECT * FROM temp_log"


task = MySqlOperator(
    task_id='select_sql',
    sql=insert_sql,
    mysql_conn_id='mysql_conn',
    autocommit=True,
    dag=dag)
```

### 3. 参数
`MySqlOperator` 接收几个参数:

  * `sql`: 待执行的sql语句;
  * `mysql_conn_id`: mysql数据库配置ID, Airflow的conn配置有两种配置方式，一是通过`os.environ`来配置环境变量实现，二是通过web界面配置到代码中,具体的配置方法会在下文描述;
  * `parameters`: 相当于`MySQLdb`库的`execute` 方法的第二参数,比如: `cur.execute('insert into UserInfo values(%s,%s)',('alex',18))`;
  * `autocommit`: 自动执行 `commit`;
  * `database`: 用于覆盖`conn`配置中的数据库名称, 这样方便于连接统一个mysql的不同数据库;

### 4. `conn`配置

![](index_files/_7B3DEB9FB4-8B39-E0B6-6329-35711BA04258_7D.jpg)

建议`conn`配置通过web界面来配置，这样不用硬编码到代码中，关于配置中的各个参数:

  * `Conn Id`: 对应 `MySqlOperator` 中的 `mysql_conn_id`；
  * `Host`: 数据库IP地址;
  * `Schema`: 库名, 可以被`MySqlOperator`中的`database`重写;
  * `Login`: 登录用户名;
  * `Password`: 登录密码;
  * `Port`: 数据库端口;
  * `Extra`: `MySQLdb.connect`的额外参数,包含`charset`、`cursor`、`ssl`、`local_infile`
 
其中`cursor`的值的对应关系为: `sscursor` —> `MySQLdb.cursors.SSCursor`; `dictcursor` —> `MySQLdb.cursors.DictCursor`; `ssdictcursor` —> `MySQLdb.cursors.SSDictCursor`

