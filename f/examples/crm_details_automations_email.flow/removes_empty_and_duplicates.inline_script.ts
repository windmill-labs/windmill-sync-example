// import * as wmill from "https://deno.land/x/windmill@v1.83.1/mod.ts"

export async function main(r1?: string, r2?: string, r3?: string, r4?: string) {
  // Assign empty strings to undefined inputs
  const inputs = [r1, r2, r3, r4].map((input) => input ?? "");
  
  const results = inputs.filter((result, index, array) => {
    // Remove empty values
    if (result.trim() === "") {
      return false;
    }
    // Remove duplicates
    return array.indexOf(result) === index;
  });
  
  return results;
}