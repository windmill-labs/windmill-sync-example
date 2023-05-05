export async function main(completion: string) {
  const regex = /1. First Name: (.+)\n2. Last Name: (.+)\n3. Profession: (.+)\n4. Company: (.+)\n5. What the Company Does: (.+)/;
  const matches = completion.match(regex);
  if (!matches) {
    throw new Error("Invalid completion string");
  }

  const [, value1, value2, value3, value4, value5] = matches;
  const first_name = value1.trim();
  const last_name = value2.trim();
  const profession = value3.trim();
  const company = value4.trim();
  const what_company_does = value5.trim();

  return { first_name, last_name, profession, company, what_company_does };
}
