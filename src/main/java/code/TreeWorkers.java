package code;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.io.IOException;
import java.util.Collections;
import java.util.Comparator;
import code.*;

public class TreeWorkers {

	
	public static void main(String[] args) {
		ObjectMapper om = new ObjectMapper();
		try {
			List<Component> components = om.readValue(new String(Files.readAllBytes(Paths.get("data.json"))), new TypeReference<List<Component>>(){});

			Collections.sort(components, new Comparator<Component>() {
				public int compare(Component a, Component b) {
					if (a.position > b.position) {
						return 1;
					} else {
						return -1;
					}
						
				}	
			});

			Map<String, Worker> workers = new HashMap<>();

			for (Component component : components) {
				Worker worker = new Worker(component, workers);
				workers.put(component.name, worker);
				System.out.println(String.format("-> %s", component.name));
			}

			for (Component component : components) {
				workers.get(component.name).start();
			}
			for (Worker worker : workers.values()) {
				try {
					worker.join();
				} catch (InterruptedException ie) {
					System.out.println("Interrupted waiting for worker to finish");	
				}
			}


		} catch(IOException io) {
			System.out.println("Could not load file");
			System.out.println(io.getMessage());
		}
		System.exit(0);
	}

}
