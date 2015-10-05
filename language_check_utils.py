import language_check

def check(conversation):

    # The grammar checker
    tool = language_check.LanguageTool('en-US')

    human_readable_conversation = (" ".join(conversation)).strip()

    errors = tool.check(human_readable_conversation)

    if len(errors) > 0:
        return False
    else:
        return True
