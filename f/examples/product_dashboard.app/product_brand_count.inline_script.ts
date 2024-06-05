export async function main(data: {brand: string}[]) {
  const result: {data: number[], labels: string[]} = {
    data: [],
    labels: []
  }
  if(!Array.isArray(data)) { return result }

  const count: Record<string, number> = {}
  data.forEach(({brand}) => {
    brand = brand.toLowerCase()
    if(count[brand]) {
      count[brand]++
    } else {
      count[brand] = 1
    }
  })
  Object.entries(count).forEach(([key, value]) => {
    result.data.push(value)
    result.labels.push(key)
  })
  return result
}
