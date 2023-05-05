// import * as wmill from "https://deno.land/x/windmill@v1.82.0/mod.ts"

const websites = ["Indeed", "Glassdoor", "AngelList", "Hired", "Monster", "CareerBuilder", "SimplyHired", "Dice", "Upwork", "BEAMSTART"];

export async function main(search_result: string) {
  for (let website of websites) {
    if (search_result.includes(website)) {
      search_result = search_result.replace(website, "");
    }
  }
  return search_result;
}