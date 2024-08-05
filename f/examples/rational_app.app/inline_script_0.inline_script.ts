type gmail = {}
export async function main(x: gmail) {
    if (Object.keys(x ?? {}).length > 0) {
      return []
    }
    return [
        {
            "id": 1,
            "name": "A cell with a long name",
            "age": 42
        },
        {
            "id": 2,
            "name": "A briefer cell",
            "age": 84
        }
    ]
}