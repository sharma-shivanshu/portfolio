import re

filepath = './projects/market-tracker/index.html'
with open(filepath, 'r') as f:
    content = f.read()

# Replace the tryLive function with a Yahoo Finance based one
yahoo_script = """
async function tryLive() {
  let hit = false;
  
  // Yahoo Finance Symbols
  const symbols = {
    nifty: '^NSEI',
    sensex: '^BSESN',
    gold: 'GC=F' // Gold Futures USD
  };
  
  // Need USD/INR for gold conversion
  let usdInr = 83.5; 
  try {
    const res = await fetch('https://api.allorigins.win/raw?url=' + encodeURIComponent('https://query1.finance.yahoo.com/v8/finance/chart/INR=X?interval=1d&range=1d'));
    const data = await res.json();
    if(data.chart.result[0].meta.regularMarketPrice) usdInr = data.chart.result[0].meta.regularMarketPrice;
  } catch(e) {}

  for (const [k, sym] of Object.entries(symbols)) {
    try {
      const url = `https://api.allorigins.win/raw?url=` + encodeURIComponent(`https://query1.finance.yahoo.com/v8/finance/chart/${sym}?interval=1d&range=10d`);
      const res = await fetch(url);
      const data = await res.json();
      const result = data.chart.result[0];
      const timestamps = result.timestamp;
      const closes = result.indicators.quote[0].close;
      
      let rows = [];
      for (let i = 0; i < timestamps.length; i++) {
        if (closes[i] !== null && closes[i] !== undefined) {
          let d = new Date(timestamps[i] * 1000);
          let dateStr = d.toLocaleDateString('en-IN', { month: 'short', day: 'numeric' });
          
          let price = closes[i];
          // Gold from USD/oz to INR/10g
          if(k === 'gold') {
              price = (price * usdInr) / 31.1034768 * 10;
          }
          
          rows.push({ date: dateStr, close: Math.round(price) });
        }
      }
      
      // take last 7
      rows = rows.slice(-7);
      
      if (rows.length >= 3) {
        D[k].prices = rows.map(r => r.close);
        D[k].dates = rows.map(r => r.date);
        hit = true;
      }
    } catch(e) {
      console.error("Failed fetching for", k, e);
    }
  }
  
  if (hit) {
    drawCards(true);
    drawAll();
    document.getElementById('updated').textContent = '✓ Live Data (Yahoo Finance) · Updated: ' + new Date().toLocaleTimeString('en-IN');
  } else {
    // Generate dates up to today for indicative data
    let today = new Date();
    let dates = [];
    for(let i=6; i>=0; i--) {
        let d = new Date(today);
        d.setDate(d.getDate() - i);
        dates.push(d.toLocaleDateString('en-IN', {month:'short', day:'numeric'}));
    }
    D.nifty.dates = dates;
    D.sensex.dates = dates;
    D.gold.dates = dates;
    drawCards(false);
    drawAll();
    document.getElementById('updated').textContent = '⚠ Indicative data (live fetch failed) · ' + new Date().toLocaleTimeString('en-IN');
  }
}
"""

content = re.sub(r'async function tryLive\(\) \{.*\}', yahoo_script.strip(), content, flags=re.DOTALL)

with open(filepath, 'w') as f:
    f.write(content)
