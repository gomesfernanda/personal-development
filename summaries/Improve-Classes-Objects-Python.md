# Summary for the article "Improve your Python classes and object oriented programming"
[link for it here](https://jeffknupp.com/blog/2014/06/18/improve-your-python-python-classes-and-object-oriented-programming/)

- Class is like the blueprint (or model) for creating objects
- The object itself will be when you create an _instance_ of that class
- `self` is the instance that the user will create
- `__init__` method: initialize the object
	- rule of thumb: don't *introduce* a new attribute outside the `__init__` method
### Instance attributes
- A function defined in a class is called a *method*
	- They can access and modify anything previously set on `self`.
- *Static methods*
	- Class attributes are attributes that are set at the class-level.
	- Static methods don't have access to `self`, because they don't "call" self parameter when defined.
- *Class methods*
	- Variant of the static method.
	- Instead of receiving the *instance* as the first parameter, it is passed the *class*.
	- Class methods are used more often in connection with _inheritance_.
### Inheritance
- Is the process by which a "child" class derives the data and behavior of a "parent" class.
- *Abstract classes*
	- Concepts that other objects will inherit some characteristics.
	- For example, "vehicle" would be an abstract class, while "car" and "truck" would be the _real_ objects deriving from vehicle.
	- ABC: Abstract Base Class
	- When you're creating an ABC, you need to define the meta class `ABCMeta` that is inside the `abc` module.