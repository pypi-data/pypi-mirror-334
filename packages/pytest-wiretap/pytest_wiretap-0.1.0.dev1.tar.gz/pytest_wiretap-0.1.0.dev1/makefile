install:
	uv pip install -e .

public:
	uv build
	uvx twine upload dist/*
	make clean

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf build/ dist/
