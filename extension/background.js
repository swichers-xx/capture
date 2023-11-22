// Function to handle sending data
function sendData(data) {
    chrome.storage.local.get(['ip', 'port'], function(settings) {
      if (settings.ip && settings.port) {
        const url = `http://${settings.ip}:${settings.port}/receive_data`;
  
        fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch(error => console.error('Error:', error));
      }
    });
  }
  
  // Function to handle history data
  function handleHistoryData(historyItems) {
    // Assuming your server expects an array of URLs
    const data = historyItems.map(item => item.url);
    sendData(data);
  }
  
  // Listen for messages from popup
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "exportHistory") {
      chrome.history.search({ text: '', maxResults: 100 }, handleHistoryData);
    }
  });
  