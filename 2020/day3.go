package main

import "fmt"
import "log"
import "bufio"
import "os"

func readFile(filename string) ([]string, err) {
	lines = []string
	file, err := os.Open(filename)
    if err != nil {
        return nil, error
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    // optionally, resize scanner's capacity for lines over 64K, see next example
    for scanner.Scan() {
		lines = append(lines, scanner.Text())
    }

    if err := scanner.Err(); err != nil {
        log.Fatal(err)
    }
}

func main() {
   fmt.Println("Hello, World!")
}