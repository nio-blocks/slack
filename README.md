Slack
===========

Send messages to a [Slack](http://slack.com) channel as a bot

Properties
--------------
 * Slack API Token - The API Token for your bot. Get a test token at the [Slack Web API page](https://api.slack.com/web).
 * Slack Channel - The channel to send your message to. You can use the channel name (prefixed with a hashtag) or you can use the channel ID returned from the API.
 * Message - The message to send to the channel.
 * Bot Info - Information about the bot that will be sending the message
    * Name - How the name should appear
    * Icon - The icon for the bot. This can either be a URL to an image or an emoji code. Emoji codes should start and end with a `:`. For example, `:smiley_cat:`. For a list of emoji codes see the [Emoji Cheat Sheet](http://www.emoji-cheat-sheet.com/)


Dependencies
----------------
 * [slacker](https://github.com/os/slacker)

Commands
----------------
None

Input
-------
Any list of signals.

Output
---------
None
