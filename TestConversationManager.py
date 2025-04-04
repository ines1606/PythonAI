import unittest
import ConversationManager as c


class TestConversationManager(unittest.TestCase):
    c_manager = c.ConversationManager()
    c_manager.conversation_history.append({"role":"user", "content":"Hallo! Wie gehts?"})


    def test_total_tokens_used(self):
        print(self.c_manager.total_tokens_used())

    def test_print_history(self):
        self.c_manager.print_history()

    def test_enforce_token_budget(self):
        self.c_manager.enforce_token_budget()
        self.test_print_history()

    

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestConversationManager("test_enforce_token_budget"))
    suite.addTest(TestConversationManager("test_print_history"))
    suite.addTest(TestConversationManager("test_total_tokens_used"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())