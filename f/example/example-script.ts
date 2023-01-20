import * as wmill from "https://deno.land/x/windmill@v1.60.0/mod.ts";
export async function main() {
  console.log(await wmill.getVariable("f/example/example-variable"));
}
