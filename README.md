# Hadoop-build-env
> Automatically `Deploy`, `Configure`, `Benchmark`, and `Performance Report`

Here does focus on hadoop-3.0.0-alpha2 mainly.

We am willing to contribute to the hadoop community, and making our efforts.

## How to use
Users need to change/assign variables in `0.*.sh` script files, and run script by ascend order.

*PSEUDO_DIS_MODE* 
```
run, compile, benchmark and all actions are only in your dev-PC.

           run|compile|bench|report
    user ------> |__|
                dev-pc

1. setup `HADOOP_CLUSTER_MODE='PSEUDO_DIS_MODE'`
2. run install.sh run && install.sh src
```

*FULLY_DIS_MODE*

```
compile, view report are only in yout dev-PC.
run, benchmark, performance log are in cluster-PCs.

                                  run|bench
         compile|report          |_|_|_|_|_|    
    user ---> |__| ----------->  |_|_|_|_|_|
             dev-pc   deploy     |_|_|_|_|_|
                      *.jar     hadoop cluster     

1. setup `HADOOP_CLUSTER_MODE='FULLY_DIS_MODE'`
2. setup `HADOOP_FDM_NODES`
3. run install.sh src

```

## Notes

[Git & Bash](./NOTES-Git-Bash.md)

[Compile](./NOTES-Compile.md)

## References

[Hadoop: BUILDING.txt](https://git-wip-us.apache.org/repos/asf?p=hadoop.git;a=blob;f=BUILDING.txt)

[Hadoop: How To Contribute](https://wiki.apache.org/hadoop/HowToContribute)

[Book: Apache Hadoop YARN](http://yarn-book.com/)

