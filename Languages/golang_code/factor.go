package main

import(
    "fmt"
    )

func main(){
    // keep a flag to see if you have printed before
    // if you havent print ("i") else print (" i")
    var numb int = 24
    var orignumb int = numb
    fmt.Print("(")
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
    fmt.Print(")")
}
