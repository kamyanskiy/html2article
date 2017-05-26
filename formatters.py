import textwrap


class ParseHelper(object):
    @staticmethod
    def format_text_for_a_element(aitem):
        return "[{0}] {1}".format(aitem["href"], aitem.get_text())

    @staticmethod
    def format_text_line(item):
        result = []
        if item.find_all("a"):
            for line in item.children:
                text = line
                if line.name == "a":
                    text = ParseHelper.format_text_for_a_element(line)
                result.append(text.strip())
        else:
            return item.get_text().strip()
        return "".join(result)

    @staticmethod
    def format_text(article_list):
        text = ''
        for line in article_list:
            if len(line) <= 80:
                text += line
            else:
                text += textwrap.fill(line, 80)
            text += "\n\n"
        return text