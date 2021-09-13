from markovify import NewlineText
from .chain import SQLChainState3

class TweetgenNewlineText(NewlineText):
    def sentence_join(self, sentences):
        return "".join(sentences)
    def word_join(self, words):
        return "".join(words)

    @classmethod
    def from_sql(cls, user_ids):
        return cls(
            None,
            state_size=SQLChainState3.state_size,
            chain=SQLChainState3(user_ids),
        )
