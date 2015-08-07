from slacker import Slacker

from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import VersionProperty, StringProperty, \
    ExpressionProperty, ObjectProperty, PropertyHolder


class BotInformation(PropertyHolder):

    name = ExpressionProperty(title='Name', default='')
    icon = ExpressionProperty(
        title='Icon (URL or emoji)', default=':smiley_cat:')

    def get_bot_details(self, signal):
        """ Returns a dictionary of kwargs for the bot details.

        Given a signal, this method will construct a dictionary of kwargs
        for the Slack API call with the correct parameters. Mainly, it will
        figure out whether an icon is a URL or an emoji and use the correct
        parameter name
        """
        param_dict = dict()

        # Put the bot's name in the username field
        param_dict['username'] = self.name(signal)

        # If it starts and ends with a colon, it's an emoji code
        icon = self.icon(signal).strip()
        if icon.startswith(':') and icon.endswith(':'):
            param_dict['icon_emoji'] = icon
        else:
            param_dict['icon_url'] = icon

        return param_dict


@Discoverable(DiscoverableType.block)
class Slack(Block):

    """ Send messages to a slack channel as a bot """

    version = VersionProperty('0.1.0')
    api_token = StringProperty(
        title='Slack API Token', default='[[SLACK_API_TOKEN]]')
    channel = ExpressionProperty(title='Slack Channel', default='{{$channel}}',
                                 attr_default=AttributeError)
    message = ExpressionProperty(
        title='Message', default='{{$message}}', attr_default=AttributeError)

    bot_info = ObjectProperty(BotInformation, title='Bot Details')

    def __init__(self):
        super().__init__()
        self._slacker = None

    def configure(self, context):
        super().configure(context)
        self._slacker = Slacker(self.api_token)

    def process_signals(self, signals, input_id='default'):
        for signal in signals:
            try:
                self._send_message(
                    self.channel(signal),
                    self.message(signal),
                    **self.bot_info.get_bot_details(signal))
            except:
                self._logger.exception("Unable to send message for signal {}"
                                       .format(signal))

    def _send_message(self, to_channel, message, **kwargs):
        """ Send a message to a Slack channel

        Pass additional kwargs for additional parameters to be sent to the
        Slack API call. These parameters can be found here:
        https://api.slack.com/methods/chat.postMessage
        """
        self._logger.debug("Sending message {} to channel {}".format(
            message, to_channel))

        resp = self._slacker.chat.post_message(to_channel, message, **kwargs)

        if resp.body.get('ok'):
            self._logger.debug("Message {} sent successfully".format(message))
