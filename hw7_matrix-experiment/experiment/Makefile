.PHONY: test
test: matrix_experiment_sim
	@rm -rf out && mkdir out
	@for exp in m1024-b16 m8192-b64 m65536-b256 m65536-b4096 ; do \
		for impl in smart naive ; do \
			echo "t-sim-$$exp-$$impl" ; \
			./matrix_experiment_sim $$exp $$impl >out/t-sim-$$exp-$$impl ; \
		done ; \
	done

CXXFLAGS=-std=c++17 -O3 -Wall -Wextra -g -Wno-sign-compare

matrix_experiment_sim: matrix_transpose.h matrix_tests.h matrix_experiment_sim.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) matrix_experiment_sim.cpp -o $@

.PHONY: clean
clean::
	rm -f matrix_experiment_sim
	rm -rf out

