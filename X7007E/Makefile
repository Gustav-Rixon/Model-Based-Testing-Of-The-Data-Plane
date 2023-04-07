runToEnd:
	sudo altwalker online tests -m models/vlanModel.json "random(reached_vertex(v23))"
runRand:
	@echo "Running with time=${time}"
	sudo rm my_log_file.log
	sudo altwalker online tests -m models/vlanModel.json "random(time_duration(${time}))"
test:
	sudo altwalker offline -m models/vlanModel.json "random(reached_vertex(v23))"
