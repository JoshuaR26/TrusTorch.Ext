// The array of words you want to trigger the popup
const domains = ["amazon.in", "flipkart.com"];

// The function that creates the popup window
function createPopup() {
  chrome.windows.create({
    url: "popup.html",
    width: 600,
    height: 400,
    type: "popup"
  });
}

// The function that checks if the current tab is on Amazon or Flipkart product page
function isProductPage(tab) {
  const url = new URL(tab.url);
  return domains.some(domain => url.hostname.endsWith(domain));
}

// The listener that handles the web navigation events
chrome.webNavigation.onCommitted.addListener((details) => {
  chrome.tabs.get(details.tabId, (tab) => {
    if (isProductPage(tab)) {
      createPopup();
    }
  });
});
