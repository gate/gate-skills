方法一：直接用远程版本覆盖本地文件，然后 merge

# 先把 skills 目录的文件恢复成 origin/develop 的版本
git checkout origin/develop -- skills/
# 然后再 merge
git merge origin/develop

如果这里提示失败，
# 先 commit checkout 过来的文件
git commit -m "chore: sync skills directory from develop"
先把本地文件commit进去



方法二：如果你还有其他文件需要保留修改，可以只针对冲突文件


# 取消暂存并丢弃 skills 目录的所有修改
git restore --staged skills/
git restore skills/
# 然后 merge
git merge origin/develop