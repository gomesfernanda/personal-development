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

