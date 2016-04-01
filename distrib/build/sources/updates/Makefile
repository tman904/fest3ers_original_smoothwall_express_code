# Keep 'make clean' tidy.

clean:
	@for i in update[1-9]*; do if [ -d $$i ]; then cd $$i; make clean; fi; done
