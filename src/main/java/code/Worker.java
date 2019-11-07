package code;
import java.lang.Thread;
import java.util.Map;
import java.lang.Runtime;
import java.io.File;
import java.lang.Process;
import java.lang.InterruptedException;
import java.io.IOException;

public class Worker extends Thread {
	Component component;
	Map<String, Worker> workers;

	public Worker(Component component, Map<String, Worker> workers) {
		super();
		this.component = component;
		this.workers = workers;
	}

	public void run() {
		for (String ancestor : component.ancestors) {
			try {
				workers.get(ancestor).join();
			} catch (InterruptedException ie) {
				System.out.println("Interrupted waiting for parent");
			}
		}

		System.out.println(String.format("<- %s", component.name));		
		ProcessBuilder pb = new ProcessBuilder("sleep", "5");
		Map<String, String> env = pb.environment();
		env.put("VAR1", "myValue");
		env.remove("OTHERVAR");
		env.put("VAR2", env.get("VAR1") + "suffix");
		
		try {
			Process p = pb.start();
			p.waitFor();
		} catch (IOException io) {
			System.err.println(io.getMessage());
		} catch (InterruptedException ie) {
			System.err.println(ie.getMessage());
		}

		System.out.println(String.format("-> %s", component.name));
	}	
}
