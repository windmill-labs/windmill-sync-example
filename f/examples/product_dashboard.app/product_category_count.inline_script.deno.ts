export async function main(data: {category: string}[]) {
  const result: {data: number[], labels: string[]} = {
    data: [],
    labels: []
  }
  if(!Array.isArray(data)) { return result }

  const count: Record<string, number> = {}
  data.forEach(({category}) => {
    if(count[category]) {
      count[category]++
    } else {
      count[category] = 1
    }
  })
  Object.entries(count).forEach(([key, value]) => {
    result.data.push(value)
    result.labels.push(key)
  })
  return result
}
