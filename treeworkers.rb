require 'json'

components = JSON.parse(File.read("data.json"))

threads = Hash.new

components = components.sort_by { |item| item["position"] }

components.each { |component| 
	threads[component["name"]] = Thread.new {
		component["ancestors"].each {  |ancestor| 
			threads[ancestor].join()
		}	
		puts("<- #{component["name"]}")
		sleep(5)
		puts("-> #{component["name"]}")
	}
}

components.each { |component| 
	threads[component["name"]].join()	
}
