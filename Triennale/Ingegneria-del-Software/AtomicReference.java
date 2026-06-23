package informatica.ingegneria.software.concurrency.atomic;

import java.util.function.UnaryOperator;

public class AtomicReference<T> {
	private T value; // Oggetto a cui stiamo facendo riferimento
	private Object mutex; // Mutex
	
	public AtomicReference() {
		this.value = null;
		this.mutex = new Object();
	}
	
	public AtomicReference(T value) {
		this.value = value;
		this.mutex = new Object();
	}
	
	public T get() {
		synchronized(mutex) {
			return value;
		}
	}
	
	public void set(T value) {
		synchronized(mutex) {
			this.value = value;
		}
	}
	
	public T getAndSet(T value) {
		synchronized(mutex) {
			T result = this.value;
			this.value = value;
			
			return result;
		}
	}
	
	public T getAndUpdate(UnaryOperator<T> update) {
		synchronized(mutex) {
			T result = value;
			this.value = update.apply(value);
			
			return result;
		}
	}
	
	public T updateAndGet(UnaryOperator<T> update) {
		synchronized(mutex) {
			T result = update.apply(value);
			this.value = result;
			
			return result;
		}
	}
}
