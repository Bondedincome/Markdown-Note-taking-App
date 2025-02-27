import language_tool_python

tool = language_tool_python.LanguageTool('en-US')

def check_grammar(text: str):
    matches = tool.check(text)
    return [{"message": match.message, "offset": match.offset, "error": match.context} for match in matches]
