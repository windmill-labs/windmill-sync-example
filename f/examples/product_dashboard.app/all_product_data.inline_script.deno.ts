export async function main() {
  const res = await fetch('https://dummyjson.com/products')
  const json = await res.json()
  return json.products.map((p: Record<string, any>) => {
    delete p.images
    delete p.thumbnail
    delete p.description
    return p
  })
}
