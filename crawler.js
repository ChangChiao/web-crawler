const puppeteer = require("puppeteer");
const nodemailer = require("nodemailer");

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    timeout: 60000,
  });
  const page = await browser.newPage();

  // Step 1: 前往頁面並點擊年齡確認
  await page.goto("https://www.ptt.cc/bbs/Gamesale/index.html", {
    waitUntil: "networkidle2",
  });
  await page.click('button:has-text("我同意，我已年滿十八歲")');

  // Step 2: 搜尋關鍵字「劍星」
  await page.waitForSelector(".search-bar input");
  await page.type(".search-bar input", "劍星");
  await page.keyboard.press("Enter");

  // Step 3: 等待 1 秒載入搜尋結果
  await page.waitForTimeout(1000);

  // Step 4: 擷取所有搜尋結果
  const results = await page.$$eval(".r-ent .title a", (nodes) => {
    return nodes.map((node) => node.innerText);
  });

  // Step 5: 檢查是否符合條件（劍星 + 售 + 今天日期）
  const today = new Date();
  const dateStr = today
    .toLocaleDateString("zh-TW", { month: "2-digit", day: "2-digit" })
    .replace("/", "/");

  const matched = results.find(
    (entry) =>
      entry.includes("劍星") && entry.includes("售") && entry.includes(dateStr)
  );

  // Step 6: 若符合條件，寄出 Email
  if (matched) {
    const transporter = nodemailer.createTransport({
      service: "gmail",
      auth: {
        user: process.env.GMAIL_USER,
        pass: process.env.GMAIL_PASS,
      },
    });

    await transporter.sendMail({
      from: process.env.GMAIL_USER,
      to: process.env.TARGET_EMAIL,
      subject: "PTT 有人在賣劍星",
      text: `找到符合的商品：\n\n${matched}`,
    });
  }

  await browser.close();
})();
