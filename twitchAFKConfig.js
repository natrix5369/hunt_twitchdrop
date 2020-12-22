/* Config */
exports.channel = "sleepydragn1"; // Channel name to AFK at, UNLESS SPECIFIED VIA COMMAND LINE ARGUMENT
exports.furtherAuthDetection = true; // Detect reCAPTCHAs, 2FA, or other authentication methods after login and pause for user input. true for enabled, false for disabled.
exports.streamAudio = false; // Determines if the stream has its audio muted or not. Should have no effect on drops. true to enable audio, false to disable it.
exports.logging = true; // Exports console output to log files stored in the logs subfolder. true for enabled, false for disabled.

/* Video Quality */
exports.maxQuality = "MIN"; // Maximum video quality setting to use
// Possible Values:
// "MAX" or "SOURCE"
// "AUTO"
// "1080p60"
// "1080p"
// "720p60"
// "720p"
// "480p"
// "360p"
// "160p"
// "MIN"

/* Application Resolution */
exports.width = 1280; // Width of the application window. Does not affect the stream resolution.
exports.height = 720; // Height of the application window. Does not affect the stream resolution.

/* Refresh Rate */
exports.minRefreshRate = 1440; // Minimum rate of how often the page should be refreshed in minutes
exports.maxRefreshRate = 1445; // Maximum rate of how often the page should be refreshed in minutes

/* Pause Rate */
exports.minPauseRate = 2; // Minimum rate of how often to pause the stream in minutes
exports.maxPauseRate = 5; // Maximum rate of how often to pause the stream in minutes

/* Chat */
// Have some respect for your fellow chat members, please do not set the rate below 2 minutes.
exports.chatSpamEnabled = true; // To chat spam, or not to chat spam? true for enabled, false for disabled.
exports.minChatSpamRate = 2; // Minimum rate of how often to spam chat with a randomized message in minutes
exports.maxChatSpamRate = 3;  // Maximum rate of how often to spam chat with a randomized message in minutes
exports.chatSpams = [ // Array of randomized messages for chat spam - should be kept in quotes and seperated with a comma
	"LUL",
	"LUL LUL",
	"LUL LUL LUL",
	"TPFufun",
	"VoteYea",
	"VoteYea VoteYea",
	"VoteYea VoteYea VoteYea",
	"Kappa",
	"Kappa Kappa",
	"Kappa Kappa Kappa",
	"KonCha",
	"TehePelo"
];

/* Credentials */
exports.username = "natrix5369"; // Twitch username
exports.password = "Epa53691997"; // Twitch password

/* Channel Points */
exports.claimBonusPoints = true; // Claims bonus channel points when they pop up. true for enabled, false for disabled.
exports.pointTracker = false; // Keeps track of channel points and outputs to the console when they increase. true for enabled, false for disabled.
exports.pointTrackerRate = 5; // The rate at which channel points are checked and messages are sent out, in minutes

/* Debug */
exports.printSlimerErrors = true; // Output SlimerJS related error messages. true for enabled, false for disabled.
exports.printSlimerErrorsStack = false; // Output SlimerJS stack traces as well. Requires printSlimerErrors to be enabled. true for enabled, false for disabled.
exports.printJSConsole = false; // Output in-page console messages. true for enabled, false for disabled.
exports.printJSErrors = false; // Output in-page JavaScript errors. true for enabled, false for disabled.
exports.printJSErrorsStack = false; // Output stack traces as well. Requires printJSErrors to be enabled. true for enabled, false for disabled.
exports.printJSErrorsStackVerbose = false; // If true, prints THE WHOLE STACK. If false, only prints the last line. Requires printJSErrors and printJSErrorsStack to be enabled.