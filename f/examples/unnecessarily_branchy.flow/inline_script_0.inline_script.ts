import * as wmill from 'https://deno.land/x/windmill@v1.27.2/mod.ts'
import { sleep } from "https://deno.land/x/sleep/mod.ts";

export async function main() {
  let result = []
  for (let i = 0; i < 10; i++) {
    console.log('I should sleep')
    result.push(i)
    await sleep(0.2)
  }
  return result
}
