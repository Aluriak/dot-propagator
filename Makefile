
tree:
	$(MAKE) dot TEST_CASE=tree
hole:
	$(MAKE) dot TEST_CASE=pigeon-hole
euler:
	$(MAKE) dot TEST_CASE=euler
fizzbuzz:
	$(MAKE) dot TEST_CASE=fizzbuzz
truth1:
	$(MAKE) dot TEST_CASE=truth1


dot: dot_run dot_conv dot_show
dot_run:
	- clingo -n 0 dotpropagator.lp ./test_cases/$(TEST_CASE).lp
dot_conv:
	dot -Tpng out/out.dot > out/out.png
dot_show: dot_conv
	feh out/out.png
