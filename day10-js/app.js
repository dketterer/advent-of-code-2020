const fs = require('fs')


function range(start, stop, step) {
    var a = [start], b = start
    while (b < stop) {
        a.push(b += step || 1)
    }
    return (b > stop) ? a.slice(0, -1) : a
}


function find_next(index, obj) {
    if (index >= obj.jolts.length - 1) {
        obj.map[index] = 1
        return 1
    }
    if (obj.map[index]) {
        return obj.map[index]
    }

    let to_go = 3
    result = 0
    for (const offset of range(1, 3, 1)) {
        if (obj.jolts[index + offset] <= to_go) {

            result += find_next(index + offset, obj)

            to_go -= obj.jolts[index + offset]
        } else break
    }
    obj.map[index] = result
    return result
}

const toNumbers = arr => arr.map(Number)

fs.readFile(__dirname + "/input.txt", (err, file) => {
    const lines = file.toString().split("\n")
    let jolts = toNumbers(lines)
    jolts.sort((a, b) => a - b)

    let delta_jolts = [0]
    let prev = 0
    for (const jolt of jolts) {
        delta_jolts.push(jolt - prev)
        prev = jolt
    }

    let diff_1 = 0
    let diff_3 = 1
    for (const jolt of delta_jolts.slice(1)) {
        if (jolt >= 1 && jolt <= 3) {
            if (jolt === 1) diff_1++
            if (jolt === 3) diff_3++
        } else break;
    }
    console.log("Part 1: " + (diff_1 * diff_3))

    let obj = {
        jolts: delta_jolts,
        map: new Map()
    }
    result = find_next(0, obj)
    console.log("Part 2: " + result)
})