package main

import (
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
)

const (
	execAllowedInstruction   = "do()"
	execForbiddenInstruction = "don't()"
)

const (
	mulInstructionPattern            = `mul\(\d{1,3},\d{1,3}\)`
	conditionalMulInstructionPattern = `(do\(\)|don't\(\)|mul\(\d{1,3},\d{1,3}\))`
)

func loadInput(filePath string) []string {
	input, err := os.ReadFile(filePath)
	if err != nil {
		log.Fatalln("Error on reading input file", err)
	}
	return strings.Split(string(input), "\n")
}

func findAllInstructions(memory []string, pattern string) []string {
	regex := regexp.MustCompile(pattern)
	instructions := []string{}
	for _, line := range memory {
		matches := regex.FindAllString(line, -1)
		if matches != nil {
			instructions = append(instructions, matches...)
		}
	}
	return instructions
}

func computeMulInstruction(instruction string) int {
	parts := strings.Split(instruction[4:len(instruction)-1], ",")
	if len(parts) != 2 {
		log.Fatalln("Invalid mul instruction:", instruction)
	}

	a, err := strconv.Atoi(parts[0])
	if err != nil {
		log.Fatalln("Error converting mul part to int:", parts[0])
	}

	b, err := strconv.Atoi(parts[1])
	if err != nil {
		log.Fatalln("Error converting mul part to int:", parts[1])
	}

	return a * b
}

func executeInstructions(instructions []string) int {
	execAllowed := true
	result := 0
	for _, instruction := range instructions {
		if instruction == execAllowedInstruction {
			execAllowed = true
		} else if instruction == execForbiddenInstruction {
			execAllowed = false
		} else if execAllowed {
			result += computeMulInstruction(instruction)
		}
	}
	return result
}

func scanAndExecute(memory []string, pattern string) int {
	mulInstructions := findAllInstructions(memory, pattern)
	return executeInstructions(mulInstructions)
}

func main() {
	filePath := "input"
	if len(os.Args) > 1 {
		filePath = os.Args[1]
	}

	corruptedMemory := loadInput(filePath)

	partOneResult := scanAndExecute(corruptedMemory, mulInstructionPattern)
	log.Println("Sum of mul instructions:", partOneResult)

	partTwoResult := scanAndExecute(corruptedMemory, conditionalMulInstructionPattern)
	log.Println("Sum of mul instructions with conditions:", partTwoResult)
}
