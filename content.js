// An example of a simple one-time request
//chrome.runtime.sendMessage("hello");

// This line opens up a long-living connection to the background script
var port = chrome.runtime.connect({name:"contentPort"});

port.onMessage.addListener(function(message, sender) {
	if (message.greeting == "TEST") {
		//alert(message.greeting);
	}
});



