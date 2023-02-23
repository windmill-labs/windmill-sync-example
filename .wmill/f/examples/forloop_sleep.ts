import { sleep } from "https://deno.land/x/sleep/mod.ts";

export async function main() {
  for (let i = 0; i < 20; i++) {
    console.log("sleeping...");
    await sleep(0.6);
  }
  return "woke up";
}
