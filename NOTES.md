# Notes
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

