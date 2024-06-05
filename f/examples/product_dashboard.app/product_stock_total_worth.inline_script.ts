export async function main(data: {brand: string, title: string, stock: number, price: number}[]) {
  const result: {data: number[], labels: string[]} = {
    data: [],
    labels: []
  }
  if(!Array.isArray(data)) { return result }

  const count: Record<string, number> = {}
  data.forEach(row => {
    const key = `${row.brand} ${row.title}`
    const value = row.stock * row.price
    count[key] = value
  })
  Object.entries(count).forEach(([key, value]) => {
    result.data.push(value)
    result.labels.push(key)
  })
  return result
}
