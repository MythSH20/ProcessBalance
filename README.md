项目介绍：调度器训练程序采用模块化处理，下辖模块有affinity模块，管理调度器的实际调度动作执行。Info模块负责采集系统与进程信息，stress模块中设置有所有的压力负载。调度器的训练入口已在main中集成。对于小样本任务，执行时先获取压力测试负载任务，接着通过Subprocess包执行编译、运行的命令，期间收集进程的信息。调度器会采集系统信息，可在任意windows系统中运行

项目所需软件包：data/condalist.txt
python版本：3.8.19
运行方法：对于小样本任务，配置好所需环境与软件包后，在main.py中直接启动，可在main函数中调整训练轮次与并发线程数。


