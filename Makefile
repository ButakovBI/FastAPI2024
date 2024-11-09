.PHONY: style test coverage all clean run help all

all:
	docker compose build
	docker compose up -d

test:
	@echo "Запуск всех тестов с покрытием..."
	coverage run -m pytest tests
	coverage report -m

style:
	@echo "Запуск линтинга с flake8 и автоформатирования с autopep8..."
	flake8 src/*.py tests/*.py
	autopep8 --in-place --aggressive --aggressive src/*.py tests/*.py

coverage:
	@echo "Генерация HTML отчета о покрытии..."
	coverage html


clean:
	@echo "Очистка..."
	rm -rf .pytest_cache .ruff_cache __pycache__ */__pycache__ */*/__pycache__
	rm -rf .coverage htmlcov
	rm -f output_config.json

help:
	@echo "Доступные команды:"
	@echo "  make all            			- Линтинг кода, запуск тестов и проверка покрытия"
	@echo "  make test           			- Запуск тестов и проверка покрытия кода"
	@echo "  make style          			- Запуск линтинга flake8 и форматирование кода с помощью autopep8"
	@echo "  make coverage       			- Генерация HTML отчета о покрытии"
	@echo "  make clean          			- Очистка временных файлов и отчетов о покрытии"
	@echo "  make help           			- Отображение этого сообщения помощи"
