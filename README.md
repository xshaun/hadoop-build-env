# Hadoop-build-env
> Automatical `deployment`, `configuration`, `benchmark execution`, and `performance report`

Here mainly focus on hadoop-3.0.0-beta1.
And we take delight in contribution in efficient cluster scheduling and approaches that can help it.

## How to run
1. customize `setting.yaml` according to user demands.

2. run `bhe <stage(s)>`  e.g.
```shell

hbe init # prepare enviroment in control-proxy and cluster for all actions 

hbe initcontrolp # install nessary libs in control-proxy for compiling...

hbe initcompile # initially compile source code in control-proxy. This will resolve maven depandency and download a number of jar libs.

hbe initcluster # install nessary libs in cluster for running... 

hbe initdeploy  # configure site, distribute binary libs into cluster, prepare execution environment in cluster

hbe config # configure site.xml, worker and some configuration.

hbe deploy  # configure site, distribute binary libs into cluster to cluster

================================================================

hbe compile  # compile source code in control-proxy

hbe sync  # distribute binary libs into cluster 

hbe start  # run start-all.sh

hbe stop  # run stop-all.sh

================================================================
# usually used:

hbe compile config sync strart

hbe compile sync strart

hbe compile deploy

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
```
Rules:
1. put `*.py` into `./scripts/` and `*.sh` into `./utilities/`
2. customized python files need to inherit `basis.py` and overwrite its `action()` method.
3. define `tigger` function to support automatical execution. 

```

## Notes

[Git & Bash](./docs/notes.git-bash.md)

[Compile](./docs/notes.maven-compilation.md)

## References

[Hadoop: BUILDING.txt](https://git-wip-us.apache.org/repos/asf?p=hadoop.git;a=blob;f=BUILDING.txt)

[Hadoop: How To Contribute](https://wiki.apache.org/hadoop/HowToContribute)

[Book: Apache Hadoop YARN](http://yarn-book.com/)

