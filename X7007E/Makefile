runToEnd:
	sudo altwalker online tests -m models/vlanModel.json "random(reached_vertex(v23))"
runRand:
	@echo "Running with time=${time}"
	@if [ -e my_log_file.log ]; then sudo rm my_log_file.log; fi
	sudo altwalker online tests -m models/vlanModel.json "random(time_duration(${time}))"
test:
	sudo altwalker offline -m models/vlanModel.json "random(reached_vertex(v23))"
