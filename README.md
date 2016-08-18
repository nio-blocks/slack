Slack
=====

Send messages to a [Slack](http://slack.com) channel as a bot

Properties
----------
 * **slack_api_token**: The API Token for your bot. Get a test token at the [Slack Web API page](https://api.slack.com/web).
 * **slack_channel**: The channel to send your `message` to. You can use the channel name (prefixed with a hashtag) or you can use the channel ID returned from the API.
 * **message**: The `message` to send to the `channel`.
 * **bot_info**: Information about the bot that will be sending the `message`
    * *Name*: How the name should appear
    * *Icon*: The icon for the bot. This can either be a URL to an image or an emoji code. Emoji codes should start and end with a `:`. For example, `:smiley_cat:`. For a list of emoji codes see the [Emoji Cheat Sheet](http://www.emoji-cheat-sheet.com/)


Dependencies
------------
 * [slacker](https://github.com/os/slacker)

Commands
--------
None

Input
-----
Any list of signals.

Output
------
EnrichSignals mixin is used to pass through input signals and enrich them with the [response](https://api.slack.com/methods/chat.postMessage) from the Slack request.

```python
{
  "successful": True,
  "error": None,
  "body": {
    "ok": True,
    "ts": "1405895017.000506",
    "channel": "C024BE91L",
    "message": {
      "type": "message",
      "username": "hansmosh",
      "text": "i <3 n.io",
      "ts": "1405895017.000506",
        …
    }
  },
  "raw": '{"ok":true,"chanel":"C024BE91L",...}'
}
```
