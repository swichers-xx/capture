document.addEventListener('DOMContentLoaded', () => {
    // Load stored IP and port
    chrome.storage.local.get(['ip', 'port'], function(result) {
      document.getElementById('ip').value = result.ip || '';
      document.getElementById('port').value = result.port || '';
    });
  
    // Save IP and port when button is clicked
    document.getElementById('saveSettings').addEventListener('click', () => {
      let ip = document.getElementById('ip').value;
      let port = document.getElementById('port').value;
      
      chrome.storage.local.set({ ip: ip, port: port }, () => {
        console.log('Settings saved');
      });
    });
  });
  