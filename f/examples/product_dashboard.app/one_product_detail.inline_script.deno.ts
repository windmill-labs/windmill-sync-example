export async function main(id: number) {
  if (!id) {
    return `
    <p class="text-sm text-gray-600 text-center pt-8">
      Select a row from the tablee
    </p>
    `;
  }
  const res = await fetch("https://dummyjson.com/products/" + id);
  const { brand, title, thumbnail, description } = await res.json();
  return `
  <img width="363" height="200" src="${thumbnail}">
  <p class="text-lg font-bold my-1">
    ${brand} ${title}
  </p>
  <p>
    ${description}
  </p>
  `;
}
