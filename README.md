# Hadoop-build-env
> Automatical `deployment`, `configuration`, `benchmark execution`, and `performance report`

Here mainly focus on hadoop-3.0.0-beta1.
And we take delight in contribution in efficient cluster scheduling and approaches that can help it.

## How to run
1. [optional]. Customize `setting.yaml` according to user demands.

2. [optional]. Create soft/hard link in the folder within $PATH.
```bash
# sudo ln -s <absolute path>/hbe <folder in $PATH>/<name you liked>
#
# example. Enter hadoop-build-env folder 
$ sudo ln -s `pwd`/hbe /usr/bin/hbe
```

3. Run `bhe <stage(s)>`  . 
```shell
# prepare enviroment in control-proxy and cluster for all actions 
$ hbe init 

# install nessary libs in control-proxy for compiling...
$ hbe initcontrolp 

# initally compile source code, configure site, distribute binary libs into cluster, 
# prepare runtime environment for cluster
$ hbe initdeploy 

# prepare runtime environment for cluster 
$ hbe initcluster 

# initially compile source code in control-proxy.
# This stage will resolve maven depandency and download necessary jars.
$ hbe initcompile  
		  
# configure site.xml, worker, hadoop-env.sh ...
$ hbe config 

# compile source code, configure site, distribute binary libs into cluster
$ hbe deploy 

# compile source code in control-proxy. default compile hadoop-main.
# params: rm, nm
$ hbe compile 
              
# add permissions for stage-sync, and also create hdfs dirs ...
$ hbe syncp 

# distribute binary libs into cluster. default sync hadoop-main.
# params: rm, nm
$ hbe sync
           
# clean cluster files. 
# params: log
$ hbe clean 

# default start-all.sh. 
# params: yarn, hdfs
$ hbe start

# default stop-all.sh.
# params: yarn, hdfs 
$ hbe stop 

# ========================EXAMPLES AS FOLLOWING======================== #

$ hbe initcompile # first compile

$ hbe initdeploy # first compile and deploy

$ hbe deploy

$ hbe compile && hbe config && hbe stop && hbe sync && hbe strart

$ hbe compile rm nm 

$ hbe sync rm nm 

$ hbe clean log
```


*PSEUDO_DIS_MODE* 
```
run, compile, benchmark and all actions are only in your dev-PC.

           run|compile|bench|report
    user ------> |__|
            control-proxy-pc
```

*FULLY_DIS_MODE*

```
compile, view report are only in yout dev-PC.
run, benchmark, performance log are in cluster-PCs.

                                        run jobs/benchmark
            compile|report    deploy      |_|_|_|_|_|    
    user ------> |__| ----------------->  |_|_|_|_|_|
           control-proxy-pc               |_|_|_|_|_|
                                *.jar       cluster     
```

## How to customize step(s) and organize stage(s)

Rules:
1. put `*.py` into `./scripts/` and `*.sh` into `./utilities/`
2. customized python files need to inherit `basis.py` and overwrite its `action()` method.
3. define `tigger` function to support automatical execution. 


## Notes

[Git & Bash](./docs/notes.git-bash.md)

[Compile](./docs/notes.maven-compilation.md)

## References

[Hadoop: BUILDING.txt](https://git-wip-us.apache.org/repos/asf?p=hadoop.git;a=blob;f=BUILDING.txt)

[Hadoop: How To Contribute](https://wiki.apache.org/hadoop/HowToContribute)

[Book: Apache Hadoop YARN](http://yarn-book.com/)

