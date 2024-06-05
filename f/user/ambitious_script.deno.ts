// Ctrl/CMD+. to cache dependencies on imports hover.

// import { toWords } from "npm:number-to-words@1"
// import * as wmill from "https://deno.land/x/windmill@v1.138.4/mod.ts"

// fill the type, or use the +Resource type to get a type-safe reference to a resource
// type Postgresql = object

export async function main(
  a: number,
  b: "my" | "enum",
  //c: Postgresql,
  d = "inferred type string from default arg",
  e = { nested: "object" },
  //e: wmill.Base64
) {
  // let x = await wmill.getVariable('u/user/foo')
  return { foo: a };
}
