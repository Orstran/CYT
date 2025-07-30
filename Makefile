# CYT博客Docker管理命令

.PHONY: help build up down restart logs shell migrate collectstatic createsuperuser backup restore clean

help:
	@echo "CYT博客Docker管理命令:"
	@echo "  build          - 构建Docker镜像"
	@echo "  up             - 启动所有服务"
	@echo "  down           - 停止所有服务"
	@echo "  restart        - 重启所有服务"
	@echo "  logs           - 查看日志"
	@echo "  shell          - 进入Django shell"
	@echo "  migrate        - 运行数据库迁移"
	@echo "  collectstatic  - 收集静态文件"
	@echo "  createsuperuser - 创建超级用户"
	@echo "  backup         - 备份数据库"
	@echo "  restore        - 恢复数据库"
	@echo "  clean          - 清理Docker资源"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

shell:
	docker-compose exec web python manage.py shell

migrate:
	docker-compose exec web python manage.py migrate

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

backup:
	docker-compose exec db pg_dump -U cytblog_user cytblog > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore:
	@read -p "输入备份文件名: " backup_file; \
	docker-compose exec -T db psql -U cytblog_user cytblog < $$backup_file

clean:
	docker-compose down -v
	docker system prune -f
	docker volume prune -f