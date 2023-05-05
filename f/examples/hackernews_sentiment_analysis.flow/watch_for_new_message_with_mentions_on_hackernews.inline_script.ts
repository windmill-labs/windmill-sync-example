import * as wmill from "https://deno.land/x/windmill@v1.25.0/mod.ts";

const MAX_LOOKBACK = 100;

export async function main(mentions: string[]) {
  console.log(wmill.getInternalStatePath());
  let lastState = await wmill.getInternalState();
  console.log(`lastState: ${lastState}`);

  let maxItem = await getMaxItem();
  console.log(`maxItem: ${maxItem}`);

  if (!lastState) {
    console.log(
      `First run of trigger, looking back to MAX_LOOKBACK (100) elements`,
    );
    lastState = maxItem - MAX_LOOKBACK;
  }

  maxItem = Math.min(maxItem, lastState + MAX_LOOKBACK);

  const items = [];
  for (let i = lastState; i < maxItem; i++) {
    console.log(`fetching id: ${i}`);
    const item = await getItem(i);
    if (mentions.find((mention) => item.text?.includes(mention))) {
      items.push(item);
    }
  }
  await wmill.setInternalState(maxItem);

  return items;
}

export async function getMaxItem() {
  const res = await fetch("https://hacker-news.firebaseio.com/v0/maxitem.json");
  return Number(await res.text());
}

export async function getItem(id: number) {
  const res = await fetch(
    `https://hacker-news.firebaseio.com/v0/item/${id}.json`,
  );
  return res.json();
}
