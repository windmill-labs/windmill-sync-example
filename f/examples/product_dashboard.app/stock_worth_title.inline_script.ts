export async function main(data: {stock: number, price: number}[]) {
  const base = 'Stock Worth By Product'
  if(!Array.isArray(data)) { return base }

  const total = data.map(row => row.stock * row.price).reduce((acc, curr) => acc + curr)
  const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0,
  });
  return base + ` (Total Worth: ${formatter.format(total)})`
}
