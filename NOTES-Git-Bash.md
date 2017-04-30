# Notes
> +. bash
> +. git

## Bash
1. 指定行号后插入
```bash
sed -i '16a "hello hadoop"' ./hadoop.xml
```

2. shell 变量嵌套
```bash
a=2
b=a
echo ${!b} # 2
```

3. shell 数组循环
```bash
arr=(
    "apple"
    "banana"
    "orange"
    )
for item in ${arr[@]}; do
    echo $item
done
```

## Git
1. 创建并跟踪远程一个分支
```bash
git checkout -b <local branch> origin/<branch name>
git checkout -b <local branch> <tag name>
```

2. 删除远程分支和tag
```bash
git push origin --delete <branchName>
git push origin --delete tag <tagname>
```
