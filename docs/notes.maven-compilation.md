# Notes
> +. mvn 

## mvn

```bash
#
# mvn dependency:list        查看当前项目的已解析依赖
# mvn dependency:tree        查看当前项目的依赖树
# mvn dependency:analyze     工具可以帮助分析当前项目的依赖
# 
# mvn compile                编译项目的主源代码
# mvn test-compile           编译项目的中测试代码
# mvn test                   使用单元测试框架运行测试，测试代码不会被打包或部署
# mvn package                接受编译好的代码，打包成可发布的格式
# mvn verify                 运行任何检查，验证包是否有效且达到质量标准。
# mvn install                将包安装到Maven本地仓库，供本地其他Maven项目使用
# mvn deploy                 将最终的包复制到远程仓库，供其他开发人员和Maven项目使用
#
#
# Tips1： 网络下载超时，命令可能运行失败
#                可以将命令嵌入循环中，直至命令成功运行退出循环
#
# $? 2>/dev/null; while [ $? -ne 0 ]; do 待执行命令; done
# 例如：
# $? 2>/dev/null; while [ $? -ne 0 ]; do mvn clean; done
# $? 2>/dev/null; while [ $? -ne 0 ]; do mvn test; done
# $? 2>/dev/null; while [ $? -ne 0 ]; do mvn package; done
# $? 2>/dev/null; while [ $? -ne 0 ]; do mvn install -DskipTests; done
# $? 2>/dev/null; while [ $? -ne 0 ]; do mvn install; done
# $? 2>/dev/null; while [ $? -ne 0 ]; do mvn deploy; done

$? 2>/dev/null; while [ $? -ne 0 ]; do mvn clean install -DskipTests site ; done

```
