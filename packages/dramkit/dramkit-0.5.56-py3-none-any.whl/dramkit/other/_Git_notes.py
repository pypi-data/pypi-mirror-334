# -*- coding: utf-8 -*-

# Git笔记

"""
# gitGUI连接github Repository步骤:
step1：git命令：ssh-keygen -t rsa -C "邮箱" ，生成SSH Key，默认存放在用户文件夹的.ssh下面
step2：将生成的SSH Key添加到github的SSH Key设置里面。即复制.ssh/id_rsa.pub里面的内容添加到github设置里面的SSH Key中（这是本地与github的通信密码）。
step3：用git命令：ssh -T git@github.com进行连接测试
step4：用git命令添加用户信息：
    git config --global user.name github用户名
    git config --global user.email github邮箱
这样，本地与github的连接设置就完成了。
step5：在github上新建Repostitory
step6：打开git GUI将github上的项目克隆到本地
step7：在git GUI里面进行文件修改，提交，上传等操作

# git push 远程主机名 本地分支名:远程分支名
git push --force origin modellink:modellink

# 合并最近三条提交
# git rebase -i HEAD~3

# 与上一条commit合并commit
# git commit --amend

# 从fork的原始项目更新
# 查看remote
git remote -v
# 添加upstream
git remote add upstream https://gitee.com/ascend/ModelLink.git
# 查看remote变化
git remote -v
# 从upstream更新代码到本地（pull=fetch+merge）
git pull upstream master
# 远程提交
git push origin master:master
# 更新其他分支
git checkout 1.1
git pull upstream 1.1
git push origin 1.1:1.1

# 查看所有分支
git branch -a

# 从master新建dev分支并切换到该分支
git checkout -b dev

# 将master分支内容合并到当前分支
git merge master

# """