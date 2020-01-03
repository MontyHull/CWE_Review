package main

import (
    "fmt"
    )

func addSomeThing(thing int){
    if thing == 1{
        fmt.Println(thing,"line of text on the screen,",thing,"line of text.")
    } else {
        fmt.Println(thing,"lines of text on the screen,",thing,"lines of text.")
    }
    fmt.Println("Print it out, stand up and shout,",thing+1,"lines of text on the screen.\n")
}

func main(){
    var how_Many int;
    fmt.Print("How many lines? ")
    fmt.Scanln(&how_Many)
    for i := 1; i < how_Many; i++{
        addSomeThing(i)
    }
}
