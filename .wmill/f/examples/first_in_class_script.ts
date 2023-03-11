// Ctrl+. to cache dependencies on imports hover, Ctrl+S to format.

// import { toWords } from "npm:number-to-words@1"
// import * as wmill from "https://deno.land/x/windmill@v1.74.2/mod.ts"

export async function main(
  a: number,
  b: "my" | "enum",
  d = "inferred type string from default arg",
  c = { nested: "object" },
  //e: wmill.Base64
) {
  // let x = await wmill.getVariable('u/user/foo')foo
  return { foo: a };
}
