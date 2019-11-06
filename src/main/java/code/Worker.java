package code;
import java.lang.Thread;
import java.util.Map;
import java.lang.InterruptedException;

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
		try {
		    Thread.sleep(5000);
		} catch (InterruptedException ie) {
			System.out.println("Worker interrupted");
		}


		System.out.println(String.format("-> %s", component.name));
	}	
}
