.PHONY: format
format:
	black meggie_difference

.PHONY: check
check:
	black --check meggie_difference
	pylama meggie_difference

.PHONY: test
test:
	pytest -s
