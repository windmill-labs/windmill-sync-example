export async function main(
  a: number,
  b: "my" | "enum",
  //c: Postgresql,
  d = "inferred type string from default arg",
  e = { nested: "object" }
  //e: wmill.Base64
) {
  "fooooooo";
  // let x = await wmill.getVariable('u/user/foo')
  return { foo: a };
}
