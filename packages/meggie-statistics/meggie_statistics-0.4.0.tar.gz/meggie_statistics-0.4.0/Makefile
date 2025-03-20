.PHONY: format
format:
	black meggie_statistics

.PHONY: check
check:
	black --check meggie_statistics
	pylama meggie_statistics

.PHONY: test
test:
	pytest -s
