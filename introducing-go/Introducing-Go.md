# Introducing Go, by Caleb Doxsey
(link for the book [here](http://shop.oreilly.com/product/0636920046516.do))

## Chapter 1 - Getting Started
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

