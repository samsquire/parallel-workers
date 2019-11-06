package code;
import org.chocosolver.solver.Model;
import org.chocosolver.solver.variables.IntVar;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.File;
import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.io.IOException;
import java.util.Collections;
import java.util.Comparator;
import code.*;

public class Scheduler {

	
	public static void main(String[] args) {
		ObjectMapper om = new ObjectMapper();
		try {
			List<Component> components = om.readValue(new String(Files.readAllBytes(Paths.get("unscheduled.json"))), new TypeReference<List<Component>>(){});

		Model model = new Model("parallel");
		Map<String, IntVar> variables = new HashMap<>();
		
		for (Component component : components) {
			variables.put(component.name, model.intVar("start", 0, components.size()));	
		}

		for (Component component : components) {
			for (String ancestor : component.ancestors) {
				model.arithm(variables.get(ancestor), "<", variables.get(component.name)).post();
			}
			for (String successor : component.successors) {
				model.arithm(variables.get(successor), ">", variables.get(component.name)).post();
			}
		}	

		model.getSolver().solve();

		for (Component component : components) {
			System.out.println(String.format("%s %d", component.name, variables.get(component.name).getValue()));		
			component.position = variables.get(component.name).getValue();
		}

		Collections.sort(components, new Comparator<Component>() {
			public int compare(Component a, Component b) {
				if (a.position > b.position) {
					return 1;
				} else {
					return -1;
				}
					
			}	
		});

		om.writeValue(new File("data.json"), components);


		} catch(IOException io) {
			System.out.println("Could not load file");
			System.out.println(io.getMessage());
		}
		System.exit(0);
	}

}
