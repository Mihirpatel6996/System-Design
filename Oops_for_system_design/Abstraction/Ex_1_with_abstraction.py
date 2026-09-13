from abc import ABC, abstractmethod
# ABC Class is a base class for defining abstract classes in Python. It allows us to create classes that cannot be instantiated directly and must be subclassed. The abstract methods defined in the ABC class must be implemented by any subclass that inherits from it.

# Internally ow ABC class uses a metaclass called ABCMeta, which is responsible for enforcing the abstract method requirements. When a class inherits from ABC, it is marked as an abstract class, and any subclass must implement all the abstract methods defined in the ABC class. metaclass is a class that defines the behavior of other classes. In this case, ABCMeta is the metaclass that provides the functionality for creating abstract classes and enforcing the implementation of abstract methods.

# the reason we cannot use metaclass directly is that it is a lower-level construct that requires more manual handling. ABC provides a higher-level abstraction that simplifies the process of creating abstract classes and enforcing method implementation.

# we have defied a contract for performance testing, any class that implements this interface must provide implementations for the start, stop, and get_results methods.

class PerformanceTest(ABC):  ## This says:Any performance test must implement these methods,But how it does it is not defined here

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def get_results(self):
        pass

# concrete Implementation 

class LoadRunnerTest(PerformanceTest):

    def start(self):
        print("LoadRunner: starting test")

    def stop(self):
        print("LoadRunner: stopping test")

    # def get_results(self):
    #     return {"throughput": 1000} // lets not implement this method, so that we can see the effect of not implementing it

load_runner_test = LoadRunnerTest()
load_runner_test.start()

'''

We get the type error because we are trying to instantiate the LoadRunnerTest class, which is a subclass of the abstract class PerformanceTest. Since LoadRunnerTest does not provide an implementation for the abstract method get_results, it is considered an abstract class itself and cannot be instantiated.

Traceback (most recent call last):
  File "c:\Users\DELL\Desktop\System Design\System-Design\Oops_for_system_design\Abstraction\Ex_1_with_abstraction.py", line 37, in <module>
    load_runner_test = LoadRunnerTest()
                       ^^^^^^^^^^^^^^^^
TypeError: Can't instantiate abstract class LoadRunnerTest without an implementation for abstract method 'get_results'
'''


## Another proper implementation 

class JMeterTest(PerformanceTest):

    def start(self):
        print("JMeter: starting test")

    def stop(self):
        print("JMeter: stopping test")

    def get_results(self):
        return {"throughput": 800}

jmeter_test = JMeterTest()
jmeter_test.start()
jmeter_test.stop()
results = jmeter_test.get_results() ## this will work fine because we have implemented all the abstract methods defined in the PerformanceTest class.


# why it matters -- because we can now write code that works with any performance test, regardless of the specific implementation. This allows us to write code that is more flexible and extensible, as we can easily swap out one performance test for another without having to change the code that uses it.
def run_test(test: PerformanceTest):
    test.start()
    # wait...
    test.stop()
    return test.get_results()

# Usage
run_test(LoadRunnerTest())
run_test(JMeterTest())


