import unittest

from pywce import DictSessionManager, EngineConfig, WhatsAppConfig, WhatsApp, Engine


class TestPywceEngine(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        session_manager = DictSessionManager()
        start_menu = "START_MENU"

        self.webhook_headers = {
            'x-hub-signature-256': 'dsagsfgfsa',
        }

        self.webhook_payload = {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "8856996819413533",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "16505553333",
                                    "phone_number_id": "27681414235104944"
                                },
                                "contacts": [
                                    {
                                        "profile": {
                                            "name": "PyWCE"
                                        },
                                        "wa_id": "263770123456"
                                    }
                                ],
                                "messages": [
                                    {
                                        "from": "16315551234",
                                        "id": "wamid.ABGGFlCGg0cvAgo-sJQh43L5Pe4W",
                                        "timestamp": "1603059201",
                                        "text": {
                                            "body": "Hie"
                                        },
                                        "type": "text"
                                    }
                                ]
                            },
                            "field": "messages"
                        }
                    ]
                }
            ]
        }

        wa_config = WhatsAppConfig(
            token="TOKEN",
            phone_number_id="PHONE_NUMBER_ID",
            hub_verification_token="HUB_VERIFICATION_TOKEN",
            use_emulator=True
        )

        whatsapp_obj = WhatsApp(whatsapp_config=wa_config)

        config = EngineConfig(
            whatsapp=whatsapp_obj,
            templates_dir="test_templates",
            trigger_dir="test_triggers",
            start_template_stage=start_menu,
            session_manager=session_manager
        )

        self.start_menu = start_menu
        self.engine = Engine(config=config)

    async def test_message_processing(self):
        result = await self.engine.process_webhook(webhook_data=self.webhook_payload,
                                                   webhook_headers=self.webhook_headers)
        self.assertIsNone(result, "Webhook did not return result")


if __name__ == '__main__':
    unittest.main()
