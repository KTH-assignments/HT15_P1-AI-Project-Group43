import language_check

################################################################################
# Checks the grammatical correctness of a sentence, or a series of sentences.
################################################################################
def check(conversation):

    # The grammar checker
    tool = language_check.LanguageTool('en-US')

    # Since `conversation` is a list, join all words into a humanly readable form
    human_readable_conversation = ""
    for word in conversation:
        if word in [".", ",", "?"]:
            human_readable_conversation += word
        else:
            human_readable_conversation += " "
            human_readable_conversation += word

    # Remove whitespaces at the left and right of the conversation
    human_readable_conversation = human_readable_conversation.strip()

    errors = tool.check(human_readable_conversation)

    if len(errors) > 0:
        return False
    else:
        return True
