# Introducing Go, by Caleb Doxsey
(link for the book [here](http://shop.oreilly.com/product/0636920046516.do))

## Chapter 1: Getting Started
**Machine Setup**
- A text editor (author recommends Atom).
- The terminal: since Go is a compiled language, it makes heavy use of the *command line*.
- Environment: the Go toolset uses an environment variable called `GOPATH` to find Go source code. To make things easier, we set it to the same as your home directory. To set `GOPATH`:
    - On Windows: on the terminal, type

    `setx GOPATH %USERPROFILE%`
    - On OS X: on the terminal, type

    `echo 'export GOPATH=$HOME\n' >> ~/.bash_profile`
- Go: download and run the installer for your platform from [golang.org/dl](http://golang.org/dl)
    - To confirm everything is working, open a terminal and type:

    `go version`
    This should not throw an error.

**Your first program**

- Create a folder named *~/src/golang-book/chapter1*
- Open the text editor, create a new file and enter:

```go
package main

import "fmt"

// this is a comment

func main() {
    fmt.Println("Hello, world")
}
```

Save your file as *main.go*.
Now, go to your terminal and, when inside the *chapter1* directory, type `go run main.go`.

**Reading your code**

Go programs must start with a *package declaration*, in this case `package main`. It is a way Go has to organize and reuse code.

The `import` keyword is how we include code from other packages to use with our program. The `fmt` package implements formatting for inout and output.

The line that starts with `//` is a *comment*, ignored by Go compilers but useful for observations you may want to include. Go supports `//` comments for one-line and `/*   */` for multiple lines.

After, you see the function declaration

```go
func main() {
    fmt.Println("Hello, world")
}
```

Functions are building block of Go. All functions must start with the keyword `func` followed by the name of the function, a list of zero or more parameters, an optional return type, and a body.
The name `main` is special because it's the function that gets called when you execute the program.

Final piece of the program is 

```go
fmt.Println("Hello, world")
```

And we can separade in 3 components: 1) we access another function inside the `fmt` package called `Println`; 2) we create a nre string that contains `"Hello, world"` and 3) we *invoke* that function with the string as the first (and only) argument.

## Chapter 2: Types
Go is a statically typed programming language, meaning that variables always have a specific type and that type cannot change.
Built-in types in Go are described as follows.

### 1) Numbers
#### Integers
Integers are numbers without a decimal component, like 1, 2, 3, etc.
Go integer types are `uint8`, `uint16`, `uint32`, `uint64`, `int8`, `int16`, `int32` and `int64`. 8, 16, 32 and 64 tell us how many bits each of these types use. `uint` means "unsigned integers", while `int` means "signed integers". Unsigned integers only have positive numbers (and zero).
Generally, if you're working with integers, you should just use the `int` type.

#### Floating-Point Numbers
Floating-point numbers are the ones that count with a decimal component, like 1.23, 12.8, 0.00003, etc.
The actual representation on a computer is fairly complicated and are inexact.
Like integers, floating-point numbers have a certain size.
Go has two floating-point types: `float32` and `float64` (single precision and double precision, respectively).
It has also types to represent complex numbers: `complex64` and `complex128`.
Generally, we stick to `float64`.

**Example**
On a folder that you'll create called *chapter2*, create a file *main.go* containing the following:

```go
package main

import "fmt"

func main() {
    fmt.Println("1 + 1 =", 1 + 1)
    fmt.Println("1 + 1 =", 1.0 + 1.0)
}
```
If you run the program, you should see

```shell
$ go run main.go
1 + 1 = 2
1 + 1 = 2
```

Go supports the following standard arithmetic operators: `+` addition, `-` subtraction, `*` multiplication, `/` division and `%` remainder.

#### Strings
A string is a sequence of characters with a definite lenght used to represent text.
The difference between using doublequotes "" or backticks `` is that **double quotes cannot contain newlinesand they allow special escape sequences.
`len("Helo, world")` finds the lenght of a string.
`"Hello, world"[1]` returs the letter "e" because it accesses the second character on a string.
`"Hello, " + "world"` concatenates two strings together.
A space is also considered a character.

#### Booleans
A boolean value is a 1-bit integer used to represent true and false. Three logical operators are used with boolean values:

&& - and

|| - or

! - not

We often use booleans to make decisions and represent binary distinctions.

## Chapter 3: Variables

## Chapter 4: Control Structures

## Chapter 5: Arrays, Slices and Maps

## Chapter 6: Functions

## Chapter 7: Structs and Interfaces

### Structs
A **struct** is a type that contains named fields. For example:

```go
type Circle struct {
    x float64
    y float64
    r float64
}
```
The `type` keyword introduces a new type. It's followed by the name od the type (`Circle` in this case), the keyword `struct` indicatin that we are defining a struct type, and a list of fields inside of curly braces.
Fields are like a set of grouped variables. Each fiels has a name and a type and is stored adjacent to the other fields in the struct.

After defining a struct, we can create an instance of our new `Circle` type in many ways

```go
var c Circle
c := new(Circle) // this allocates memory for all the fields, sets each of them to their zero value, and returns a pointer to the struct (*Circle)
c := Circle{x: 0, y: 0, r: 5}
c := Circle {0, 0, 5}
c := &Circle{0, 0, 5}
 ```
 **NOTE**: pointers are often used with structs so that functions can modify their contents.

 **Fields**
We can access fields using the `.` operator:

```go
fmt.Println(c.x, c.y, c.r)
c.x = 10
c.y = 5
```

Creating a function that uses a `Circle`:

```go
func circleArea(c *Circle) float64 {
    return math.Pi * c.r*c.r
}
```

our `main` stays:

```go
func main() {
    c := Circle {0, 0, 5}
    fmt.Println(circleArea(&c))
}
```

Note that we created a pointer inside `circleArea` function and we addressed it on main function. This happens because if we attempted to modify one of the fields inside of the circleArea function, it would not modify the original variable.

### Methods

```go
func (c *Circle) area() float64 {
    return math.Pi * c.r*c.r
}
```

In between the keyword `func` and the name of the function, we've added a *receiver*, that is like a parameter, but it allows us to call a function using the `.` ooperator: `fmt.Println(c.area())`

### Interfaces

```go
type Shape interface {
    area() float64
}
```

An interface is created using the `type` keyword, followed by a name and the keyword `interface`. But instead of defining fields, we're defining a *method set* (a list of methods that a type must have in order to *implement* the interface).
