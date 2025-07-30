#!/bin/bash

# CYT博客Docker部署脚本

echo "开始部署CYT博客..."

# 检查Docker和Docker Compose是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker未安装，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 创建环境变量文件
if [ ! -f .env ]; then
    echo "创建环境变量文件..."
    cp .env.example .env
    echo "请编辑 .env 文件，设置正确的环境变量"
    read -p "按回车键继续..."
fi

# 构建并启动服务
echo "构建Docker镜像..."
docker-compose build

echo "启动服务..."
docker-compose up -d

# 等待数据库启动
echo "等待数据库启动..."
sleep 10

# 运行数据库迁移
echo "运行数据库迁移..."
docker-compose exec web python manage.py migrate

# 创建超级用户（可选）
echo "是否创建超级用户？(y/n)"
read -r create_superuser
if [ "$create_superuser" = "y" ]; then
    docker-compose exec web python manage.py createsuperuser
fi

# 收集静态文件
echo "收集静态文件..."
docker-compose exec web python manage.py collectstatic --noinput

echo "部署完成！"
echo "访问 http://localhost 查看博客"
echo "访问 http://localhost/admin/ 进入Django管理后台"
echo "访问 http://localhost/custom-admin/ 进入自定义管理后台"

# 显示服务状态
docker-compose ps