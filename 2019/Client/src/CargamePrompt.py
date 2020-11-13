from IPython.terminal.prompts import Prompts, Token

class CargamePrompt(Prompts):
    def in_prompt_tokens(self, cli=None):
        return [(Token.Prompt, 'root@kali# ')]
    def out_prompt_tokens(self):
        return [(Token, " result: ")]