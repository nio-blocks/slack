from unittest.mock import MagicMock
from collections import defaultdict
from nio.common.signal.base import Signal
from nio.util.support.block_test_case import NIOBlockTestCase
from ..slack_block import Slack


class TestSlack(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        # This will keep a list of signals notified for each output
        self.last_notified = defaultdict(list)

    def signals_notified(self, signals, output_id='default'):
        self.last_notified[output_id].extend(signals)

    def test_send_message(self):
        """ Tests that messages get sent under the default conditions """
        blk = Slack()
        self.configure_block(blk, {
            'message': '{{$message}}',
            'channel': '{{$channel}}',
            'api_token': 'FAKE TOKEN',
            'bot_info': {
                'name': 'Bot Name',
                'icon': ':bot_emoji:'
            }
        })
        mock = blk._slacker.chat.post_message = MagicMock()
        blk.start()
        blk.process_signals([Signal({
            'message': 'This is my message',
            'channel': 'This is my channel'
        })])
        blk.stop()

        mock.assert_called_once_with(
            'This is my channel', 'This is my message',
            icon_emoji=':bot_emoji:', username='Bot Name')

    def test_send_message_icon_url(self):
        """ Tests that messages get sent when a URL is supplied for an icon """
        blk = Slack()
        self.configure_block(blk, {
            'message': '{{$message}}',
            'channel': '{{$channel}}',
            'api_token': 'FAKE TOKEN',
            'bot_info': {
                'name': 'Bot Name',
                'icon': 'http://ICONURL'
            }
        })
        mock = blk._slacker.chat.post_message = MagicMock()
        blk.start()
        blk.process_signals([Signal({
            'message': 'This is my message',
            'channel': 'This is my channel'
        })])
        blk.stop()

        mock.assert_called_once_with(
            'This is my channel', 'This is my message',
            icon_url='http://ICONURL', username='Bot Name')

    def test_no_message(self):
        """ Tests message is not sent if it can't be found on the signal """
        blk = Slack()
        self.configure_block(blk, {
            'message': '{{$message}}',
            'channel': '{{$channel}}',
            'api_token': 'FAKE TOKEN',
            'bot_info': {}
        })
        mock = blk._slacker.chat.post_message = MagicMock()
        blk.start()
        blk.process_signals([Signal({
            'not_a_message': 'This is my message',
            'channel': 'This is my channel'
        })])
        blk.stop()

        self.assertEqual(mock.call_count, 0)

    def test_no_channel(self):
        """ Tests message is not sent if channel can't be found """
        blk = Slack()
        self.configure_block(blk, {
            'message': '{{$message}}',
            'channel': '{{$channel}}',
            'api_token': 'FAKE TOKEN',
            'bot_info': {}
        })
        mock = blk._slacker.chat.post_message = MagicMock()
        blk.start()
        blk.process_signals([Signal({
            'message': 'This is my message',
            'not_a_channel': 'This is my channel'
        })])
        blk.stop()

        self.assertEqual(mock.call_count, 0)

    def test_bad_expression(self):
        """ Tests message is not sent if there is an invalid expression """
        blk = Slack()
        self.configure_block(blk, {
            'message': '{{ message }}',  # this is a bad expression
            'channel': '{{ $channel }}',
            'api_token': 'FAKE TOKEN',
            'bot_info': {}
        })
        mock = blk._slacker.chat.post_message = MagicMock()
        blk.start()
        blk.process_signals([Signal({
            'message': 'This is my message',
            'channel': 'This is my channel'
        })])
        blk.stop()

        self.assertEqual(mock.call_count, 0)
