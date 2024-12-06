#!/usr/bin/env swift
import Foundation

let file = "./input.txt"
let path = URL(fileURLWithPath: file)
guard let text = try? String(contentsOf: path, encoding: .ascii) else {
    print("Could not read file!")
    exit(1)
}

let values =
    text
    .trimmingCharacters(in: .newlines)
    .components(separatedBy: .newlines)
    .map { $0.components(separatedBy: "   ").map({ Int($0)! }) }

let leftList = values.map({ $0[0] }).sorted()
let rightList = values.map({ $0[1] }).sorted()

let answer = zip(leftList, rightList)
    .map { abs($0.0 - $0.1) }
    .reduce(0, +)

print(answer)
