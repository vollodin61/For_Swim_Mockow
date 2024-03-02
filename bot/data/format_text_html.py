"""Это чтоб сообщения писать в разном формате
	вообще есть встроенные функции у aiogram, но я о них узнал позже
"""

def bold(some_text):
	return f"<b>{some_text}</b>"


def italic(some_text):
	return f"<i>{some_text}</i>"


def underline(some_text):
	return f"<u>{some_text}</u>"


def strikethrough(some_text):  # зачёркнутый
	return f"<s>{some_text}</s>"


def monospace(some_text):
	return f"<code>{some_text}</code>"


def text_to_link_url(url, some_text):
	return f"<a href={url}>{some_text}</a>"


def text_to_spoiler(some_text):  # скрытый к нему нужно прикрутит
	return f"<spoiler>{some_text}</spoiler>"


def text_to_code(some_code_in_string):
	return (f'<pre language="python">\n'
			f"{some_code_in_string}\n"
			f"</pre>")
