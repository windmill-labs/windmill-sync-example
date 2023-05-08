export async function main(email: string) {
  let [name, domain] = email.split("@");
  let name_space = name.charAt(0) + " " + name.slice(1);
  name = name.replace(/[0-9]/g, " ");
  name_space = name_space.replace(/[0-9]/g, " ");
  const nameWithoutDots = name.replace(/\./g, " ");
  const commonDomains = [
    "gmail.com",
    "yahoo.com",
    "outlook.com",
    "hotmail.com",
    "aol.com",
    "icloud.com",
    "mail.ru",
    "yandex.ru",
    "live.com",
    "zoho.com",
    "protonmail.com",
    "gmx.com",
    "fastmail.com",
    "comcast.net",
    "verizon.net",
    "163.com",
    "qq.com",
    "sina.com",
    "naver.com",
    "t-online.de",
  ];

  const isCommonDomain = commonDomains.includes(domain);

  if (isCommonDomain) {
    return { name_space, name: nameWithoutDots, domain: "" };
  } else {
    return { name_space, name: nameWithoutDots, domain };
  }
}