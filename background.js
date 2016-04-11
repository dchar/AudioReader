// An example of a simple one-time request
/*
chrome.runtime.onMessage.addListener(function(response, sender, sendResponse) {
	alert(response);
});
*/

// Long-lived connection listener
chrome.runtime.onConnect.addListener(function(port) {
	port.postMessage({greeting:"TEST"});
});
