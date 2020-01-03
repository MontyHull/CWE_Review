package main

import (
    "fmt"
    "time"
)

func prime_factor(numb int){
    var orignumb int = numb
    for i := 2; i <= numb; i++{
        if numb%i == 0{
            is_i_prime := true
            for j := 2; j < i; j++{
                if i%j == 0{
                    is_i_prime = false
                }
            }
            if is_i_prime && i != orignumb {
                fmt.Print(i," ")
                numb = numb/i
                i = 1
            }
        }
    }
}

func addSomeThing(thing int){
    if thing == 1{
        fmt.Println(thing,"line of text on the screen,",thing,"line of text.")
        } else {
            fmt.Println(thing,"lines of text on the screen,",thing,"lines of text.")
        }
        fmt.Println("Print it out, stand up and shout,",thing+1,"lines of text on the screen.\n")
}

func main(){
    for i := 1; i < 5; i++{
        addSomeThing(i)
        time.Sleep(time.Duration(1)*time.Second)
    }
}
